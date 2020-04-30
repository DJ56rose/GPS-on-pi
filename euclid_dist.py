import csv
import numpy as np
from seaborn import heatmap
from matplotlib import pyplot as plt

filename = "test_drive_GPS_data.txt"
f = open(filename, "r")

# Read in data
lat = []
long = []
for row in csv.reader(f):
    if "Latitude" in row[1]: continue
    lat.append(float(row[1]))
    long.append(float(row[3]))

# Set constants and convert to radians
R = 6371    # radius of earth in km
latitude = np.pi/180 * (np.asarray(lat))
longitude = np.pi/180 * (np.asarray(long))

# Prepare x, y, z points
x = R * np.multiply(np.cos(latitude), np.cos(longitude))
y = R * np.multiply(np.cos(latitude), np.sin(longitude))
z = R * np.sin(np.sin(latitude))

# Calculate Euclidean distance in km
x_diff = np.square(np.diff(x))
y_diff = np.square(np.diff(y))
z_diff = np.square(np.diff(z))
euclid_dist = np.sqrt(x_diff+y_diff+z_diff)
euclid_dist_miles = 0.6214 * euclid_dist

# Get total distance
total_dist = np.sum(euclid_dist)
total_dist_miles = np.sum(euclid_dist_miles)

# Save total distance in km
np.savetxt("total_distance.txt", [total_dist], fmt='%10.3f')

# Calculate average speed in km/h - assume 15s between each data point
delta = 15
av_speed = (euclid_dist*3600) / delta
av_speed_miles = (euclid_dist_miles*3600) / delta
num_points = len(av_speed)

#print("Distance:", total_dist, "km (", total_dist_miles,"miles)")
#print("Average speed:", np.sum(av_speed)/num_points,"km/h (",np.sum(av_speed_miles)/num_points,"mph)")

# Create and save average speed heatmap
sns = heatmap([av_speed_miles])
font = 15
plt.xlabel("Data point", fontsize=font)
plt.title("Average speed (mph)", fontsize=font)
plt.tight_layout()
plt.savefig("speed_heatmap.png")
plt.close()

# Create and save average speed plot
plt.xlabel("Data point")
plt.ylabel("Average speed (km/h)")
plt.title("Average speed")
plt.plot(av_speed)
plt.savefig("speed.png")
