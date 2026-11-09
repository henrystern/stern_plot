"""Configuration parameters and paths."""

from io import BytesIO
from pathlib import Path

import requests

from sternplot.theme import ThemeColourSpec, ThemeScaleSpec

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[0]
FAVICON_PATH = PROJ_ROOT / "static/favicon.png"

if not FAVICON_PATH.exists():
    logo_url = "https://hstern.ca/static/assets/web-app-manifest-512x512.png"
    FAVICON_PATH = BytesIO(requests.get(logo_url).content)

site_colour = {
    "dark_green": "#1f3023",
    "light_green": "#003601",
    "dark_grey": "#394148",
    "light_grey": "#a0a0a0",
    "light_pink": "#eeccff",
    "lighter_pink": "#e1c1f2",
}
dracula = {
    "Background": "#282A36",
    "Foreground": "#F8F8F2",
    "Selection": "#44475A",
    "Comment": "#6272A4",
    "Red": "#FF5555",
    "Orange": "#FFB86C",
    "Yellow": "#F1FA8C",
    "Green": "#50FA7B",
    "Purple": "#BD93F9",
    "Cyan": "#8BE9FD",
    "Pink": "#FF79C6",
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
dracula_palette = [
    dracula["Comment"],
    dracula["Red"],
    dracula["Orange"],
    dracula["Yellow"],
    dracula["Green"],
    dracula["Purple"],
    dracula["Cyan"],
    dracula["Pink"],
]

theme_colours = {
    "hstern_dark": ThemeColourSpec(
        background=site_colour["dark_green"],
        foreground=site_colour["light_grey"],
        title=site_colour["light_pink"],
        gridlines=site_colour["dark_grey"],
        shade="#313037",
        palette=dark_palette,
        logo=FAVICON_PATH,
    ),
    "hstern_light": ThemeColourSpec(
        background=site_colour["light_pink"],
        foreground=site_colour["dark_grey"],
        title=site_colour["light_green"],
        gridlines=site_colour["lighter_pink"],
        shade="#E6E6E6",
        palette=light_palette,
        logo=FAVICON_PATH,
    ),
    "dracula": ThemeColourSpec(
        background=dracula["Background"],
        foreground=dracula["Foreground"],
        title=dracula["Foreground"],
        gridlines=dracula["Selection"],
        shade="#313037",
        palette=dracula_palette,
        logo=None,
    ),
}

theme_scales = {"revealjs": ThemeScaleSpec(scale=1.25, width=940, height=600)}
