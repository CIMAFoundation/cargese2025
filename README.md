## Propagator Examples (Cargèse 2025)

This repository contains the material used during the [ workshop at Cargèse 2025](https://forefireapi.github.io/cargese2025).  Each script demonstrates how to drive the **Propagator** fire spread core directly from Python, either through a lightweight script (`simple_example.py`) or via interactive [marimo](https://marimo.io) apps (`venafro.py`, `monti_pisani.py`).  The focus is on fire-simulation workflows that can be re-used in your own studies.

### Repository layout

- `simple_example.py` – fully scripted synthetic scenario showcasing the Propagator API in just a few lines.
- `venafro.py` – marimo app driven by DEM/vegetation/scar rasters (`venafro_*.tif`) to replay the Venafro case study.
- `monti_pisani.py` – marimo app running ensembles of random ignitions over the Monti Pisani rasters.
- `utils.py` – shared plotting helpers (vegetation map, probability/contour overlays).
- `pyproject.toml` / `uv.lock` – dependency pins (Propagator git revision, marimo, rasterio, matplotlib).

### Prerequisites

- Python ≥ 3.13
- [uv](https://github.com/astral-sh/uv) **or** any virtual environment capable of installing packages listed in `pyproject.toml`

### Install the environment

```bash
# create and populate the virtual environment using uv
uv sync

# alternatively, standard venv + pip
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

> ℹ️ The `propagator` dependency is pulled directly from the CIMA Foundation repository at commit `6674076`, matching the version demonstrated during the workshop.

### Run the scripted example

```bash
uv run python simple_example.py
```

This script builds a synthetic flat DEM, applies constant wind/moisture settings, and runs the simulation for up to six hours (simulation time).  When it completes it displays the probability surface using `matplotlib`.

### Launch the marimo apps

Each marimo file can be run independently; choose the one that matches your scenario:

```bash
# Venafro case study (uses venafro_* rasters)
uv run marimo run venafro.py

# Monti Pisani ensemble (ignition uncertainty)
uv run marimo run monti_pisani.py
```

While the app is running you can experiment with wind speed/direction, moisture, simulation time, number of realizations, and (for Monti Pisani) ignition-radius uncertainty.  The UI shows progress via marimo’s status spinner, and plots are updated once the solver finishes.

### More information

- Workshop page: https://forefireapi.github.io/cargese2025
- Propagator core: https://github.com/CIMAFoundation/propagator_sim

----------------------------------------
[Presentation PDF](presentation.pdf)