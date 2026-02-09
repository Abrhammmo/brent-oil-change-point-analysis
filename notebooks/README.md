# notebooks

Exploratory Jupyter notebooks used to run the data processing, analysis, and visualizations for the project.

Key notebooks

- `time_series_analysis.ipynb`: end-to-end time series analysis and preprocessing pipeline.
- `changepoint_analysis.ipynb`: focused notebook for change-point detection experiments and diagnostics.

How to use

- Install project dependencies and ensure the project root is on the Python path so notebooks can `import src` modules.
- Open notebooks in Jupyter or VS Code and run cells interactively.

Notes

- Keep heavy data-processing code in `src/` and use notebooks mainly for orchestration and visualization.
