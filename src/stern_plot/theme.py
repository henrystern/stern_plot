"""Set the default layout and output configuration for plotly plots."""

from PIL import Image
import plotly.graph_objects as go
import plotly.io as pio

from stern_plot.config import FAVICON_PATH


def set_plot_template(colour, palette):
    """Set the plot layout template for plotly"""
    font = "Muli, 'Open Sans', Verdana, Arial, sans-serif"
    custom_template = go.layout.Template(
        layout=dict(
            plot_bgcolor=colour["background"],
            paper_bgcolor=colour["background"],
            font=dict(color=colour["foreground"], family=font),
            title=dict(
                x=0.08,
                xanchor="left",
                yanchor="top",
                font=dict(color=colour["title"], size=25),
            ),
            yaxis=dict(
                showline=True,
                linecolor=colour["foreground"],
                linewidth=2,
                gridcolor=colour["gridlines"],
                # automargin=True,
            ),
            xaxis=dict(
                showline=True,
                linecolor=colour["foreground"],
                linewidth=2,
                gridcolor=colour["gridlines"],
                # automargin=True,
            ),
            legend=dict(
                font=dict(size=14),
                # bgcolor="rgb(0, 0, 0, 1)",  # Transparent background
            ),
            colorway=palette,
            # NOTE Don't bother making responsive, text doesn't scale and looks worse than rescaling png.
            # If you need it to be responsive add a link to a related plot with no annotations.
            width=800,
            height=511,
            images=[
                dict(
                    layer="above",
                    name="Logo",
                    source=Image.open(FAVICON_PATH),
                    xref="paper",
                    yref="paper",
                    x=0.99,
                    y=-0.08,
                    sizex=0.11,
                    sizey=0.11,
                    xanchor="right",
                    yanchor="top",
                )
            ],
        ),
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


site_colour = {
    "dark_green": "#1f3023",
    "light_green": "#003601",
    "dark_grey": "#394148",
    "light_grey": "#a0a0a0",
    "light_pink": "#eeccff",
    "lighter_pink": "#e1c1f2",
}

light_theme = {
    "background": site_colour["light_pink"],
    "foreground": site_colour["dark_grey"],
    "title": site_colour["light_green"],
    "gridlines": site_colour["lighter_pink"],
}
dark_theme = {
    "background": site_colour["dark_green"],
    "foreground": site_colour["light_grey"],
    "title": site_colour["light_pink"],
    "gridlines": site_colour["dark_grey"],
}


dark_palette = [
    "#fd7f6f",
    "#7eb0d5",
    "#b2e061",
    "#bd7ebe",
    "#ffb55a",
    "#ffee65",
    "#beb9db",
    "#fdcce5",
    "#8bd3c7",
]
light_palette = dark_palette  # TODO define light_palette


pio.templates["hstern_dark"] = set_plot_template(dark_theme, dark_palette)
pio.templates["hstern_light"] = set_plot_template(light_theme, light_palette)
