"""Functions for modifying plot layouts."""

import stern_plot.theme as theme


def add_plot_notes(fig, note, x=0, y="auto"):
    """Add note to bottome left of figure."""
    if isinstance(note, list):
        note = "<br>".join(note)
    if y == "auto":
        y = -0.15 - 0.05 * note.count("<br>")

    text_colour = fig.layout.template.layout.font.color
    fig.add_annotation(
        dict(
            x=x,
            y=y,
            xref="x domain",
            yref="y domain",
            text=note,
            showarrow=False,
            font=dict(size=12, color=text_colour),
            align="left",
        )
    )
    return fig


def inset_legend_layout(x=0.02, y=0.99):
    """Get legend layout to inset legend in plot."""
    return dict(
        yanchor="top",
        y=y,
        xanchor="left",
        x=x,
        bordercolor=theme.site_colour["dark_grey"],
        borderwidth=2,
    )
