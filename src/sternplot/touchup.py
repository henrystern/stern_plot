"""Open a Plotly figure in the local Plotly Touchup page.

How it works
------------
* The figure JSON is written to a temp file (no URL-length limits).
* A tiny loopback-only HTTP server (127.0.0.1, background thread) serves
  plotly-touchup.html and those temp files.  A server is used instead of a
  file:// URL because browsers block fetch() from file:// pages.
* The browser is pointed at  http://localhost:<port>/plotly-touchup.html?src=figs/<file>.json

Over SSH
--------
A remote process cannot launch a browser on your laptop by itself.  Two cases:

1. Your SSH client sets $BROWSER on the remote (VS Code Remote-SSH, Cursor, ...).
   Then webbrowser.open() hands the URL to your *local* browser and the port is
   forwarded automatically.  This is used automatically.
2. Plain `ssh`.  The function prints the one-line port-forward command and URL.
   The default port is fixed (8765) so a single forward keeps working for every
   later call:  ssh -L 8765:localhost:8765 user@host
   (add `-L` on the ssh command you already use, or `~C` then `-L 8765:localhost:8765`
   inside an existing session).
"""

from __future__ import annotations

import atexit
import getpass
import http.server
import os
from pathlib import Path
import re
import shutil
import socket
import tempfile
import threading
import urllib.parse
import uuid
import webbrowser

import plotly.io as pio

__all__ = ["touchup", "stop_server"]

DEFAULT_PORT = 8765
_HTML_NAME = "plotly-touchup.html"

_lock = threading.Lock()
_server: http.server.ThreadingHTTPServer | None = None
_tmpdir: Path | None = None
_html_path: Path = Path(
    os.environ.get("PLOTLY_TOUCHUP_HTML", Path(__file__).with_name(_HTML_NAME))
)

_FIG_RE = re.compile(r"/figs/([A-Za-z0-9_-]+\.json)")
_LOCAL_HOSTS = {"localhost", "127.0.0.1", "::1"}


def _in_ssh() -> bool:
    return any(
        os.environ.get(k) for k in ("SSH_CONNECTION", "SSH_CLIENT", "SSH_TTY")
    )


class _Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):  # type: ignore # silence request logging
        pass

    def _send(
        self,
        code: int,
        body: bytes = b"",
        ctype: str = "text/plain; charset=utf-8",
    ):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_GET(self):
        # Reject odd Host headers (DNS-rebinding protection). Port forwards
        # still arrive as localhost:<port>.
        host = (
            (self.headers.get("Host") or "")
            .rsplit(":", 1)[0]
            .strip("[]")
            .lower()
        )
        if host not in _LOCAL_HOSTS:
            return self._send(403, b"forbidden")

        path = urllib.parse.urlsplit(self.path).path
        if path in ("/", "/" + _HTML_NAME):
            try:
                return self._send(
                    200, _html_path.read_bytes(), "text/html; charset=utf-8"
                )
            except OSError:
                return self._send(500, f"Cannot read {_html_path}".encode())

        m = _FIG_RE.fullmatch(path)
        if m and _tmpdir is not None:
            f = _tmpdir / m.group(1)
            if f.is_file():
                return self._send(
                    200, f.read_bytes(), "application/json; charset=utf-8"
                )
        self._send(404, b"not found")

    do_HEAD = do_GET  # noqa: N815


def _ensure_server(port: int) -> http.server.ThreadingHTTPServer:
    global _server, _tmpdir
    with _lock:
        if _server is not None:
            return _server
        if not _html_path.is_file():
            raise FileNotFoundError(
                f"{_html_path} not found. Put {_HTML_NAME} next to touchup.py "
                "or set the PLOTLY_TOUCHUP_HTML environment variable."
            )
        http.server.ThreadingHTTPServer.daemon_threads = True
        try:
            srv = http.server.ThreadingHTTPServer(
                ("127.0.0.1", port), _Handler
            )
        except OSError:  # preferred port busy -> any free port
            srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        _tmpdir = Path(tempfile.mkdtemp(prefix="plotly_touchup_"))
        threading.Thread(
            target=srv.serve_forever, name="plotly-touchup", daemon=True
        ).start()
        _server = srv
        atexit.register(stop_server)
        return srv


def stop_server() -> None:
    """Stop the background server and delete the temp figure files."""
    global _server, _tmpdir
    with _lock:
        if _server is not None:
            _server.shutdown()
            _server.server_close()
            _server = None
        if _tmpdir is not None:
            shutil.rmtree(_tmpdir, ignore_errors=True)
            _tmpdir = None


def touchup(
    fig,
    name: str = "figure",
    *,
    port: int = DEFAULT_PORT,
    open_browser: bool = True,
    print_url: bool | None = None,
) -> str:
    """Open `fig` (a plotly Figure or figure dict) in Plotly Touchup.

    The figure is written to a temp JSON file and referenced via ``?src=`` in
    the URL.  Returns the URL.

    name          Used for exported file names in the app.
    port          Preferred local port (falls back to a free one if busy).
                  Keep it fixed if you use an SSH port forward.
    open_browser  Set False to only print/return the URL.
    print_url     Print the URL (and SSH hint). Default: True over SSH or if
                  no browser could be opened.
    """
    srv = _ensure_server(port)
    actual_port = srv.server_address[1]

    slug = re.sub(r"[^A-Za-z0-9_-]+", "_", name).strip("_") or "figure"
    fname = f"{slug}-{uuid.uuid4().hex[:8]}.json"
    (_tmpdir / fname).write_text(pio.to_json(fig), encoding="utf-8")  # type: ignore

    query = urllib.parse.urlencode({"src": f"figs/{fname}", "name": name})
    url = f"http://localhost:{actual_port}/{_HTML_NAME}?{query}"

    ssh = _in_ssh()
    opened = False
    if open_browser:
        # Over SSH only trust an explicit $BROWSER (set by VS Code Remote etc.);
        # otherwise webbrowser could start a text browser like lynx/w3m in the
        # terminal, or a browser on the remote machine's display.
        if not ssh or os.environ.get("BROWSER"):
            try:
                opened = webbrowser.open(url)
            except webbrowser.Error:
                opened = False

    if print_url is None:
        print_url = ssh or not opened
    if print_url:
        print(f"Plotly Touchup: {url}")
        if ssh and not opened:
            host = socket.getfqdn()
            print(
                "Not on a local desktop. On your laptop, forward the port and open the URL above:\n"
                f"  ssh -L {actual_port}:localhost:{actual_port} {getpass.getuser()}@{host}"
            )
    return url
