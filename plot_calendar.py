import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from matplotlib.font_manager import FontProperties

city_name = "Vizag"
city_coordinates = "17.7219°N, 83.3057°E"

#https://www.timeanddate.com/eclipse/2025
total_lunar_eclipse_day_index = 250 #7 sep in 365 days

# https://www.rmg.co.uk/stories/topics/meteor-shower-guide
# peak day index, start of shower, end of shower tuples of major ones - quadrantids, perseids, and geminids
meteor_showers = [(3, 1, 12), (224, 198, 236), (348, 338, 354)]

with open("vizag_data.json", "r") as f:
    data = json.load(f)
    
sunrise_times = data["sunrise"]
sunset_times = data["sunset"]
days_in_month = data["days_in_month"]
moon_phases = data["moon_phases"]
noon_times = data["noon"]
civil_twilight = data["civil"]
nautical_twilight = data["nautical"]
astronomical_twilight = data["astro"]
civil_twilight_dawn, civil_twilight_dusk = zip(*civil_twilight)
nautical_twilight_dawn, nautical_twilight_dusk = zip(*nautical_twilight)
astronomical_twilight_dawn, astronomical_twilight_dusk = zip(*astronomical_twilight)

fig, ax = plt.subplots(figsize=(24, 24), subplot_kw=dict(polar=True), dpi=300)
fig.patch.set_facecolor('#faf0e6')  
ax.set_theta_direction(-1)
ax.set_theta_offset(np.pi / 2)

num_days = len(sunrise_times)
sunrise_r = np.array(sunrise_times + [sunrise_times[0]]) / 24
sunset_r = np.array(sunset_times + [sunset_times[0]]) / 24
noon_r = np.array(noon_times + [noon_times[0]]) / 24
dawn_r = np.array(list(civil_twilight_dawn) + [civil_twilight_dawn[0]]) / 24
dusk_r = np.array(list(civil_twilight_dusk) + [civil_twilight_dusk[0]]) / 24
dawn_nautical_r = np.array(list(nautical_twilight_dawn) + [nautical_twilight_dawn[0]]) / 24
dusk_nautical_r = np.array(list(nautical_twilight_dusk) + [nautical_twilight_dusk[0]]) / 24
dawn_astro_r = np.array(list(astronomical_twilight_dawn) + [astronomical_twilight_dawn[0]]) / 24
dusk_astro_r = np.array(list(astronomical_twilight_dusk) + [astronomical_twilight_dusk[0]]) / 24

theta = np.linspace(0, 2 * np.pi, len(sunrise_r), endpoint=True)

# Night
ax.fill_between(theta, sunset_r, 1, color='#011F26', zorder=2)
ax.fill_between(theta, 0, sunrise_r, color='#011F26', zorder=2)

# Day
ax.fill_between(theta, sunrise_r, sunset_r, color='#fbba43', zorder=2)

ax.fill_between(theta, dawn_r, sunrise_r, color='#1C5C7C', zorder=2, alpha=0.85)
ax.fill_between(theta, sunset_r, dusk_r, color='#1C5C7C', zorder=2, alpha=0.85)
ax.fill_between(theta, dawn_nautical_r, dawn_r, color='#0A3F4D', zorder=2, alpha=0.7)
ax.fill_between(theta, dusk_r, dusk_nautical_r, color='#0A3F4D', zorder=2,  alpha=0.7)
ax.fill_between(theta, dawn_astro_r, dawn_nautical_r, color='#092A38', zorder=2,  alpha=0.8)
ax.fill_between(theta, dusk_nautical_r, dusk_astro_r, color='#092A38', zorder=2,  alpha=0.8)
ax.fill_between(theta, noon_r - 0.002, noon_r + 0.002, color='#FFFACD', alpha=0.05, zorder=3)

months_labels = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
cumulative_days = np.cumsum(days_in_month)
month_ticks = [(cumulative_days[i - 1] if i > 0 else 0) + days_in_month[i] / 2 for i in range(12)]
month_ticks_rad = [tick / num_days * 2 * np.pi for tick in month_ticks]
ax.set_xticks(month_ticks_rad)
ax.set_xticklabels([])
label_height = 1.1
for angle, label in zip(month_ticks_rad, months_labels):
    ax.text(angle, label_height, label, horizontalalignment='center', fontsize=22, color="#2F4F4F", fontweight='bold')

for i in range(12):
    angle = cumulative_days[i] / num_days * 2 * np.pi if i < 11 else 2 * np.pi
    ax.plot([angle, angle], [0, 1.2], color='#02735E', linewidth=0.5, zorder=3)

closest_full_moon_days = []
i = 0
while i < len(moon_phases):
    if 13.5 <= moon_phases[i] <= 14.5:
        closest_day = i
        min_diff = abs(moon_phases[i] - 14)
        j = i + 1
        while j < len(moon_phases) and 13.5 <= moon_phases[j] <= 14.5:
            diff = abs(moon_phases[j] - 14)
            if diff < min_diff:
                min_diff = diff
                closest_day = j
            j += 1
        closest_full_moon_days.append(closest_day+1)
        i = j
    else:
        i += 1

marker_radius = 0.97
marker_size = 100
for day_index in closest_full_moon_days:
    angle = day_index / num_days * 2 * np.pi
    ax.scatter(angle, marker_radius, s=marker_size, color='#A1A2A6', marker='o', zorder=4)

