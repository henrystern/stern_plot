"""Functions for exporting and importing plots."""

from pathlib import Path

from plotly.graph_objects import Figure
import plotly.io as pio

from sternplot.theme import get_config_options


def show(fig, key):
    """Show the plot with the custom config options."""
    if isinstance(fig, dict):
        fig[key].show(config=get_config_options(key))
    elif isinstance(fig, Figure):
        fig.show(config=get_config_options(key))


def write_all(fig: dict, dest: Path, fmt="json"):
    """Write dictionary of figure name to figure to destination folder."""
    if fmt in ["png", "jpg", "jpeg", "webp", "svg", "pdf", "eps"]:
        pio.write_images(
            fig.values(),
            [f"{k}.{fmt}" for k in fig.keys()],
            format=fmt,
            scale=3,
        )
        return
    for k, f in fig.items():
        write(f, dest / f"{k}.{fmt}")


def write(f: Figure, dest: Path):
    """Write an individual figure to destination file."""
    if dest.suffix == ".json":
        f.write_json(dest)
    elif dest.suffix == ".html":
        f.write_html(
            dest,
            config=get_config_options(dest.stem),
            include_plotlyjs="cdn",
        )
    elif dest.suffix in [
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".svg",
        ".pdf",
        ".eps",
    ]:
        f.write_image(
            dest,
            format=dest.suffix[1:],
            scale=3,
        )

    else:
        raise ValueError(
            f"Unknown file format {dest.suffix} for figure {dest.stem}."
        )
