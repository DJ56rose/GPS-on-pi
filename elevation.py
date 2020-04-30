import csv
from seaborn import heatmap
import numpy as np
from matplotlib import pyplot as plt

filename = "test_drive_GPS_data.txt"
f = open(filename, "r")

# Read elevation values
elev = []
for row in csv.reader(f):
    val = row[5]
    if "Elevation" in val: continue
    elev.append(float(row[5]))

# Save max elevation gain?
elevation = np.asarray(elev)
gain = max(elevation) - min(elevation)
np.savetxt("elevation_gain.txt", [gain], fmt='%10.2f')

# Create and save heat map
sns = heatmap([elevation])
font = 15
plt.xlabel("Data point", fontsize=font)
plt.title("Elevation (M)", fontsize=font)
plt.tight_layout()
plt.savefig("elevation_heatmap.png")
plt.close()

# Create and save elevation plot
plt.xlabel("Data point")
plt.ylabel("Elevation (m)")
plt.title("Reported elevation")
plt.plot(elevation)
plt.savefig("elevation.png")
plt.close()

# Derivative
# deriv = [x - elev[i - 1] for i, x in enumerate(elev)][1:]
# deriv = np.asarray(deriv)
# sns2 = heatmap([deriv])
# plt.show()
