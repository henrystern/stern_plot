"""Configuration parameters and paths."""

from io import BytesIO
from pathlib import Path

import requests

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[0]
FAVICON_PATH = PROJ_ROOT / "static/favicon.png"

if not FAVICON_PATH.exists():
    logo_url = "https://hstern.ca/static/assets/web-app-manifest-512x512.png"
    FAVICON_PATH = BytesIO(requests.get(logo_url).content)
