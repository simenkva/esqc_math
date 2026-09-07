import matplotlib.pyplot as plt
from matplotlib.transforms import offset_copy
from cycler import cycler
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

theme_colors = [
    "#3EAF3E",  # Apple
    "#E0479E",  # Cerise
    "#7AE17A",  # Pastel Green
    "#BCB6FF",  # Melrose
    "#B8E1FF",  # French Pass
    "#E6FBFB",  # White Ice
    "#2C2029",  # Thunder
]

# set up a linear segmented colormap that interpolates between the theme colors 0, 2, 1, 4, 5.
physchem_cmap1 = LinearSegmentedColormap.from_list(
    "physchem_cmap1",
    [theme_colors[0], theme_colors[2], theme_colors[1], theme_colors[4], theme_colors[5]],
    N=256,
)

book1 = cycler(color=theme_colors)

plt.rcParams["axes.prop_cycle"] = book1

# Increase font size
plt.rcParams["font.size"] = 12

# Set STIX TWO
plt.rcParams.update(
    {
        "font.family": "STIX Two Text",  # axis labels, titles, tick labels, etc.
        "mathtext.fontset": "stix",  # math in $...$ uses STIX math glyphs (close match)
        "axes.unicode_minus": False,
    }
)

# define a colormap interpolating between
# C0, C6, and C1:

physchem_cmap1 = LinearSegmentedColormap.from_list(
    "physchem_cmap1", [theme_colors[0], theme_colors[6], theme_colors[1]], N=256
)


# Set default figure size
plt.rcParams["figure.figsize"] = (4, 4)


def make_transparent_background(fig):
    # for all axes in the figure, set the background to transparent

    fig.patch.set_alpha(0)

    for ax in fig.get_axes():
        ax.set_facecolor("none")


def new_plot(figsize=(4, 4)):
    """ Create an empty axis cross. """
    fig, ax = plt.subplots(figsize=figsize)
    # move bottom and left spines to x=0 and y=0
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')

    # hide the top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # show ticks only on the bottom and left spines
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # optional: add arrows at the tips of the axes
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

    ax.set_xlim(-4.5,4.5)
    ax.set_ylim(-4.5,4.5)
    ax.set_xticks(range(-4, 5))
    ax.set_yticks(range(-4, 5))

    ax.set_axisbelow(True)
    ax.grid(alpha=0.3)
    
    # add labels "1" and "2" next to the arrow tips, offset a few points for spacing
    x_label_transform = offset_copy(ax.get_yaxis_transform(), fig=fig, x=4, y=4, units='points')
    y_label_transform = offset_copy(ax.get_xaxis_transform(), fig=fig, x=4, y=4, units='points')
    ax.text(1, 0, "1", fontsize=12, ha='left', va='bottom', transform=x_label_transform)
    ax.text(0, 1, "2", fontsize=12, ha='left', va='bottom', transform=y_label_transform)
    
    return fig, ax


def draw_point(ax, point, color='C1'):
    """ Draw a point at the given coordinates. """
    ax.scatter(point[0], point[1], color=color)
    return ax


def draw_vector(ax, vector, origin=np.array([0, 0]), color='C0'):
    """ Draw a vector from the origin to the given point. """
    ax.quiver(origin[0], origin[1], vector[0], vector[1], angles='xy', scale_units='xy', scale=1, color=color)
    return ax


def retick(ax, points):
    """ Adjust the x and y ticks based on the given points. """
    x_min, x_max = points[:, 0].min() - 1, points[:, 0].max() + 1
    y_min, y_max = points[:, 1].min() - 1, points[:, 1].max() + 1
    xticks = range(int(np.floor(x_min)), int(np.ceil(x_max)) + 1)
    yticks = range(int(np.floor(y_min)), int(np.ceil(y_max)) + 1)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    return ax
