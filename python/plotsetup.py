import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib.colors import LinearSegmentedColormap

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
