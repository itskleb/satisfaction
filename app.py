"""
Scouting America Program Satisfaction Dashboard
-------------------------------------------------
A Streamlit dashboard for exploring survey responses and comparing satisfaction
across boroughs, districts, programs, units, and respondent characteristics
(tenure in the program, relationship to Scouting, and satisfaction level).

Run locally:    streamlit run app.py
"""

import numpy as np
import pandas as pd
import streamlit as st

import theme
from charts import (
    ab_compare_chart,
    group_average_chart,
    likert_distribution_chart,
    scale_count_chart,
    scale_range_for,
)
from data_utils import filter_options, load_data, mean_or_nan, numeric_column, question_choices
from questions import (
    CATEGORICAL_FILTERS,
    QUESTIONS,
    SATISFACTION_BAND_ORDER,
    TENURE_COLUMN,
    TENURE_ORDER,
    TEXT_QUESTIONS,
)

st.set_page_config(
    page_title="Scouting America | Program Satisfaction",
    page_icon="🏕️",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Global style
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {theme.SURFACE_LIGHT}; }}

    /* Default body text - Streamlit's own theme fades a lot of this to a
       low-contrast gray by default, so force it black everywhere except
       inside the dark green sidebar (handled separately below). */
    .stApp, .stApp p, .stApp span, .stApp label, .stApp div,
    .stMarkdown, .stCaption, [data-testid="stCaptionContainer"],
    .stMarkdown blockquote, .stMarkdown blockquote p,
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"],
    [data-testid="stWidgetLabel"] p,
    .stSelectbox, .stMultiSelect, .stDataFrame, .stTextInput,
    [data-baseweb="select"] * {{
        color: {theme.TEXT_PRIMARY} !important;
        opacity: 1 !important;
    }}

    [data-testid="stSidebar"] {{
        background-color: {theme.BRAND_GREEN};
    }}
    [data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
        opacity: 1 !important;
    }}
    /* Exception: text typed/shown inside the white dropdown boxes themselves
       needs to stay dark, or it becomes invisible on their white background. */
    [data-testid="stSidebar"] [data-baseweb="select"] * {{
        color: {theme.TEXT_PRIMARY} !important;
    }}
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {{
        background-color: {theme.BRAND_GOLD} !important;
    }}
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] * {{
        color: {theme.BRAND_GREEN} !important;
    }}
    h1, h2, h3 {{ color: {theme.BRAND_GREEN} !important; }}
    div[data-testid="stMetric"] {{
        background-color: white;
        border: 1px solid {theme.GRID_LINE};
        border-left: 4px solid {theme.BRAND_GREEN};
        border-radius: 6px;
        padding: 10px 14px;
    }}

    /* Top header bar */
    [data-testid="stHeader"] {{
        background-color: {theme.BRAND_BLUE} !important;
    }}
    [data-testid="stHeader"] button {{
        background-color: transparent !important;
    }}
    [data-testid="stHeader"] button span,
    [data-testid="stHeader"] button p,
    [data-testid="stHeader"] svg {{
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

df = load_data()

# ---------------------------------------------------------------------------
# Sidebar - global filters
# ---------------------------------------------------------------------------
st.sidebar.markdown("## 🏕️ Filters")
st.sidebar.caption("Filters apply to Overview, Question Explorer, and Open-Ended tabs.")

completed_only = st.sidebar.checkbox(
    "Completed responses only",
    value=False,
    help="Off by default so partial/in-progress responses are included in every count and chart.",
)

filtered = df.copy()
if completed_only and "Finished" in filtered.columns:
    filtered = filtered[filtered["Finished"] == 1]

st.sidebar.markdown("#### Embedded Data")
for col, display in CATEGORICAL_FILTERS.items():
    if col not in filtered.columns:
        continue
    opts = filter_options(df, col)
    chosen = st.sidebar.multiselect(display, opts, default=[], key=f"filt_{col}")
    if chosen:
        filtered = filtered[filtered[col].isin(chosen)]

st.sidebar.markdown("#### Respondent Experience")
tenure_opts = [t for t in TENURE_ORDER if t in df[TENURE_COLUMN].dropna().unique()]
chosen_tenure = st.sidebar.multiselect("Time in the Program", tenure_opts, default=[])
if chosen_tenure:
    filtered = filtered[filtered[TENURE_COLUMN].isin(chosen_tenure)]

sat_opts = [s for s in SATISFACTION_BAND_ORDER if s in df["Satisfaction Level"].dropna().unique()]
chosen_sat = st.sidebar.multiselect("Satisfaction Level (Overall)", sat_opts, default=[])
if chosen_sat:
    filtered = filtered[filtered["Satisfaction Level"].isin(chosen_sat)]

st.sidebar.markdown("---")
st.sidebar.metric("Responses in current filter", len(filtered))
if st.sidebar.button("Reset all filters"):
    st.rerun()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("Program Satisfaction Dashboard")
st.caption("Scouting America — Council survey results")

tab_overview, tab_explore, tab_compare, tab_ab, tab_text = st.tabs(
    ["Overview", "Question Explorer", "Compare Groups", "A/B Subset Compare", "Open-Ended Responses"]
)

# ---------------------------------------------------------------------------
# Overview tab
# ---------------------------------------------------------------------------
with tab_overview:
    if filtered.empty:
        st.warning("No responses match the current filters.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Responses", len(filtered))
        c2.metric("Avg. Overall Satisfaction", f"{mean_or_nan(filtered['Q7_1']):.1f} / 10")
        c3.metric("Avg. Likelihood to Recommend", f"{mean_or_nan(filtered['Q8_1']):.1f} / 10")
        c4.metric("Avg. Likely to Re-register", f"{mean_or_nan(filtered['Q18_1']):.1f} / 5")

        st.markdown("#### Headline Ratings")
        col_a, col_b, col_c = st.columns(3)
        for col, qid in zip((col_a, col_b, col_c), ("Q7_1", "Q8_1", "Q9_1")):
            with col:
                st.markdown(f"**{QUESTIONS[qid]['label']}**")
                fig = scale_count_chart(filtered[qid], 1, 10)
                st.plotly_chart(fig, use_container_width=True, key=f"ov_{qid}")

        st.markdown("#### Satisfaction with Program Aspects")
        aspect_qids = [q for q, m in QUESTIONS.items() if m["group"] == "Program Aspects"]
        for qid in aspect_qids:
            meta = QUESTIONS[qid]
            fig = likert_distribution_chart(filtered[qid], meta["scale_order"], meta["label"])
            st.plotly_chart(fig, use_container_width=True, key=f"ov_likert_{qid}")

# ---------------------------------------------------------------------------
# Question Explorer tab
# ---------------------------------------------------------------------------
with tab_explore:
    st.markdown("Pick any survey question to see its distribution for the currently filtered responses.")
    groups = question_choices()
    group_name = st.selectbox("Question group", list(groups.keys()))
    qid_label_pairs = groups[group_name]
    qid = st.selectbox(
        "Question",
        [q for q, _ in qid_label_pairs],
        format_func=lambda q: QUESTIONS[q]["label"],
    )
    meta = QUESTIONS[qid]
    st.caption(meta["text"])

    if filtered.empty:
        st.warning("No responses match the current filters.")
    else:
        series = filtered[qid]
        n_valid = series.notna().sum()
        st.write(f"**n = {n_valid}** valid responses")

        if meta["type"] == "likert_5":
            fig = likert_distribution_chart(series, meta["scale_order"], meta["label"])
            st.plotly_chart(fig, use_container_width=True)
        elif meta["type"] == "scale_10":
            fig = scale_count_chart(series, 1, 10)
            st.plotly_chart(fig, use_container_width=True)
            st.metric("Average", f"{mean_or_nan(series):.2f} / 10")
        elif meta["type"] == "scale_5_num":
            fig = scale_count_chart(series, 1, 5, axis_note="1 = low, 5 = high; no text labels captured for this item")
            st.plotly_chart(fig, use_container_width=True)
            st.metric("Average", f"{mean_or_nan(series):.2f} / 5")

# ---------------------------------------------------------------------------
# Compare Groups tab
# ---------------------------------------------------------------------------
with tab_compare:
    st.markdown("Split the currently filtered responses by a dimension and compare average scores across groups.")

    split_options = {**CATEGORICAL_FILTERS, TENURE_COLUMN: "Time in the Program", "Satisfaction Level": "Satisfaction Level (Overall)"}
    split_col = st.selectbox(
        "Split by",
        list(split_options.keys()),
        format_func=lambda c: split_options[c],
    )

    groups = question_choices()
    group_name2 = st.selectbox("Question group ", list(groups.keys()), key="cmp_group")
    qid = st.selectbox(
        "Question ",
        [q for q, _ in groups[group_name2]],
        format_func=lambda q: QUESTIONS[q]["label"],
        key="cmp_qid",
    )
    min_n = st.slider("Flag groups with fewer than N responses", 1, 20, 5)

    if filtered.empty:
        st.warning("No responses match the current filters.")
    else:
        value_col = numeric_column(qid)
        work = filtered[[split_col, value_col]].dropna(subset=[split_col])
        summary = work.groupby(split_col)[value_col].agg(["mean", "count"]).reset_index()
        if summary.empty:
            st.info("No data available for this combination.")
        else:
            fig = group_average_chart(
                summary[split_col].tolist(),
                summary["mean"].tolist(),
                summary["count"].tolist(),
                scale_range_for(qid),
                min_n_flag=min_n,
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Gold bars indicate groups below the response-count threshold — interpret with caution.")
            st.dataframe(
                summary.rename(columns={split_col: split_options.get(split_col, split_col), "mean": "Average", "count": "N"}),
                use_container_width=True,
                hide_index=True,
            )

# ---------------------------------------------------------------------------
# A/B Subset Compare tab
# ---------------------------------------------------------------------------
with tab_ab:
    st.markdown("Build two independent subsets from the full dataset (ignoring the sidebar) and compare them directly.")

    show_filters = st.checkbox("Show group filters", value=True, key="ab_show_filters")

    all_filter_cols = {**CATEGORICAL_FILTERS, TENURE_COLUMN: "Time in the Program", "Satisfaction Level": "Satisfaction Level (Overall)"}

    def build_subset(prefix: str, default_name: str):
        name = st.text_input(f"Group {prefix} name", value=default_name, key=f"ab_name_{prefix}")
        subset = df.copy()
        if show_filters:
            for col, display in all_filter_cols.items():
                if col not in subset.columns:
                    continue
                opts = sorted(v for v in df[col].dropna().unique().tolist())
                chosen = st.multiselect(display, opts, default=[], key=f"ab_{prefix}_{col}")
                if chosen:
                    subset = subset[subset[col].isin(chosen)]
        else:
            # Filters are hidden, but keep whatever was already chosen in effect.
            for col in all_filter_cols:
                if col not in subset.columns:
                    continue
                chosen = st.session_state.get(f"ab_{prefix}_{col}", [])
                if chosen:
                    subset = subset[subset[col].isin(chosen)]
        return subset, name

    col_left, col_right = st.columns(2)
    with col_left:
        subset_a, name_a = build_subset("A", "Group A")
    with col_right:
        subset_b, name_b = build_subset("B", "Group B")

    st.markdown("---")
    group_name3 = st.selectbox("Question group", list(question_choices().keys()), key="ab_group")
    qids = st.multiselect(
        "Questions to compare",
        [q for q, _ in question_choices()[group_name3]],
        default=[q for q, _ in question_choices()[group_name3]][:3],
        format_func=lambda q: QUESTIONS[q]["label"],
        key="ab_qids",
    )

    if not qids:
        st.info("Pick at least one question above.")
    elif subset_a.empty or subset_b.empty:
        st.warning("One or both groups have no matching responses.")
    else:
        # All chosen questions must share a scale type/range for one chart.
        ranges = {scale_range_for(q) for q in qids}
        if len(ranges) > 1:
            st.warning("Selected questions use different scales — pick questions from a single scale for a fair comparison.")
        else:
            labels = [QUESTIONS[q]["label"] for q in qids]
            means_a = [mean_or_nan(subset_a[numeric_column(q)]) for q in qids]
            means_b = [mean_or_nan(subset_b[numeric_column(q)]) for q in qids]
            fig = ab_compare_chart(
                labels, means_a, means_b, len(subset_a), len(subset_b), ranges.pop(),
                name_a=name_a or "Group A", name_b=name_b or "Group B",
            )
            st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Open-Ended Responses tab
# ---------------------------------------------------------------------------
with tab_text:
    st.markdown("Browse free-text responses for the currently filtered set (sidebar filters apply).")
    text_qid = st.selectbox(
        "Question",
        list(TEXT_QUESTIONS.keys()),
        format_func=lambda q: TEXT_QUESTIONS[q],
    )
    search = st.text_input("Search text (optional)")

    if filtered.empty:
        st.warning("No responses match the current filters.")
    else:
        texts = filtered[[text_qid, "Boro", "Program", "District"]].dropna(subset=[text_qid])
        if search:
            texts = texts[texts[text_qid].str.contains(search, case=False, na=False)]
        st.write(f"**{len(texts)}** responses")
        for _, row in texts.iterrows():
            st.markdown(
                f"> {row[text_qid]}\n\n"
                f"<span style='color:{theme.TEXT_MUTED}; font-size:0.85em;'>"
                f"{row['Program']} · {row['Boro']} · {row['District']}</span>",
                unsafe_allow_html=True,
            )
            st.markdown("---")
