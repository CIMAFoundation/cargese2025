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
    return FUEL_SYSTEM_LEGACY_DICT, PropagatorOutOfBoundsError, mo, np


@app.cell
def _(FUEL_SYSTEM_LEGACY_DICT, mo):
    # create controls for later usage
    wind_speed_slider = mo.ui.slider(label="Wind Speed km/h", start=0, stop=50, step=5, value=10)
    wind_dir_slider = mo.ui.slider(label="Wind Dir [°]", start=0, stop=360, step=45, value=0)
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
    return (TIME_LIMIT,)


@app.cell
def _(PropagatorOutOfBoundsError, TIME_LIMIT, mo):
    # initialize the simulator object
    pass
    # create boundary conditions
    pass
    # set them
    pass

    time = 0
    # execute the simulation
    with mo.status.spinner(title="Running ...") as _spinner:
        # run the simulation
        while False:
            try:
                ...            
            except PropagatorOutOfBoundsError:
                break
            _spinner.update(subtitle=f"progress:{int(100*time/TIME_LIMIT)}%")
            if time >= TIME_LIMIT:
                break
    return


@app.cell
def _():
    # extract output and plot
    pass

    #fig = plt.figure()
    #plt.imshow(fire_probability, cmap='hot')
    #plt.title(label=f"Probability at time {int(time/3600)}h")
    #plt.colorbar()
    #fig
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