angle = total_lunar_eclipse_day_index / num_days * 2 * np.pi
# halo_radius = marker_radius
# halo = Circle((angle, halo_radius), radius=0.009, color='white', alpha=0.7, zorder=4)
# ax.add_patch(halo)
ax.scatter(angle, marker_radius, s=marker_size, color='#7E2A2A', marker='o', zorder=5)

first_sunday = 5
sundays = [(first_sunday + i * 7) for i in range(52)]

for i, day_index in enumerate(sundays):
    angle = day_index / num_days * 2 * np.pi
    month_index = 0
    for i in range(len(days_in_month)):
        if day_index > sum(days_in_month[:i+1]):
            month_index += 1
        else:
            break
    month_day = day_index - sum(days_in_month[:month_index])
    label_radius = 1.02
    rotation = -np.degrees(angle)
    rotation = (rotation + 180) % 360 - 180
    angle_deg = np.degrees(angle)
    angle_deg = (angle_deg + 360) % 360
    def scaled(val):
        return (val ** 3 * (1 - val)*0.7 + val) * 0.015 #handcoded 
    if 0 <= angle_deg <= 90:
        diff = (angle_deg / 90)
        label_radius -= scaled(diff)
    elif 90 < angle_deg <= 180: 
        diff = 1 - (angle_deg - 90) / 90
        label_radius += scaled(diff)
    elif 180 < angle_deg <= 270:
        diff = (angle_deg - 180) / 90
        label_radius -= scaled(diff)
    elif 270 < angle_deg < 360:
        diff = 1-(angle_deg - 270) / 90
        label_radius += scaled(diff)

    ha = 'center'
    va = 'center'
    if -90 < rotation < 90:
        ha = 'left'
    else:
        ha = 'right'
    ax.text(angle, label_radius, str(month_day), ha=ha, va=va, fontsize=16, color='#696969', rotation=rotation, zorder=5, fontweight='bold') 

hour_labels_to_display = ['1AM', '4AM', '7AM', '10AM', '1PM', '4PM', '7PM', '10PM']
hour_ticks_to_display = [x / 24 for x in range(1, 24, 3)]
for i, label in enumerate(hour_labels_to_display):
    angle_rad = 75 * np.pi / 180
    radius = hour_ticks_to_display[i]
    ax.text(angle_rad, radius, label, ha='left', va='center', fontsize=9, color='#e7fdeb', zorder=10)
    
for tick in hour_ticks_to_display:
    ax.fill_between(theta, tick-0.0005, tick+0.0005, color='gray', alpha=0.4, zorder=3, linewidth=0)

for shower in meteor_showers:
    peak_day, start_day, end_day = shower
    start_angle = start_day / num_days * 2 * np.pi
    end_angle = end_day / num_days * 2 * np.pi
    peak_angle = peak_day / num_days * 2 * np.pi
    
    if shower == meteor_showers[0]:  # Quadrantids
        num_lines = int((end_day - start_day) / 1.2) 
        scale = 0.03 # Sharper peak
        skew = 1.8  # Faster rise, slower fall
    elif shower == meteor_showers[1]:  # Perseids
        num_lines = int((end_day - start_day) / 2.5)
        scale = 0.12  # Broader peak
        skew = 1.2  # Moderate asymmetry
    else:  # Geminids
        num_lines = int((end_day - start_day) / 2)
        scale = 0.09 # Slightly more defined peak
        skew = 1.3 # Moderate asymmetry
    beta_samples = np.random.beta(2, 2*skew, num_lines)
    random_angles = start_angle + beta_samples * (end_angle - start_angle)
    peak_idx = np.abs(random_angles - peak_angle).argmin()
    random_angles[peak_idx] = peak_angle
    random_angles = np.append(random_angles, [start_angle, end_angle])
    random_radii = np.random.uniform(0.91, 0.928, num_lines + 2)
    radius_inc = np.random.uniform(0.001, 0.008, num_lines + 2)
    for radius, angle, change in zip(random_radii, random_angles, radius_inc):
        ax.plot([angle, angle], [radius, radius + change], color='white', linewidth=0.4, zorder=6, alpha=0.65 + change * 20)    
    
    ax.plot([peak_angle, peak_angle], [0.95, 0.97], color='white', linewidth=0.25, zorder=6, alpha=1)
    ax.plot([peak_angle - 0.002, peak_angle - 0.002], [0.9, 0.94], color='white', linewidth=0.3, zorder=6, alpha=1)
    ax.plot([peak_angle + 0.003, peak_angle + 0.003], [0.92, 0.95], color='white', linewidth=0.25, zorder=6, alpha=0.9)

font_system = FontProperties(fname='Arvo-Bold.ttf' , weight='bold', size=64)
ax.text(0.5, 1.18, city_name, ha='center', va='center', fontproperties=font_system, transform=ax.transAxes)
font_system = FontProperties(fname='Arvo-Regular.ttf', size=20)
ax.text(0.5, 1.14, city_coordinates, ha='center', va='center', fontproperties=font_system, transform=ax.transAxes)
font_system = FontProperties(fname='Arvo-Regular.ttf', size=48)
ax.text(0.5, 1.23, "2025", ha='center', va='center', fontproperties=font_system, transform=ax.transAxes)

ax.set_ylim(0, 1.05)
ax.set_yticklabels([])
plt.subplots_adjust(top=0.9)

plt.savefig(f'{city_name}.png', bbox_inches='tight', pad_inches=1)
plt.savefig(f'{city_name}.pdf', bbox_inches='tight', pad_inches=1)
