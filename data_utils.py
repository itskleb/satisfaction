"""Data loading and shared aggregation helpers for the dashboard."""

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

from questions import (
    CATEGORICAL_FILTERS,
    QUESTIONS,
    SATISFACTION_SOURCE_COLUMN,
    TENURE_COLUMN,
    TEXT_QUESTIONS,
    satisfaction_band,
)

DATA_PATH = Path(__file__).parent / "survey_responses.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)

    # Numeric coercion only for columns that are actually numeric scales.
    # Likert-5 columns already contain their text labels (e.g. "Extremely
    # satisfied") in this export and must stay as strings for the
    # distribution charts - a parallel "<qid>__num" column is added below
    # for averaging/comparison purposes.
    for qid, meta in QUESTIONS.items():
        if qid in df.columns and meta["type"] in ("scale_10", "scale_5_num"):
            df[qid] = pd.to_numeric(df[qid], errors="coerce")
        if qid in df.columns and meta["type"] == "likert_5":
            order_map = {label: i + 1 for i, label in enumerate(meta["scale_order"])}
            df[f"{qid}__num"] = df[qid].map(order_map)

    # Derived filter: satisfaction band, from the overall satisfaction score.
    df["Satisfaction Level"] = df[SATISFACTION_SOURCE_COLUMN].apply(satisfaction_band)

    # Treat "Finished" as a clean 0/1 flag.
    if "Finished" in df.columns:
        df["Finished"] = pd.to_numeric(df["Finished"], errors="coerce").fillna(0).astype(int)

    return df


def filter_options(df: pd.DataFrame, column: str) -> list:
    """Sorted, non-null unique values for a plain categorical column."""
    return sorted(v for v in df[column].dropna().unique().tolist())


def question_choices() -> dict:
    """Group -> list of (qid, label) for the question picker, in group order."""
    groups: dict = {}
    for qid, meta in QUESTIONS.items():
        groups.setdefault(meta["group"], []).append((qid, meta["label"]))
    return groups


def numeric_column(qid: str) -> str:
    """Column name to use for averaging/aggregation for a given question."""
    if QUESTIONS[qid]["type"] == "likert_5":
        return f"{qid}__num"
    return qid


def n_label(n: int) -> str:
    return f"n = {n}"


def mean_or_nan(series: pd.Series):
    s = series.dropna()
    if len(s) == 0:
        return np.nan
    return s.mean()


def top_box_pct(series: pd.Series, top_values: set) -> float:
    """Percent of non-null responses in the given top-box value set."""
    s = series.dropna()
    if len(s) == 0:
        return np.nan
    return 100.0 * s.isin(top_values).sum() / len(s)
