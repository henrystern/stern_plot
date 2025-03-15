"""Functions for exporting and importing plots."""

from pathlib import Path

from plotly.graph_objects import Figure

import stern_plot.theme as theme


def show(fig, key):
    """Show the plot with the custom config options."""
    fig[key].show(config=theme.get_config_options(key))


def write_all(fig: dict, dest: Path, fmt="json"):
    """Write dictionary of figure name to figure to destination folder."""
    for k, f in fig.items():
        write(f, dest / f"{k}.{fmt}")


def write(f: Figure, dest: Path):
    """Write an individual figure to destination file."""
    if dest.suffix == ".json":
        f.write_json(dest)
    elif dest.suffix == ".html":
        f.write_html(
            dest,
            config=theme.get_config_options(dest.stem),
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
