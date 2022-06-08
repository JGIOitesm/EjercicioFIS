import numpy as np
import skfuzzy as sk
from matplotlib import pyplot as plt

vel_auto = np.arange (10, 120.1, 0.1)
dist_auto = np.arange (15, 100.1, 0.1)
vel_peaton = np.arange (1, 20.1, 0.1)

v_auto_mfs = [sk.trapmf(vel_auto, [70, 100, 120, 120]), # Alta
                sk.gbellmf(vel_auto, 28,8,60),          # Media
                sk.trapmf(vel_auto, [10, 10, 30, 45])]  # Baja

d_auto_mfs = [sk.gaussmf(dist_auto, 100, 10),   # Alta
                sk.gaussmf(dist_auto, 60, 20),  # Media
                sk.gaussmf(dist_auto, 15, 10)]  # Baja

v_peaton_mfs = [sk.gbellmf(vel_peaton, 2,2,20), # Alta
                sk.gbellmf(vel_peaton, 2,2,15),  # Media-Alta
                sk.gbellmf(vel_peaton, 2,2,10),  # Media
                sk.gbellmf(vel_peaton, 2,2,5),   # Media-Baja
                sk.gbellmf(vel_peaton, 2,2,1)]   # Baja

def vel_peaton_calc(vel_auto_input, dist_auto_input, show = False):
    vel_indx = round((vel_auto_input - 10)/0.1)
    dist_indx = round((dist_auto_input - 15)/0.1)
    
    # Reglas de inferencia
    R = [[min(vel_auto_mf[vel_indx], dist_auto_mf[dist_indx]) for vel_auto_mf in v_auto_mfs] for dist_auto_mf in d_auto_mfs]

    vel_cut_peaton = [max(R[2][1], R[2][0]),# Alta => dist_low y vel_med, dist_low y vel_high
                    max(R[2][2],R[1][0]),   # Media-alta => dist_low y vel_low, dist_med y vel_high
                    R[1][1],                # Media => dist_med y vel_med
                    max(R[1][2],R[0][0]),   # Media-baja => dist_med y vel_low, dist_high y vel_high
                    max(R[0][2], R[0][1])]  # Baja => dist_high y vel_low, dist_high y vel_med

    velocities_output = np.zeros(vel_peaton.shape)
    xy_sum = 0
    area = 0
    for i,vel in enumerate(vel_peaton):
        velocities_output[i] = max([min(vel_cut_peaton[mf_index], v_peaton_mfs[mf_index][i]) for mf_index in range(len(vel_cut_peaton))])
        xy_sum += vel*velocities_output[i]
        area += velocities_output[i]

    center = xy_sum/area # Velocidad a la que debe cruzar
    return (center, velocities_output) if show else center

vel_input = round(float(input("Velocidad del carro: ")),1)
dist_input = round(float(input("Distancia del carro: ")),1)
center, vel_peaton_output = vel_peaton_calc(vel_input, dist_input, True)
print("Velocidad del peatón: ", center)

plt.figure(figsize = (20, 5))
plt.subplot(1,4,1)
for vel_mf in v_auto_mfs:
    plt.plot(vel_auto, vel_mf)
plt.legend(["alta", "media", "baja"], loc='lower left')
plt.ylabel(r'$\mu$')
plt.xlabel("km/h")
plt.title("Entrada 1: Velocidad del auto")

plt.subplot(1,4,2)
for dist_mf in d_auto_mfs:
    plt.plot(dist_auto, dist_mf)
plt.legend(["lejana", "mediana", "cercana"], loc='lower left')
plt.ylabel(r"$\mu$")
plt.xlabel('m')
plt.title('Entrada 2: Distancia del auto')

plt.subplot(1,4,3)
for v_peaton_mf in v_peaton_mfs:
    plt.plot(vel_peaton, v_peaton_mf)
plt.legend(["alta", "media-alta", "media", "media-baja", "baja"], loc='lower left')
plt.ylabel(r'$\mu$')
plt.xlabel('km/h')
plt.title('Salida: Velocidad del peaton')

plt.subplot(1,4,4)
plt.plot(vel_peaton, vel_peaton_output)
plt.axvline(x = center)
plt.ylabel(r'$\mu$')
plt.xlabel('km/h')
plt.ylim([0, 1.05])
plt.title('Control')
plt.show()
