import numpy as np

year, month, day, temp, corrected = np.loadtxt("Uppsala_temperaturer_2008_2017.txt",
                                               usecols=(0, 1, 2, 3, 4), unpack=True)
t = 21

conv_rate = 13.34  # 2 000 000 J/h = 13.34 kWh/dygn


def temp_rad(temp_out, temp_ins):
    if temp_out < 0:
        return temp_ins * (1 + 0.043 * temp_ins - 0.035 * temp_out)
    elif 0 <= temp_out < temp_ins:
        return temp_ins * (1 + 0.043 * (temp_ins - temp_out))
    elif temp_ins <= temp_out:
        return 0


def main(temp_ins):
    # 1. i)
    heat_leakage = [(temp_ins - i) * conv_rate if (temp_ins - i) >= 0 else 0 for i in corrected]
    # for index, value in enumerate(heat_leakage):
    # print(f"{int(year[index])}/{int(month[index])}/{int(day[index])}: {value:.1f} kWh/dag")

    # 1. ii)
    cop = [1 / (1 - (10 + 273.3) / (temp_rad(i, temp_ins) + 273.3)) if temp_rad(i, temp_ins) != 0 else 0 for i in
           corrected]
    # for index, value in enumerate(cop):
    # print(f"{int(year[index])}/{int(month[index])}/{int(day[index])}: {value:.2f} cop")

    # 1 iii)
    wnet = [heat_leakage[i] / cop[i] if cop[i] != 0 else 0 for i, val in enumerate(corrected)]
    # for index, value in enumerate(wnet):
    # print(f"{int(year[index])}/{int(month[index])}/{int(day[index])}: {value:.1f} kWh/dag")

    # 2
    years = {}
    for index, value in enumerate(wnet):
        if year[index] not in years.keys():
            years[int(year[index])] = 0
        years[year[index]] += value

    # Kul dict comprehension --- väldigt långsam
    # years = {int(year[index]): sum(wnet[i] for i, _ in enumerate(wnet) if year[i] == year[index]) for index in range(len(year)) if int(year[index]) not in years}

    return heat_leakage, cop, wnet, years


first = main(21)
print(f"Medelvärdet av elförbrukning från värmepumpen är {sum(first[3].values()) / len(first[3]):.1f} kWh/år")
second = main(19)
print(f"Om man minskar temperaturen till 19 grader har man sparat {sum(first[3].values()) - sum(second[3].values()):.1f} kWh under 10 år")
