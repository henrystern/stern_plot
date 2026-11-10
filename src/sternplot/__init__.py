"""Define themes for plotly plots."""
# ruff: noqa: F401

from typing import Literal

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from .adjust import add_notes
from .config import theme_colours, theme_scales
from .plot_io import show, write_all
from .theme import set_plot_scaling, set_plot_template
from .touchup import touchup

type NewTemplate = Literal[
    "hstern_dark", "hstern_light", "dracula", "economist", "revealjs"
]

for theme_name, colours in theme_colours.items():
    pio.templates[theme_name] = set_plot_template(colours)

for theme_name, scale in theme_scales.items():
    pio.templates[theme_name] = set_plot_scaling(scale)


def set_as_default(template: NewTemplate = "hstern_dark"):
    """Set one of the newly created templates as the default for all plotly figures."""
    pio.templates.default = template


# Monkey-patch go.Figure to support .pipe()
if not hasattr(go.Figure, "pipe"):
    setattr(
        go.Figure,
        "pipe",
        lambda self, func, *args, **kwargs: func(self, *args, **kwargs),
    )
