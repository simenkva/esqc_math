import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.colors import LightSource


def f(x, y):
    """Evaluate the function, leaving its undefined origin unplotted."""
    radius_squared = x**2 + y**2
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(
            radius_squared > 0,
            x * y**2 / radius_squared ** (3 / 2),
            np.nan,
        )


def make_square_polar_mesh(
    half_width, inner_radius, radial_points, angular_points
):
    """Sample a square radially so every neighborhood has fine angular detail."""
    theta = np.linspace(-np.pi, np.pi, angular_points)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    # The outer radius varies with angle so that its boundary is a square.
    outer_radius = half_width / np.maximum(np.abs(cos_theta), np.abs(sin_theta))
    radial_fraction = np.linspace(0.0, 1.0, radial_points) ** 1.7
    radius = inner_radius + radial_fraction[:, None] * (
        outer_radius[None, :] - inner_radius
    )

    x = radius * cos_theta[None, :]
    y = radius * sin_theta[None, :]
    return x, y


def main():
    half_width = 4.0
    inner_radius = 0.02
    radial_points = 241
    angular_points = 721

    # A polar mesh retains hundreds of angular samples arbitrarily close to the
    # origin. A Cartesian mesh has only a handful there, regardless of its size.
    x, y = make_square_polar_mesh(
        half_width, inner_radius, radial_points, angular_points
    )
    z = f(x, y)

    # Use a light pastel map and add gentle directional shading without allowing
    # shadowed faces to become dark.
    color_limit = np.nanmax(np.abs(z))
    color_norm = colors.Normalize(vmin=-color_limit, vmax=color_limit)
    pastel_cmap = colors.LinearSegmentedColormap.from_list(
        "pastel_surface",
        ["#b9afe8", "#9ed3e8", "#bfe6cc", "#f4ce9b", "#e99fb2"],
    )
    face_colors = pastel_cmap(color_norm(z))
    light = LightSource(azdeg=135, altdeg=55)

    radius = np.hypot(x, y)
    theta = np.arctan2(y, x)
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)
    dz_dtheta = sin_theta * (2 * cos_theta**2 - sin_theta**2)
    surface_normals = np.stack(
        (sin_theta * dz_dtheta, -cos_theta * dz_dtheta, radius), axis=-1
    )
    surface_normals /= np.linalg.norm(surface_normals, axis=-1, keepdims=True)
    diffuse_light = np.clip(surface_normals @ light.direction, 0.0, 1.0)

    # Darken in HSV space and raise saturation in shadow, rather than blending
    # toward gray. This gives the pastel surface clearer, colored contrast.
    shadow = 1.0 - diffuse_light
    shaded_hsv = colors.rgb_to_hsv(face_colors[..., :3])
    shaded_hsv[..., 1] = np.clip(
        shaded_hsv[..., 1] * (1.0 + 0.4 * shadow), 0.0, 1.0
    )
    shaded_hsv[..., 2] *= 0.68 + 0.32 * diffuse_light
    face_colors[..., :3] = colors.hsv_to_rgb(shaded_hsv)

    fig = plt.figure(figsize=(10, 8), layout="constrained")
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(
        x,
        y,
        z,
        rcount=radial_points,
        ccount=angular_points,
        facecolors=face_colors,
        linewidth=0,
        antialiased=False,
        shade=False,
    )

    ax.set(
        xlim=(-half_width, half_width),
        ylim=(-half_width, half_width),
        zlim=(-1.05 * color_limit, 1.05 * color_limit),
        xlabel=r"$x$",
        ylabel=r"$y$",
        zlabel=r"$f(x,y)$",
    )
    ax.set_box_aspect((1, 1, 0.55))
    ax.view_init(elev=30, azim=135)
    plt.show()


if __name__ == "__main__":
    main()
