import marimo

__generated_with = "0.17.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    from datetime import timedelta
    from matplotlib import pyplot as plt
    from propagator.core import Propagator, BoundaryConditions, PropagatorOutOfBoundsError
    from propagator.core.constants import FUEL_SYSTEM_LEGACY_DICT
    import rasterio as rio

    return (
        BoundaryConditions,
        FUEL_SYSTEM_LEGACY_DICT,
        Propagator,
        PropagatorOutOfBoundsError,
        mo,
        np,
        plt,
        rio,
        timedelta,
    )


@app.cell
def _(mo):
    mo.md("""
    #Venafro Fire simulation
    Simple example of using Propagator CORE to simulate a real fire.
    """)
    return


@app.cell
def _(np):
    from matplotlib.colors import ListedColormap, BoundaryNorm
    colors = [
        "#228B22",  # 1: broadleaves - forest green
        "#7CFC00",  # 2: shrubs - lawn green
        "#D3D3D3",  # 3: non-vegetated - light gray
        "#ADFF2F",  # 4: grassland - green-yellow
        "#006400",  # 5: conifers - dark green
        "#FFD700",  # 6: agro-forestry - gold
        "#8B4513",  # 7: non-fire prone forests - brown
    ]
    cmap = ListedColormap(colors)
    bounds = np.arange(0.5, len(colors) + 1.5)
    norm = BoundaryNorm(bounds, cmap.N)
    return cmap, colors, norm


@app.cell
def _(mo):
    realizations_slider = mo.ui.slider(label="Number of simulations", start=1, stop=100, step=1, value=10, show_value=True)

    timesteps_slider = mo.ui.slider(label="Simulation time [hours]", start=1, stop=12, step=1, value=3, show_value=True)
    wind_speed_slider = mo.ui.slider(label="Wind Speed km/h", start=0, stop=50, step=1, value=13,  show_value=True)
    wind_dir_slider = mo.ui.slider(label="Wind Dir [°]", start=0, stop=360, step=5, value=180, show_value=True)
    fuel_moisture_slider = mo.ui.slider(label="Fuel Moisture [%]", start=0, stop=50, step=1, value=6, show_value=True)
    return (
        fuel_moisture_slider,
        realizations_slider,
        timesteps_slider,
        wind_dir_slider,
        wind_speed_slider,
    )


@app.cell
def _(
    fuel_moisture_slider,
    mo,
    realizations_slider,
    timesteps_slider,
    wind_dir_slider,
    wind_speed_slider,
):
    mo.vstack([
        realizations_slider,
        timesteps_slider,
        wind_speed_slider,
        wind_dir_slider,
        fuel_moisture_slider,
    ],  justify='center')
    return


@app.cell
def _(rio):
    with rio.open('venafro_dem.tif') as f:
        dem = f.read(1)

    with rio.open('venafro_veg.tif') as f:
        veg = f.read(1)

    with rio.open('venafro_scar.tif') as f:
        scar = f.read(1)
    return dem, scar, veg


@app.cell
def _(
    BoundaryConditions,
    Propagator,
    dem,
    fuel_moisture_slider,
    np,
    realizations_slider,
    timesteps_slider,
    veg,
    wind_dir_slider,
    wind_speed_slider,
):
    IGNITION_POINT = (49,53)
    time_limit = timesteps_slider.value * 3600
    simulator = Propagator(
        dem=dem,
        veg=veg,
        realizations=realizations_slider.value
    )
    ignition_mask = np.zeros(veg.shape)
    ignition_mask[IGNITION_POINT] = 1
    simulator.set_boundary_conditions(
        BoundaryConditions(
            time=0,
            ignition_mask=ignition_mask,
            wind_dir=np.full(veg.shape, wind_dir_slider.value),
            wind_speed=np.full(veg.shape, wind_speed_slider.value),
            moisture=np.full(veg.shape, fuel_moisture_slider.value)
        )
    )
    return simulator, time_limit


@app.cell
def _(
    FUEL_SYSTEM_LEGACY_DICT,
    PropagatorOutOfBoundsError,
    cmap,
    colors,
    mo,
    norm,
    plt,
    scar,
    simulator,
    time_limit,
    timedelta,
    veg,
):
    with mo.status.spinner(title="Running ...") as _spinner:
        while True:
            next_time = simulator.next_time()
            if next_time is None:
                break
            if next_time > time_limit:
                break

            try:
                simulator.step()
                _spinner.update(subtitle=f"{simulator.time}/{time_limit}")            
            except PropagatorOutOfBoundsError:
                _spinner.update(subtitle="Simulation stopped: fire reached out of bounds area.")
                break

        output = simulator.get_output()
        fire_probability = output.fire_probability
        ax = plt.imshow(veg, cmap=cmap, norm=norm)
        cbar = plt.colorbar(ax, ticks=range(1, len(colors) + 1))
        cbar.ax.set_yticklabels([f"{i}: {FUEL_SYSTEM_LEGACY_DICT[i]['name']}" for i in range(1, len(colors) + 1)])
        cbar.set_label("Vegetation Type", rotation=270, labelpad=15)
        plt.title(label=f"Probability at time {timedelta(seconds=int(simulator.time))}")

        plt.contour(fire_probability, levels=[0.5], colors="red", linewidths=2)
        plt.contour(scar, levels=[0.5], colors='violet', linewidths=2)

    ax
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
