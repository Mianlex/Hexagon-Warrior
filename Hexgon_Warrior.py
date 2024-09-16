##Hexgon-Warrior
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize, ListedColormap
import matplotlib.patheffects as path_effects 

# Caregories: Define the data for radar chart 
## Your Skills/Abilities ##Could be any amount No need to be 6.
categories = ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5', 'Category 6']
#categories = ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5', 'Category 6','Category 7', 'Category 8', 'Category 9']
## Level/Score of your skills #correlated to the caregories
values = [3, 4, 2, 4, 5, 1]
#values = [3, 4, 2, 3, 5, 1,4,3,2]
## Number of variables/categories
num_vars = len(categories)
## Compute angle of each category (divide the plot into equal parts)
angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
angles += angles[:1]  # Complete the loop
## Add the first value at the end to close the radar chart loop
values += values[:1]
## Set color palette for categories blocks (using Seaborn for better colors)
#palette = sns.color_palette("coolwarm", 10)
palette = sns.color_palette("pastel",10)
markerline_color = "white"
text_color = palette[0]
line_color = palette[0]
fill_color = palette[0]
marker_color = palette[0]


# Level: label of Level in your skills #Refer to the values above
## As a reference: 
level=["Novice","Advanced Beginner","Competent","Proficient","Expert"]
## Color map for each level
levelpalette = sns.color_palette("cubehelix", len(level)*100)
levelpalette.reverse()
## Transparent parameter in color of level blocks #1=solid 0=transparent
alpha=0.9

# Initialize the radar chart
fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True),dpi=200)

# Draw one axe per variable and add labels
ax.set_theta_offset(pi / 2)  # Rotate the plot to start from the top
ax.set_theta_direction(-1)  # Set the direction of the angles

# Remove circular boundary (this caused both the circle and polygon to appear)
ax.spines['polar'].set_visible(False)
# Hide radial and angular grid lines
ax.xaxis.set_visible(False)  # Hides the angular grid lines and labels
ax.yaxis.set_visible(False)  # Hides the radial grid lines and labels
    

# Step 1: Create polygonal gridlines manually #Zorder=0 
## Plot the polar line toward the angle of polygon
## Gradient set for laser color
## Get the seaborn color palette and convert to a ListedColormap
cmap = ListedColormap(levelpalette)
## radius define as lenth of level
r = np.linspace(0, len(level), 100)
## Normalize the data points
norm = Normalize(vmin=r.min(), vmax=r.max())

for i in angles:
    #### Convert the data to segments for the LineCollection in gradient color
    theta = np.full_like(r, i) 
    points = np.array([theta, r]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, cmap=cmap, norm=norm,zorder=0,
                        linestyle="--", linewidth=1, alpha=alpha)
    lc.set_array(r)  # Map colors to the radius values (r)
    ax.add_collection(lc)
    
##plot the polygon boundaries
for i in range(1, len(level)):
    ax.plot(angles, [i]*len(angles), linestyle='--', color=levelpalette[i*100], linewidth=1.5, zorder=0,alpha=alpha)

##Manually create the polygonal outer boundary in solid
ax.plot(angles, [5]*len(angles), color=levelpalette[-1], zorder=0, linewidth=1.5, alpha=alpha)  # Outermost polygon boundary


# Step 2: Plot data with customized line and fill color
ax.plot(angles, values, linewidth=2.5, linestyle='solid', color=line_color, clip_on=True)

# Step 3: Fill the area under the plot with transparency to prevent solid blocks
ax.fill(angles, values, color=fill_color, alpha=0.3)  # Lowered alpha to fix color block issue

# Step 4: Add small circles with transparent fill at each data point
ax.scatter(angles[:-1], values[:-1], color=marker_color, s=50, edgecolor=markerline_color, linewidths=2, zorder=30, clip_on=True)

# Step 5: Add custom text labels for each category
for i, angle in enumerate(angles[:-1]):
    x = angle # Adjust multiplier to move text further/closer
    y = len(level)+0.65
    angle_deg = -1*np.degrees(angle)
    #print(angle_deg)
    if abs(angle_deg) >= 90 and abs(angle_deg) <= 270:
        rotation = angle_deg+180
    else:
        rotation = angle_deg
    ax.text(x, y, categories[i],  
            horizontalalignment='center', verticalalignment='center', 
            size=11, color="black",
            weight = 'bold',
             rotation=rotation)


# Step 6: Title    
title = plt.title('Hexagon-Warrior', size=20,weight='bold', color=text_color, pad=20)
# Apply a stroke (outline) effect to the title
title.set_path_effects([path_effects.Stroke(linewidth=1.5, foreground='black'),  # Black outline
                        path_effects.Normal()])  # Normal text rendering inside

# Remove radial labels (ticks) to prevent interference
ax.set_rticks([])

# Show the chart
plt.ylim(0, len(level)+0.5)
#If you want to save the fig.
#plt.savefig('Example.jpg', bbox_inches='tight')
plt.show()
