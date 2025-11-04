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
    from utils import plot_results
    return (
        BoundaryConditions,
        Propagator,
        PropagatorOutOfBoundsError,
        mo,
        plot_results,
        rio,
    )


@app.cell
def _(mo):
    mo.md("""
    #Venafro Fire simulation
    Simple example of using Propagator CORE to simulate a real fire.
    """)
    return


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
    simulator.set_boundary_conditions(
        BoundaryConditions(
            time=0,
            ignitions=[IGNITION_POINT],
            wind_dir=wind_dir_slider.value,
            wind_speed=wind_speed_slider.value,
            moisture=fuel_moisture_slider.value
        )
    )
    return simulator, time_limit


@app.cell
def _(
    PropagatorOutOfBoundsError,
    mo,
    plot_results,
    scar,
    simulator,
    time_limit,
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

        ax = plot_results(simulator, scar)

    ax
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
