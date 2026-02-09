# Dashboard Images

This folder stores static images used by documentation and the dashboard prototype (PNG). Images are intended for reports, README illustrations, and quick visual references — not as primary data sources.

Contents and purpose

Image provenance and regeneration

Quick instructions to regenerate a figure

1. Open the relevant notebook in `notebooks/` (e.g., `time_series_analysis.ipynb`).
2. Re-run the plotting cell(s) that produce the figure.
3. Export or save the figure to this folder (prefer SVG for vector charts or PNG for raster):

```python
fig.savefig('dashboard_imgs/figures/my_figure.svg', bbox_inches='tight')
```

Best practices

If you'd like, I can scan notebooks for figure-generating cells and add a small script to automate exporting the main figures into this folder.

Major images (descriptions)

- `event impact and prices.png`: Combined view showing the Brent price series with annotated events and computed event impacts (pre/post comparison). Use to explain how specific events correlate with price moves.
- `filters for date and event.png`: Screenshot of the frontend filters UI allowing users to select date ranges and event types; useful for documenting interactive controls and expected behavior.
- `home_page.png`: The dashboard landing view — overview charts, high-level stats, and navigation to the events and analysis pages.
- `price analysis for an event.png`: Deep-dive visual showing price series around a selected event, including local trend lines and summary statistics (pre/post means and volatility).
- `price change around key events.png`: Aggregated chart that overlays price changes around multiple key events (aligned at event date) to visualize typical responses.
- `Responsive frontend check.png`(GALAXY Z FOLD): Mobile / small-screen screenshot demonstrating responsive layout and component stacking for narrow viewports.
- `Responsive frontend check.png` (desktop): Desktop / wide-screen screenshot showing full layout and side-by-side components (this filename is reused for both checks in the repo).
- `volatility analysis and events.png`: Chart combining rolling volatility metrics with event markers to show temporal alignment between volatility spikes and real-world events.
- `volatility analysis for an event.png`: Focused volatility plot around a single event, showing how volatility changes in the event window and summary metrics.

