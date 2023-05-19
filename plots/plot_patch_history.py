#! /usr/bin/python3

# numpy
import numpy as np
# datetime
import datetime as dt
# matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import FixedLocator, FixedFormatter
# sys
import sys

# utils
from utils import mavg, correct_data

rcParams['hatch.linewidth'] = 8.0

# Always show Ny years
Ny = 3 if len(sys.argv) < 5 else int(sys.argv[4])
# -->
N = Ny*365
# -->
N5 = N/4

device    = sys.argv[1]
data_file = sys.argv[2]
release   = sys.argv[3]

print(device)

# Load the data
data = np.loadtxt(f"../data/{device}/{data_file}", dtype=str)
# -->
data = correct_data(data)

# Specify the release dates of the different Android versions
adup = {
     8:"2017-08-21",
     9:"2018-08-06",
    10:"2019-09-03",
    11:"2020-09-08",
    12:"2021-10-04",
    13:"2022-08-15"
}

# Enable LaTeX
plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=14)
plt.rcParams['text.latex.preamble']=r"\usepackage{amsmath}\usepackage{mathpazo}\usepackage{mathabx}"

# Create the plot
fig = plt.figure(figsize=(0.4*12.0, 0.4*11.0), dpi=150, edgecolor="white")
ax = fig.add_subplot(1,1,1)
ax.tick_params(axis='both', which='both', labelsize=11, direction="in", width=0.5)
ax.xaxis.set_ticks_position('both')
ax.yaxis.set_ticks_position('both')
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(0.5)

