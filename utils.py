import numpy as np
from datetime import timedelta
from propagator.core.constants import FUEL_SYSTEM_LEGACY_DICT # type: ignore
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from propagator.core import Propagator # type: ignore
from matplotlib.image import AxesImage
from typing import Optional

veg_colors = [
    "#228B22",  # 1: broadleaves - forest green
    "#7CFC00",  # 2: shrubs - lawn green
    "#D3D3D3",  # 3: non-vegetated - light gray
    "#ADFF2F",  # 4: grassland - green-yellow
    "#006400",  # 5: conifers - dark green
    "#FFD700",  # 6: agro-forestry - gold
    "#8B4513",  # 7: non-fire prone forests - brown
]
cmap = ListedColormap(veg_colors)
bounds = np.arange(0.5, len(veg_colors) + 1.5)
norm = BoundaryNorm(bounds, cmap.N)

tick_labels = [f"{i}: {FUEL_SYSTEM_LEGACY_DICT[i]['name']}" for i in range(1, len(veg_colors) + 1)]


def plot_vegetation(simulator: Propagator) -> AxesImage:
    """
    Plots the vegetation map of the simulator.
    """
    ax = plt.imshow(simulator.veg, cmap=cmap, norm=norm)
    cbar = plt.colorbar(ax, ticks=range(1, len(veg_colors) + 1))
    cbar.ax.set_yticklabels(tick_labels)
    cbar.set_label("Vegetation Type", rotation=270, labelpad=15)
    plt.title("Vegetation Map")
    return ax

def plot_results(simulator: Propagator, scar: Optional[np.ndarray]=None, thresholds:list[float]=[0.5], colors: list[str]=['red']) -> AxesImage:
    """
    Plots the simulation results including vegetation types, fire probability contour, and overlayed scar contour.
    """
    output = simulator.get_output()
    fire_probability = output.fire_probability

    ax = plot_vegetation(simulator)
    plt.title(label=f"Probability at time {timedelta(seconds=int(simulator.time))}")

    for t, c in zip(thresholds, colors):
        plt.contour(fire_probability, levels=[t], colors=[c], linewidths=2)

    if scar is not None:
        plt.contour(scar, levels=[0.5], colors='violet', linewidths=2)

    return ax