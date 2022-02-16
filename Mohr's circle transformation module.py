# Packages
import os
from typing import Tuple
import numpy as np
from numpy.lib.utils import byte_bounds
import openpyxl as ex
from tkinter import *
from tkinter import ttk
from math import *
from sys import *
# from os import *
from subprocess import *
import matplotlib.path
import matplotlib.pylab as plt
from numpy import cos
from numpy import pi

Sigma_max = 0
Sigma_min = 0
Ta_max = 0
teta = 0
Sigmax = 0
Sigmay = 0
ta_xy = 0
Sigma_x = 0
Ta_xy = 0
Sigma_y = 0


# Calculations
def Calculations():
    global Sigma_max, Sigma_min, Ta_max, teta, Sigmax, Sigmay, ta_xy, Sigma_x, Ta_xy, Sigma_y

    Sigma_x = int(Sigma_x1.get())
    Sigma_y = int(Sigma_y1.get())
    Ta_xy = int(En3.get())
    alpha = int(teta2.get()) * ((2 * np.pi) / 360)
    teta = 90
    textFile = 'done!'

    Ta_yx = -Ta_xy
    # sigma average
    Sigma_avg = (Sigma_y + Sigma_x) / 2
    # Radius of mohr circle
    R = np.sqrt(Ta_xy ** 2 + (Sigma_x - Sigma_avg) ** 2)
    # principal stresses
    Sigma_max = R + Sigma_avg
    Sigma_min = -R + Sigma_avg
    Ta_max = R
    # angel of principal planes
    if (Ta_xy >= 0 and Sigma_x > Sigma_y) or (Ta_xy <= 0 and Sigma_y > Sigma_x):
        teta1 = -0.5 * np.arctan(2 * abs(Ta_xy) / abs(Sigma_x - Sigma_y))
        teta = (360 * teta1) / (2 * np.pi)
    elif (abs(Sigma_y - Sigma_x) != 0):
        teta1 = 0.5 * np.arctan(2 * abs(Ta_xy) / abs(Sigma_y - Sigma_x))
        teta = (360 * teta1) / (2 * np.pi)
    else:
        teta1 = np.pi / 2
        teta = 90

    # beta function (the angel between new diameter(new XY) and x axis)
    def f(teta1, alpha):
        if (teta1 < 0 and alpha > 0) or (teta1 > 0 and alpha < 0):
            beta = 2 * abs(teta1) + 2 * abs(alpha)
            return (abs(teta1) / teta1) * beta
        elif (teta1 > 0 and alpha > 0) or (teta1 < 0 and alpha < 0):
            beta = 2 * abs(teta1) - 2 * abs(alpha)
            return (abs(teta1) / teta1) * beta

    beta = f(teta1, alpha)
    teta_deg = teta1 * (180 / np.pi)
    beta_deg = beta * (180 / np.pi)
    alpha_deg = alpha * (180 / np.pi)
    deg = [teta_deg, beta_deg, alpha_deg]

    # stresses in angel alpha
    if Sigma_x > Sigma_y:
        a = np.array([[1, -1], [1, 1]])
    else:
        a = np.array([[-1, 1], [1, 1]])

    b = np.array([2 * R * abs(np.cos(abs(beta))), 2 * Sigma_avg])
    c = np.linalg.solve(a, b)
    if abs(beta) <= (np.pi) / 2:
        Sigmax = c[0]
        Sigmay = c[1]
    else:
        Sigmay = c[0]
        Sigmax = c[1]

    ta_xy = R * abs(np.sin(abs(beta)))
    if beta * teta1 <= 0:
        ta_xy = -ta_xy

    print(a, b, c, Sigma_x)
    Lis.insert(END, f'\u03C3 max = {round(Sigma_max, 3)}')
    Lis.insert(END, f'\u03C3 min = {round(Sigma_min, 3)}')
    Lis.insert(END, f'\u03C4 max = {round(Ta_max, 3)}')
    Lis.insert(END, f'\u03B8 = {round(teta, 3)}')
    Lis.insert(END, f'\u03C3\' x = {round(Sigmax, 3)}')
    Lis.insert(END, f'\u03C3\' y = {round(Sigmay, 3)}')
    Lis.insert(END, f'\u03C4\' xy = {round(ta_xy, 3)}')
    return deg


