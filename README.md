# Rosenbrock derivative-free optimisation study

Individual KPI Optimisation Methods research project investigating Rosenbrock's rotating-coordinate method for unconstrained and penalty-constrained nonlinear optimisation. The project received **100/100**.

## Implemented methods

- Rosenbrock rotating-coordinate derivative-free optimisation
- direction reconstruction and stopping criteria
- circular, linear and non-convex feasibility constraints
- penalty-constrained optimisation
- Sven interval bracketing
- golden-section line search
- DSK–Powell quadratic interpolation
- convergence and parameter-sensitivity experiments

The supplementary coursework source also contains implementations of coordinate/accelerated search, Hooke–Jeeves, Nelder–Mead, steepest descent, Partan, Newton, Fletcher–Reeves and DFP methods.

## Repository structure

```text
src/rosenbrock_optimizer.py          Main research implementation
src/supplementary_algorithms/        Related optimisation coursework
report/optimization_research_project.pdf
report/supplementary/                Supporting method reports
```

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/rosenbrock_optimizer.py
```

The script prints comparison tables and opens Matplotlib figures for convergence and optimisation trajectories.

## Main experimental questions

- How do initial position and initial coordinate steps affect convergence?
- How do expansion, contraction and stopping parameters change evaluation counts?
- How does the method behave on convex, linearly constrained and non-convex regions?
- How do the golden-section and DSK–Powell searches compare along an active boundary?

## Technology

Python, NumPy and Matplotlib.

## Academic context

KPI, BSc Applied Mathematics / Data Science and Mathematical Modelling, 2026. The full project report is included in `report/`.

