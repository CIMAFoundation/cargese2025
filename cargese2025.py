import marimo

__generated_with = "0.17.6"
app = marimo.App(width="medium")


@app.cell
def _():
    # import relevant stuff
    import marimo as mo
    import numpy as np
    from matplotlib import pyplot as plt
    from propagator.core import Propagator, BoundaryConditions, PropagatorOutOfBoundsError
    from propagator.core.constants import FUEL_SYSTEM_LEGACY_DICT
    return (
        BoundaryConditions,
        FUEL_SYSTEM_LEGACY_DICT,
        Propagator,
        PropagatorOutOfBoundsError,
        mo,
        np,
        plt,
    )


@app.cell
def _(FUEL_SYSTEM_LEGACY_DICT, mo):
    # create controls for later usage
    wind_speed_slider = mo.ui.slider(label="Wind Speed km/h", start=0, stop=50, step=5, value=10)
    wind_dir_slider = mo.ui.slider(label="Wind Dir [°]", start=0, stop=360, step=45, value=135)
    fuel_moisture_slider = mo.ui.slider(label="Fuel Moisture [%]", start=0, stop=50, step=5, value=5)
    terrain_slope_slider = mo.ui.slider(label="Slope [%]", start=0, stop=50, step=5, value=10)
    veg_options = {value['name']:key for  key, value in FUEL_SYSTEM_LEGACY_DICT.items()}
    veg_dropdown = mo.ui.dropdown(
        options=veg_options,
        value='shrubs',
        label="Select Veg Type",
    )
    mo.vstack([
        wind_speed_slider,
        wind_dir_slider,
        fuel_moisture_slider,
        terrain_slope_slider,
        veg_dropdown
    ],  justify='center')
    return (
        fuel_moisture_slider,
        terrain_slope_slider,
        veg_dropdown,
        wind_dir_slider,
        wind_speed_slider,
    )


@app.cell
def _(
    fuel_moisture_slider,
    np,
    terrain_slope_slider,
    veg_dropdown,
    wind_dir_slider,
    wind_speed_slider,
):
    TIME_LIMIT = 6*3600

    # create synthetic data
    DIM = 300
    dem_slice = np.linspace(0, 20 * DIM*(terrain_slope_slider.value/100), DIM)
    dem = np.tile(dem_slice, (DIM,1))
    veg = np.full((DIM, DIM), veg_dropdown.value)

    wind_speed = np.full((DIM, DIM), wind_speed_slider.value)
    wind_dir = np.full((DIM, DIM), wind_dir_slider.value)
    fuel_moisture = np.full((DIM, DIM), fuel_moisture_slider.value)

    ignition_mask = np.full((DIM, DIM), False)
    ignition_mask[int(DIM/2), int(DIM/2)] = True
    return (
        TIME_LIMIT,
        dem,
        fuel_moisture,
        ignition_mask,
        veg,
        wind_dir,
        wind_speed,
    )


@app.cell
def _(
    BoundaryConditions,
    Propagator,
    PropagatorOutOfBoundsError,
    TIME_LIMIT,
    dem,
    fuel_moisture,
    ignition_mask,
    mo,
    veg,
    wind_dir,
    wind_speed,
):
    # initialize the simulation
    sim = Propagator(dem=dem, veg=veg, realizations=10)

    bc = BoundaryConditions(
        time=0,
        ignition_mask=ignition_mask,
        wind_dir=wind_dir,
        wind_speed=wind_speed,
        moisture=fuel_moisture
    )

    sim.set_boundary_conditions(bc)

    with mo.status.spinner(title="Running ...") as _spinner:
        # run the simulation
        while next_time := sim.next_time() is not None:
            try:
                sim.step()
            except PropagatorOutOfBoundsError:
                break
            _spinner.update(subtitle=f"progress:{int(100*sim.time/TIME_LIMIT)}%")
            if sim.time >= TIME_LIMIT:
                break
    return (sim,)


@app.cell
def _(plt, sim):
    # extract output and plot
    output = sim.get_output()
    fire_probability = output.fire_probability
    ros_max = output.ros_max
    fig = plt.figure()
    plt.imshow(fire_probability, cmap='hot')
    plt.title(label=f"Probability at time {int(sim.time/3600)}h")
    plt.colorbar()
    fig
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
