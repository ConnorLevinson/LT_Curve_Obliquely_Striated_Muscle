import numpy as np
import matplotlib.pyplot as plt

def sarc_sim(angle, angle_changing, A, I, BZ): # assign filament dimensions in microns
    #A = 1.6  # length of the thick filament
    #I = 2.05  # length of two thin filaments and a z-line or body
    #BZ = 0.20  # length of the bare-zone
    mh_spacing = 0.02  # spacing between myosin heads
    n = 30  # number of thin filaments
    h_initial = 6  # initial height of the sarcomere
    area = A * h_initial  # area is the initial length of the sarcomere (A) times the initial height of the sarcomere (h)
    p = h_initial / np.sin(np.deg2rad(angle))  # other side of the parallelogram
    
    LF_length = round((A + 4 * I) / mh_spacing) + 1 # Calculate the expected length of LF
    
    LF = np.zeros((LF_length, 2))# Create LF array to store results
    
    for l, L in enumerate(np.arange(A, A + 4 * I, mh_spacing)):
        h = area / L  # calculate the height of the sarcomere
        d = h / n  # calculate the distance between the filaments based on area and length.

        # if the angle is changing, calculate the angle of striation
        if angle_changing:
            theta = np.arcsin(h / p)
        else:
            theta = np.deg2rad(angle)
        x = d / np.tan(theta)  # calculate the lateral distance between the start of thin filaments

        # create arrays to hold the locations of the filaments
        TFL = np.zeros((n - 1, round((A - BZ) / 2 / mh_spacing) + 1, 2))  # create an array to hold the locations of the left myosin heads

        for i in range(1, n): # fill in array for myosin heads
            k = 0
            for j in np.arange((L - A) / 2 + x * i, (L - BZ) / 2 + x * i, mh_spacing):
                TFL[i - 1, k, 0] = j
                TFL[i - 1, k, 1] = (i - 1) * d
                k += 1

        TFR = np.zeros((n - 1, round((A - BZ) / 2 / mh_spacing) + 1, 2))  # create an array to hold the locations of the right myosin heads

        # fill in array for myosin heads
        for i in range(1, n):
            k = 0
            for j in np.arange((L + BZ) / 2 + x * i, (L + A) / 2 + x * i, mh_spacing):
                TFR[i - 1, k, 0] = j
                TFR[i - 1, k, 1] = (i - 1) * d
                k += 1

        tfl = np.zeros((3, n))  # create an array to hold the locations of the left thin filaments

        # fill in array for the thin filaments
        for i in range(n):
            tfl[0, i] = (i - 1) * x
            tfl[1, i] = I / 2 + (i - 1) * x
            tfl[2, i] = (i - 1) * d

        tfr = np.zeros((3, n))  # create an array to hold the locations of the right thin filaments

        # fill in array for the thin filaments
        for i in range(n):
            tfr[0, i] = L - I / 2 + i * x
            tfr[1, i] = L + i * x
            tfr[2, i] = (i - 1) * d

        # compare the arrays to calculate the force
        Fsumn = np.zeros(n)  # create an empty array to count the force produced by each filament set

        for i in range(n - 1):  # for each filament
            for k in range(round((A - BZ) / 2 / mh_spacing) + 1):  # along all possible positions
                if (tfl[0, i] <= TFL[i, k, 0] <= tfl[1, i]):  # if the left myosin head overlaps with the left thin filament
                    if (tfr[0, i] <= TFL[i, k, 0] <= tfr[1, i]):  # if the left myosin head overlaps with the right thin filament
                        Fsumn[i] = Fsumn[i]  # keep the force the same because the thin filaments are interfering with each other
                    else:
                        Fsumn[i] += 1  # if the thin filaments do not overlap and there is a left myosin head, add one to the force.
                if (tfl[0, i + 1] <= TFL[i, k, 0] <= tfl[1, i + 1]):  # check the thin filament on the other side of the left myosin head
                    if (tfr[0, i + 1] <= TFL[i, k, 0] <= tfr[1, i + 1]):
                        Fsumn[i] = Fsumn[i]
                    else:
                        Fsumn[i] += 1
                if (tfr[0, i] <= TFR[i, k, 0] <= tfr[1, i]):  # do the same for the right myosin heads
                    if (tfl[0, i] <= TFR[i, k, 0] <= tfl[1, i]):
                        Fsumn[i] = Fsumn[i]
                    else:
                        Fsumn[i] += 1
                if (tfr[0, i + 1] <= TFR[i, k, 0] <= tfr[1, i + 1]):
                    if (tfl[0, i + 1] <= TFR[i, k, 0] <= tfl[1, i + 1]):
                        Fsumn[i] = Fsumn[i]
                    else:
                        Fsumn[i] += 1

        # store the length and total force in the LF array
        LF[l, 0] = L
        LF[l, 1] = np.sum(Fsumn)

    LTcurve = LF[:l+1]  # Trim LF to the actual number of iterations
    return LTcurve

""" angle = 45
angle_changing = False
LTcurve = sarc_sim(angle, angle_changing)

L_values = LTcurve[:, 0]
L_Average = sum(L_values)/len(L_values)
Tension_values = LTcurve[:, 1]
Tension_Average = sum(Tension_values)/len(Tension_values)

# plt.plot(L_values, Tension_values)
# plt.xlabel('Sarcomere Length')
# plt.ylabel('Tension')
# plt.title('Tension vs. Sarcomere Length')
# plt.grid(True)
# plt.show()

# plt.plot(L_values/L_Average, Tension_values/Tension_Average)
# plt.xlabel('Sarcomere Length Averages')
# plt.ylabel('Tension')
# plt.title('Tension vs. Sarcomere Length')
# plt.grid(True)
# plt.show()

fig, ax = plt.subplots(1, 2, figsize=(12, 6))  # figsize is width x height in inches; adjust as necessary

# First subplot
ax[0].plot(L_values, Tension_values)
ax[0].set_xlabel('Sarcomere Length')*
ax[0].set_ylabel('Tension')
ax[0].set_title('Tension vs. Sarcomere Length')
ax[0].grid(True)

# Second subplot
ax[1].plot(L_values / L_Average, Tension_values / Tension_Average)
ax[1].set_xlabel('Sarcomere Length Averages')
ax[1].set_ylabel('Tension')
ax[1].set_title('Normalized Tension vs. Sarcomere Length')
ax[1].grid(True)

# Display the plots
plt.tight_layout()  # Adjust subplots to fit into the figure area.
plt.show()
 """
