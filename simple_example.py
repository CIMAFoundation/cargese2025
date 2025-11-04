import numpy as np
from matplotlib import pyplot as plt
from propagator.core import Propagator, BoundaryConditions, PropagatorOutOfBoundsError

TIME_LIMIT = 6*3600

# create synthetic data
DIM = 300
dem = np.full((DIM, DIM), 0) # flat terrain
veg = np.full((DIM, DIM), 5) # conifers

wind_speed = 30 # km/h
wind_dir = 180 # southern wind 
fuel_moisture = 5 # dry conditions
ignitions = [(DIM-50, int(DIM/2))] # ignition point


# initialize the simulator object
simulator = Propagator(
    dem=dem,
    veg=veg,
    realizations=50,
    do_spotting=False
)

bc = BoundaryConditions(
    time=0,
    ignitions=ignitions, # type: ignore
    moisture=fuel_moisture,
    wind_dir=wind_dir,
    wind_speed=wind_speed
)

simulator.set_boundary_conditions(bc)


"""fire_break = np.full(veg.shape, np.nan)
fire_break[int(DIM/2):int(DIM/2)+3, :] = 3 # no fuel according to FUEL_SYSTEM_LEGACY
bc = BoundaryConditions(
    time=0,
    vegetation_changes=fire_break
)
simulator.set_boundary_conditions(bc)"""



# run the simulation
while simulator.next_time() is not None:
    try:
        simulator.step()
        print(simulator.time)
    except PropagatorOutOfBoundsError:
        break
    
    if simulator.time >= TIME_LIMIT:
        break

output = simulator.get_output()
fire_probability = output.fire_probability
fig = plt.figure()
plt.imshow(fire_probability, cmap='hot')
plt.title(label=f"Probability at time {int(simulator.time/3600)}h")
plt.colorbar()
plt.show()