# Define the tick positions
xtMajor = [int(100*i) for i in np.linspace(0, N//100, N//100+1)]
xtMinor = [i + 10*j for i in xtMajor[:-1] for j in range(10)[1:]]
xlMajor = [str(i) if (i//100) % 2 == 0 else "" for i in xtMajor]
xMajorLocator = FixedLocator(xtMajor)
xMinorLocator = FixedLocator(xtMinor)
xMajorFormatter = FixedFormatter(xlMajor)

ytMajor = [int(10*i) for i in np.linspace(0, 15, 16)]
ytMinor = [i + j for i in ytMajor[:-1] for j in range(10)[1:]]
ylMajor = [str(i) if (i//10) % 3 == 0 else "" for i in ytMajor]
yMajorLocator = FixedLocator(ytMajor)
yMinorLocator = FixedLocator(ytMinor)
yMajorFormatter = FixedFormatter(ylMajor)


initial_date = dt.datetime.strptime(data[0,0], "%Y-%m-%d").date()
release_date = dt.datetime.strptime(release  , "%Y-%m-%d").date()
# -->
offset = (initial_date - release_date).days

# g(reen), o(range), r(red), p(urple)
g, o, r, p = 0, 0, 0, 0

# Find the first relevant Android version
latest_android_version = 0
for key in sorted(adup.keys()):
    android_date = dt.datetime.strptime(adup[key], "%Y-%m-%d").date()
    
    if release_date < android_date:
        latest_android_version = key -1
        break

x_array, y_array = [], []
# Loop over the data
for i, d in enumerate(data):
    if i > N:
        break

    last_aup_date = dt.datetime.strptime(adup[latest_android_version]  , "%Y-%m-%d").date()
    next_aup_date = dt.datetime.strptime(adup[latest_android_version+1], "%Y-%m-%d").date() if latest_android_version+1 in adup.keys() else None

    # Extract some data
    current_date           = dt.datetime.strptime(d[0], "%Y-%m-%d").date()
    current_patch_date     = dt.datetime.strptime(d[1], "%Y-%m-%d").date() # curent patch
    current_kernel_version = d[2]
    current_os_version     = int(d[3])

    # Increment the current android version if necessry
    if next_aup_date is not None:
        if current_date > next_aup_date:
            latest_android_version += 1
    
    # -->
    marker_size = 5 if current_os_version == latest_android_version else 3

    x = (current_date - initial_date).days + offset
    y = (current_date - current_patch_date).days

    x_array.append(x)
    y_array.append(y)

    if y <= 30:
        color = 'mediumseagreen'
        g += 1
    elif y <= 60:
        color = 'darkorange'
        o += 1
    elif y <= 90:
        color = 'crimson'
        r += 1
    else:
        color = 'darkorchid'
        p += 1

    plt.plot(x, y, "o", color=color, markersize=marker_size, zorder=-1)

x_array = np.array(x_array)
y_array = np.array(y_array)

margin = 92
window = 2*margin + 1 # roughly 6 month

xmv_array, ymv_array = [], []

i = 0
while True:
    start, end = i, i + window

    if end > len(x_array):
        break

    xmv_array.append(i + margin + offset)
    ymv_array.append(np.mean(y_array[start:end]))

    i += 1

#plt.plot(xmv_array, ymv_array, '--', color='0.7')


xmv_array = mavg(xmv_array, n=margin)
ymv_array = mavg(ymv_array, n=margin)
# -->
plt.plot(xmv_array, ymv_array, color='black')

#np.savetxt(f'../data/{device}/mean_patch', np.column_stack([xmv_array, ymv_array]))

x0 = margin + 1

# Plot the color indicator lines
plt.plot([-1, N], [0]*2, color='black', linestyle='-', linewidth=0.5)

plt.plot([-1, N], [30]*2, color='mediumseagreen', linestyle='--', linewidth=1, zorder=0)
plt.plot([-1, N], [60]*2, color='darkorange', linestyle='--', linewidth=1, zorder=0)
plt.plot([-1, N], [90]*2, color='crimson', linestyle='--', linewidth=1, zorder=0)
plt.plot([-1, N], [120]*2, color='darkorchid', linestyle='--', linewidth=1, zorder=0)

# Plot the year indicator lines
for i in range(Ny):
    plt.plot([i*365]*2, [0, 150], color='0.6', linestyle='-.', linewidth=1, zorder=0)

# Plot the today indicator
#plt.plot([(dt.date.today()-release_date).days]*2, [0, 150], color='0', linestyle='-', linewidth=2.5, zorder=2)

# Plot some invisible lines for the legend label
plt.plot(-100, 500, color='mediumseagreen', label=r'$t \leq 30\,\mathrm{days}$')
plt.plot(-100, 500, color='darkorange', label=r'$30 < t \leq 60\,\mathrm{days}$')
plt.plot(-100, 500, color='crimson', label=r'$60 < t \leq 90\,\mathrm{days}$')
plt.plot(-100, 500, color='darkorchid', label=r'$t > 90\,\mathrm{days}$')

# Hatch the dataless region since the release date
plt.fill_between([0, offset], 0, 150, facecolor="white", hatch="\\", edgecolor="0.9")

# Plot the legend
plt.legend(fontsize=9, loc='upper center', edgecolor='black', framealpha=0.9)

l = len(data)
# Plot the percantage for the different colored regions
gi, oi, ri, pi = 100*g/l, 100*o/l, 100*r/l, 100*p/l
plt.text(0.2*N5, -14, f"{gi:05.2f}\%", color='mediumseagreen')
plt.text(1.2*N5, -14, f"{oi:05.2f}\%", color='darkorange')
plt.text(2.2*N5, -14, f"{ri:05.2f}\%", color='crimson')
plt.text(3.2*N5, -14, f"{pi:05.2f}\%", color='darkorchid')

# Set the x- and y-axis
plt.xlabel('Time since release [days]', fontsize=12)
ax.xaxis.set_major_locator(xMajorLocator)
ax.xaxis.set_major_formatter(xMajorFormatter)
plt.xlim(0, N)

plt.ylabel('Age of the security patch [days]', fontsize=12)
ax.yaxis.set_major_locator(yMajorLocator)
ax.yaxis.set_major_formatter(yMajorFormatter)
plt.ylim(-20, 150)

# Set th title
plt.title(fr"\textbf{{{device}}} $|$ {release_date.strftime('%d/%m/%Y')} $|$ {Ny} years", fontsize=12)

plt.tight_layout()
plt.savefig(device + '.pdf')
#plt.show()
