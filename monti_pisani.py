import marimo

__generated_with = "0.17.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # Monti Pisani Scenarios
    Simple example of ensemble simulation in Monti Pisani area.

    Each realization will start a fire from a different random ignition point inside the radius.
    """)
    return


@app.cell
def _():
    import numpy as np
    from datetime import timedelta
    from matplotlib import pyplot as plt
    from propagator.core import Propagator, BoundaryConditions, PropagatorOutOfBoundsError
    from propagator.core.constants import FUEL_SYSTEM_LEGACY_DICT
    import rasterio as rio
    from utils import plot_results, plot_vegetation
    import random
    return (
        BoundaryConditions,
        Propagator,
        np,
        plot_vegetation,
        plt,
        random,
        rio,
    )


@app.cell
def _(mo):
    realizations_slider = mo.ui.slider(label="Number of simulations", start=1, stop=100, step=1, value=10, show_value=True)
    radius_slider = mo.ui.slider(label="Uncertainty radius (pixels)", start=100, stop=300, step=50, value=300, show_value=True)

    timesteps_slider = mo.ui.slider(label="Simulation time [hours]", start=1, stop=12, step=1, value=6, show_value=True)
    wind_speed_slider = mo.ui.slider(label="Wind Speed km/h", start=0, stop=50, step=1, value=25,  show_value=True)
    wind_dir_slider = mo.ui.slider(label="Wind Dir [°]", start=0, stop=360, step=5, value=180, show_value=True)
    fuel_moisture_slider = mo.ui.slider(label="Fuel Moisture [%]", start=0, stop=50, step=1, value=6, show_value=True)
    return (
        fuel_moisture_slider,
        radius_slider,
        realizations_slider,
        timesteps_slider,
        wind_dir_slider,
        wind_speed_slider,
    )


@app.cell
def _(
    fuel_moisture_slider,
    mo,
    radius_slider,
    realizations_slider,
    timesteps_slider,
    wind_dir_slider,
    wind_speed_slider,
):
    mo.vstack([
        realizations_slider,
        radius_slider,
        timesteps_slider,
        wind_speed_slider,
        wind_dir_slider,
        fuel_moisture_slider,
    ],  justify='center')
    return


@app.cell
def _(rio):
    with rio.open('monti_pisani_dem.tif') as f:
        dem = f.read(1)

    with rio.open('monti_pisani_veg.tif') as f:
        veg = f.read(1)
    return dem, veg


@app.cell
def _(
    BoundaryConditions,
    Propagator,
    dem,
    fuel_moisture_slider,
    radius_slider,
    random,
    realizations_slider,
    timesteps_slider,
    veg,
    wind_dir_slider,
    wind_speed_slider,
):
    realizations = realizations_slider.value
    radius = radius_slider.value
    nrows, ncols = dem.shape
    center_x, center_y = int(nrows/2), int(ncols/2)

    ignition_points = [(
        int(random.random() * radius - radius/2) + center_y, 
        int(random.random() * radius - radius/2) + center_x, 
       r
    ) for r in range(realizations)]
    time_limit = timesteps_slider.value * 3600
    simulator = Propagator(
        dem=dem,
        veg=veg,
        realizations=realizations,
        out_of_bounds_mode='ignore'
    )
    simulator.set_boundary_conditions(
        BoundaryConditions(
            time=0,
            ignitions=ignition_points,
            wind_dir=wind_dir_slider.value,
            wind_speed=wind_speed_slider.value,
            moisture=fuel_moisture_slider.value
        )
    )
    return simulator, time_limit


@app.cell
def _(mo, np, plot_vegetation, plt, simulator, time_limit):
    with mo.status.spinner(title="Running ...") as _spinner:
        while True:
            next_time = simulator.next_time()
            if next_time is None:
                break
            if next_time > time_limit:
                break

            simulator.step()
            _spinner.update(subtitle=f"{simulator.time}/{time_limit}")            

    
        fire_probability = simulator.get_output().fire_probability
        fire_probability[fire_probability == 0] = np.nan
        ax_veg = plot_vegetation(simulator)
        plt.figure()
        ax_contour = plt.contourf(fire_probability)
        plt.colorbar()



    mo.vstack([ax_veg, ax_contour])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
