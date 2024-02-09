import numpy as np

year, month, day, temp, corrected = np.loadtxt("Uppsala_temperaturer_2008_2017.txt",
                                               usecols=(0, 1, 2, 3, 4), unpack=True)
temp_ins = 21

conv_rate = 13.34  # 2 000 000 J/h = 13.34 kWh/dygn


def temp_rad(temp_out):
    if temp_out < 0:
        return temp_ins * (1 + 0.043 * temp_ins - 0.035 * temp_out)
    elif 0 <= temp_out < temp_ins:
        return temp_ins * (1 + 0.043 * (temp_ins - temp_out))
    elif temp_ins <= temp_out:
        return 0


# 1. i)
heat_leakage = [(temp_ins - i) * conv_rate for i in corrected]
for index, value in enumerate(heat_leakage):
    print(f"{int(year[index])}/{int(month[index])}/{int(day[index])}: {value:.1f} kWh/dag")

# 1. ii)
cop = [1 / (1 - 10/temp_rad(i)) if temp_rad(i) != 0 else 0 for i in corrected]
for index, value in enumerate(cop):
    print(f"{int(year[index])}/{int(month[index])}/{int(day[index])}: {value:.2f} cop")

# 1 iii)
wnet = [heat_leakage[i] / cop[i] for i, val in enumerate(corrected)]
for index, value in enumerate(wnet):
    print(f"{int(year[index])}/{int(month[index])}/{int(day[index])}: {value:.1f} kWh/dag")

