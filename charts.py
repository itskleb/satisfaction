"""Reusable Plotly chart builders, following the brand-adapted palette in theme.py."""

import pandas as pd
import plotly.graph_objects as go

import theme
from questions import QUESTIONS


def _apply_layout(fig, height=340, showlegend=True):
    fig.update_layout(
        **theme.PLOTLY_LAYOUT,
        height=height,
        showlegend=showlegend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(**theme.AXIS_STYLE)
    fig.update_yaxes(**theme.AXIS_STYLE)
    return fig


def likert_distribution_chart(series: pd.Series, scale_order: list, title: str) -> go.Figure:
    """Diverging 100%-stacked horizontal bar for a single 5-point Likert item."""
    counts = series.value_counts()
    total = counts.sum()
    pcts = [100.0 * counts.get(label, 0) / total if total else 0 for label in scale_order]

    fig = go.Figure()
    for i, label in enumerate(scale_order):
        fig.add_trace(
            go.Bar(
                y=[title],
                x=[pcts[i]],
                name=label,
                orientation="h",
                marker_color=theme.LIKERT_DIVERGING[i],
                text=[f"{pcts[i]:.0f}%" if pcts[i] >= 6 else ""],
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(color="white" if i in (0, 4) else theme.TEXT_PRIMARY, size=12),
                hovertemplate=f"{label}: %{{x:.1f}}%<extra></extra>",
            )
        )
    fig.update_layout(barmode="stack")
    fig.update_xaxes(title="Share of responses", ticksuffix="%", range=[0, 100])
    fig.update_yaxes(title=None)
    return _apply_layout(fig, height=180)


def scale_count_chart(series: pd.Series, scale_min: int, scale_max: int, axis_note: str = "") -> go.Figure:
    """Bar chart of raw counts across an integer scale (e.g. 1-10 or 1-5)."""
    values = list(range(scale_min, scale_max + 1))
    counts = series.value_counts()
    y = [int(counts.get(v, 0)) for v in values]

    fig = go.Figure(
        go.Bar(
            x=[str(v) for v in values],
            y=y,
            marker_color=theme.SINGLE_SERIES_HUE,
            text=y,
            textposition="outside",
            hovertemplate="Score %{x}: %{y} responses<extra></extra>",
        )
    )
    fig.update_xaxes(title=f"Score{(' — ' + axis_note) if axis_note else ''}")
    fig.update_yaxes(title="Responses")
    return _apply_layout(fig, height=320, showlegend=False)


def group_average_chart(labels: list, means: list, counts: list, value_range: tuple, min_n_flag: int = 5) -> go.Figure:
    """Horizontal bar of average score per group, sorted descending, with N labels.

    Groups below `min_n_flag` responses are drawn in the caution (gold) color
    instead of the primary hue, as a status flag - never a plain 4th series.
    """
    order = sorted(range(len(labels)), key=lambda i: (means[i] if means[i] == means[i] else -1))
    labels = [labels[i] for i in order]
    means = [means[i] for i in order]
    counts = [counts[i] for i in order]

    colors = [theme.STATUS_WARNING if c < min_n_flag else theme.SINGLE_SERIES_HUE for c in counts]
    text = [f"{m:.2f}  (n={c})" if m == m else f"n={c}" for m, c in zip(means, counts)]

    fig = go.Figure(
        go.Bar(
            y=labels,
            x=means,
            orientation="h",
            marker_color=colors,
            text=text,
            textposition="outside",
            hovertemplate="%{y}: %{x:.2f}<extra></extra>",
        )
    )
    lo, hi = value_range
    fig.update_xaxes(title="Average score", range=[lo, hi * 1.15])
    fig.update_yaxes(title=None)
    return _apply_layout(fig, height=max(220, 40 * len(labels)), showlegend=False)


def ab_compare_chart(question_labels: list, means_a: list, means_b: list, n_a: int, n_b: int, value_range: tuple) -> go.Figure:
    """Grouped bar comparing two subsets (Group A vs Group B) across questions."""
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name=f"Group A (n={n_a})",
            y=question_labels,
            x=means_a,
            orientation="h",
            marker_color=theme.COMPARE_A,
            text=[f"{v:.2f}" if v == v else "—" for v in means_a],
            textposition="outside",
            hovertemplate="%{y} — Group A: %{x:.2f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            name=f"Group B (n={n_b})",
            y=question_labels,
            x=means_b,
            orientation="h",
            marker_color=theme.COMPARE_B,
            text=[f"{v:.2f}" if v == v else "—" for v in means_b],
            textposition="outside",
            hovertemplate="%{y} — Group B: %{x:.2f}<extra></extra>",
        )
    )
    lo, hi = value_range
    fig.update_layout(barmode="group")
    fig.update_xaxes(title="Average score", range=[lo, hi * 1.15])
    fig.update_yaxes(title=None, autorange="reversed")
    return _apply_layout(fig, height=max(280, 55 * len(question_labels)), showlegend=True)


def scale_range_for(qid: str) -> tuple:
    qtype = QUESTIONS[qid]["type"]
    if qtype == "scale_10":
        return (1, 10)
    if qtype in ("likert_5", "scale_5_num"):
        return (1, 5)
    return (0, 0)