def mohr(S):
    plt.clf()
    """Plot Mohr circle for a 2D tensor"""
    S11 = S[0][0]  # sigma x
    S12 = S[0][1]  # Ta_xy
    S22 = S[1][1]  # sigma y
    center = [(S11 + S22) / 2.0, 0.0]
    radius = np.sqrt((S11 - S22) ** 2 / 4.0 + S12 ** 2)
    Smin = center[0] - radius
    Smax = center[0] + radius

    # print("Minimum Normal Stress: %g" % Smin)
    # print("Maximum Normal Stress: %g" % Smax)
    # print("Average Normal Stress: %g" % center[0])
    # print("Minimum Shear Stress: %g" % -radius)
    # print("Maximum Shear Stress: %g" % radius)

    plt.quiver([0, int(Sigma_min)], [int(-Ta_max), 0], [0, int(abs(Sigma_max) + abs(Sigma_min))], [int(Ta_max) * 2, 0],
               angles='xy', scale_units='xy', scale=1)
    # plt.plot([1000,0],[0,0], color = 'black', lw = 1.5)
    # plt.plot([0,0],[-1000,0] , color = 'black' , lw = 1.5)
    plt.xlim(-100, 100)
    plt.ylim(-100, 100)
    plt.plot(0, 0, 'o')
    circ = plt.Circle((center[0], 0), radius, facecolor='None', lw=2,
                      edgecolor='navy')
    plt.axis('image')
    ax = plt.gca()
    ax.add_artist(circ)
    ax.set_xlim(Smin - .1 * radius, Smax + .1 * radius)
    ax.set_ylim(-1.1 * radius, 1.1 * radius)
    print(Calculations()[1])
    if ta_xy >=0 :
        plt.plot([Sigmay, Sigmax], [-ta_xy, ta_xy], 'ko')
        plt.plot([Sigmay, Sigmax], [-ta_xy, ta_xy], color='firebrick', lw=3)
    else:
        plt.plot([Sigmay, Sigmax], [ta_xy, -ta_xy], 'ko')
        plt.plot([Sigmay, Sigmax], [ta_xy, -ta_xy], color='firebrick', lw=3)

    # if (abs(Calculations()[1]) > abs(Calculations()[0]) or abs(Calculations()[1]) < abs(Calculations()[0])) and \
    #         Calculations()[0] * Calculations()[2] <= 0:
    #     plt.plot([Sigmay, Sigmax], [-ta_xy, ta_xy], 'ko')
    #     plt.plot([Sigmay, Sigmax], [-ta_xy, ta_xy], color='firebrick', lw=3)
    # elif (abs(Calculations()[1]) < abs(Calculations()[0]) or abs(Calculations()[1]) > abs(Calculations()[0])) and \
    #         Calculations()[0] * Calculations()[2] >= 0:
    #     plt.plot([Sigmay, Sigmax], [ta_xy, -ta_xy], 'ko')
    #     plt.plot([Sigmay, Sigmax], [ta_xy, -ta_xy], color='firebrick', lw=3)
    plt.plot([S22, S11], [-S12, S12], 'ko')
    plt.plot([S22, S11], [-S12, S12], color='forestgreen', lw=3)
    # plt.plot(center[0], center[1], 'o', mfc='w')
    # plt.cla()
    plt.text(S22 + 0.1 * radius, S12, 'A')
    plt.text(S11 + 0.1 * radius, -S12, 'B')
    plt.text(Sigmay + 0.1 * radius, ta_xy, "A'")
    plt.text(Sigmax + 0.1 * radius, -ta_xy, "B'")
    # plt.cla()
    plt.xlabel(r"$\sigma$", size=18)
    plt.ylabel(r"$\tau$", size=18)
    plt.show()

    return None


def ploot():
    S = np.array([[Sigma_x, Ta_xy], [Ta_xy, Sigma_y]])
    mohr(S)


# Clear Button
def cls():
    Lis.delete(0, END)
    # plt.cla()


# State of stress
def getCustomMarker():
    verts = [
        (-5, -5),
        (-5, 5),
        (5, 5),
        (5, -5),
        (-5, -5)
    ]

    verts = verts

    codes = [matplotlib.path.Path.MOVETO,
             matplotlib.path.Path.LINETO,
             matplotlib.path.Path.LINETO,
             matplotlib.path.Path.LINETO,
             matplotlib.path.Path.CLOSEPOLY]

    path = matplotlib.path.Path(verts, codes)

    return path


# State of stress Button
def stf():
    plt.clf()
    xx = teta
    plt.subplot(1, 2, 1).scatter([0, 0], [0, 0], marker=getCustomMarker(), s=5000)
    marker = getCustomMarker()
    marker = marker.transformed(matplotlib.transforms.Affine2D().rotate_deg(xx))

    if cos(xx * pi / 180) != 0:
        scl = cos(45 * pi / 180)
    else:
        scl = 1

    plt.subplot(1, 2, 2).scatter([0, 0], [0, 0], marker=marker, s=5000 / scl)
    plt.show()
    return None


