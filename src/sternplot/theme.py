"""Set the default layout and output configuration for plotly plots."""

from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from typing import Annotated, List

from PIL import Image
import plotly.graph_objects as go


@dataclass(frozen=True)
class ThemeColourSpec:
    """Specify the colours used to adjust the template."""

    background: Annotated[str, "The background colour."]
    foreground: Annotated[str, "The font colour of the plot's text."]
    title: Annotated[str, "The font colour of the title."]
    gridlines: Annotated[
        str, "The colour of the gridlines, axislines and zerolines."
    ]
    shade: Annotated[str, "The colour used for shading forecast areas."]
    palette: Annotated[
        List[str], "The discrete colour palette for the plot traces."
    ]
    logo: Annotated[
        Path | BytesIO | None,
        "The path to a logo image, or none to skip adding the logo.",
    ] = None
    xaxis_kwargs: Annotated[dict, "The dictionary of xaxis options."] = field(
        default_factory=dict
    )
    yaxis_kwargs: Annotated[dict, "The dictionary of yaxis options."] = field(
        default_factory=dict
    )


@dataclass(frozen=True)
class ThemeScaleSpec:
    """Specify the scales used to adjust the template."""

    scale: Annotated[float, "The text scaling factor."]
    width: Annotated[int, "The plot width."]
    height: Annotated[int, "The plot height."]


def set_plot_template(spec: ThemeColourSpec):
    """Set the plot layout template for plotly"""
    font = "Muli, 'Open Sans', Verdana, Arial, sans-serif"
    axis_kwargs = dict(
        showline=True,
        linecolor=spec.foreground,
        gridcolor=spec.gridlines,
        linewidth=2,
    )
    custom_template = go.layout.Template(
        layout=dict(
            # NOTE Don't bother making responsive, text doesn't scale and looks worse than rescaling png.
            # If you need it to be responsive add a link to a related plot with no annotations.
            autosize=False,
            width=800,
            height=511,
            plot_bgcolor=spec.background,
            paper_bgcolor=spec.background,
            font=dict(color=spec.foreground, family=font, size=12),
            title=dict(
                x=0.08,
                xanchor="left",
                yanchor="top",
                font=dict(color=spec.title, size=25),
            ),
            yaxis=dict(axis_kwargs | spec.yaxis_kwargs),
            xaxis=dict(axis_kwargs | spec.xaxis_kwargs),
            legend=dict(
                font=dict(size=14),
                # bgcolor="rgb(0, 0, 0, 1)",  # Transparent background
            ),
            colorway=spec.palette,
            images=[
                dict(
                    layer="above",
                    name="Logo",
                    source=Image.open(spec.logo),
                    xref="paper",
                    yref="paper",
                    x=0.99,
                    y=-0.08,
                    sizex=0.08,
                    sizey=0.08,
                    xanchor="right",
                    yanchor="top",
                )
            ]
            if spec.logo
            else None,
        ),
    )
    return custom_template


def set_plot_scaling(spec: ThemeScaleSpec):
    """Create a plotly template to scale text to a context."""
    custom_template = go.layout.Template(
        layout=dict(
            font=dict(size=spec.scale * 12),
            title=dict(font=dict(size=spec.scale * 20)),
            legend=dict(font=dict(size=spec.scale * 14)),
            width=spec.width,
            height=spec.height,
        )
    )
    return custom_template


def get_config_options(filename_stem, overrides={}):
    """Get configuration options for plot output. Filename_stem is default name on save, without extension."""
    default_config = {
        "displaylogo": False,
        "modeBarButtonsToRemove": [
            "zoomin",
            "zoomout",
            "autoscale",
        ],
        "toImageButtonOptions": {"filename": filename_stem, "scale": 3},
        "responsive": False,
        "showTips": False,
    }
    return default_config | overrides