# GUI by Tkinter
# Window settings
W = Tk()
W.title("Mohr's circle transformation module")
W.geometry('600x500')

# Scrollbar
Scr = Scrollbar(W)
Scr.pack(side=RIGHT, fill=BOTH)
frame1 = Frame(W)
frame1.pack(expand=True, fill=BOTH)
# Scr.config(command=frame1.yview)

# Menu 
menu = Menu(W)
M1 = Menu(menu, tearoff=0)
M1.add_command(label='New File')
M1.add_command(label='Open File...')
M1.add_command(label='Save')
M1.add_command(label='Save As...')
M1.add_command(label='Close', command=W.quit)
M2 = Menu(menu, tearoff=0)
M2.add_command(label='Undo')
M2.add_command(label='Redo')
M2.add_command(label='Cut')
M2.add_command(label='Copy')
M2.add_command(label='Pase')
M3 = Menu(menu, tearoff=0)
M3.add_command(label='Slove')
M3.add_command(label='Solution...')
M4 = Menu(menu, tearoff=0)
menu.add_cascade(label='File', menu=M1)
menu.add_cascade(label='Edit', menu=M2)
menu.add_cascade(label='Solver', menu=M3)
menu.add_cascade(label='Help', menu=M4)
W.config(menu=menu)

# Labe Frame - entry
frame2 = Frame(frame1)

xd = LabelFrame(frame2, text='x direction')
Label(xd, text='Normal Stress').pack()
Sigma_x1 = Entry(xd)
Sigma_x1.pack()
Radio1 = [("Positive", "Tension (+)"), ("Negative", "Compression (-)")]
c1 = StringVar()
c1.set("Positive")
# for a1,b1 in Radio1:
#    Radiobutton(xd,value=a1,text=b1,variable=c1,).pack()

yd = LabelFrame(frame2, text='y direction')
Label(yd, text='Normal Stress').pack()
Sigma_y1 = Entry(yd)
Sigma_y1.pack()
Radio2 = [("Positive", "Tension (+)"), ("Negative", "Compression (-)")]
c2 = StringVar()
c2.set("Positive")
# for a2,b2 in Radio2:
#    Radiobutton(yd,value=a2,text=b2,variable=c2).pack()

xyd = LabelFrame(frame2, text='xy direction')
Label(xyd, text='Shear Stress').pack()
En3 = Entry(xyd)
En3.pack()
Radio3 = [("Negative", "CW on x face (-)"), ("Positive", "CCW on x face (+)")]
c3 = StringVar()
c3.set("Negative")
# for a3,b3 in Radio3:
#    Radiobutton(xyd,value=a3,text=b3,variable=c3).pack()

Tetaa = LabelFrame(frame2, text='Angel')
Label(Tetaa, text='Angel from X axis').pack()
teta2 = Entry(Tetaa)
teta2.pack()
Radio4 = [("Positive", "Tension (+)"), ("Negative", "Compression (-)")]
c4 = StringVar()
c4.set("Positive")
# for a4,b4 in Radio1:
#    Radiobutton(Tetaa,value=a4,text=b4,variable=c4,).pack()

Lis = Listbox(frame2, width=20, height=5)

# Button
but1 = Button(frame2, text='Compute', command=Calculations)
but2 = Button(frame2, text='Mohr Circle', command=ploot)
but3 = Button(frame2, text='Clear', command=cls)
but4 = Button(frame2, text='State of stress', command=stf)

# Combo Box
val = ['MPa', 'kPa', 'kg/cm^2', 'N/mm^2', 'N/cm^2']
combo = ttk.Combobox(frame2, values=val)
combo.set('Select Unit')

# Check Button
# AbsMax = IntVar()
# ch1 = Checkbutton(frame2,text='Show Absolute Maximum Shear Stress',variable=AbsMax)

# plot
frame3 = Frame(frame2)

# Pack-grid
frame2.grid(row=0, column=0)
frame3.grid(row=2, column=1)
xd.grid(row=0, column=0, pady=10)
yd.grid(row=1, column=0, pady=10)
xyd.grid(row=2, column=0, pady=10)
Tetaa.grid(row=3, column=0, pady=10)

but1.grid(row=0, column=1, pady=10, ipadx=30)
but2.grid(row=1, column=1, pady=10, ipadx=40)
but3.grid(row=3, column=1, pady=10, ipadx=30)
but4.grid(row=2, column=1, pady=10, ipadx=30)

# combo.grid(row=1,column=4,pady=0,padx=70)

# ch1.grid(row=2,column=0,ipadx=20,ipady=20)

# Lis.grid
Lis.grid(row=4, column=0, padx=100, pady=10, ipadx=20, ipady=20)

# Run Tkinter
W.mainloop()

fig = plt.figure()
