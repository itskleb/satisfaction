"""
Scouting America brand palette, adapted for chart use.

The raw brand hex codes (from Scouting America's official brand guidelines)
are used for UI chrome (headers, nav, accents). For chart *data marks* they
are re-stepped in lightness/chroma so they read reliably as data - this
follows the standard "snap to passing" approach: same hues, adjusted just
enough to clear a colorblind-safety and contrast validator.

Raw brand hex (source: Scouting America Official Brand Colors and Typefaces,
scouting.org brand identity guide):
    Scouting America Red     #CE1126
    Scouts BSA Olive (green) #243E2C
    Cub Scouts/Venturing Gold #FCD116

Chart-safe derivatives (validated: lightness band, chroma floor, CVD
separation >= 15 dE normal-vision, contrast vs white surface):
    Green (positive / primary):  #2E7D46
    Gold  (neutral / caution):   #C9A227
    Red   (negative / critical): #C8102E
"""

# Brand chrome (headers, sidebar, nav) - true brand hex.
BRAND_RED = "#CE1126"
BRAND_GREEN = "#243E2C"
BRAND_GOLD = "#FCD116"
BRAND_CREAM = "#FCFCFB"

# Chart-safe categorical trio (fixed order - never re-cycle).
CHART_GREEN = "#2E7D46"   # positive / satisfied / high
CHART_GOLD = "#C9A227"    # neutral / caution
CHART_RED = "#C8102E"     # negative / dissatisfied / low

# Single-hue bars for "average score by group" charts (identity is the group
# label on the axis, not the color - so one consistent hue is used, per the
# "nominal categorical -> same slot-1 hue" rule).
SINGLE_SERIES_HUE = CHART_GREEN

# Two-series comparison (Group A vs Group B in the custom compare tab).
COMPARE_A = CHART_GREEN
COMPARE_B = CHART_GOLD

# Status colors for flagging low-N or low-score groups (reserved meaning -
# never reused as a plain series color).
STATUS_GOOD = CHART_GREEN
STATUS_WARNING = CHART_GOLD
STATUS_CRITICAL = CHART_RED

# Diverging 5-step ramp for Likert charts (dissatisfied <-> satisfied /
# disagree <-> agree). Equal steps per arm around a neutral midpoint.
LIKERT_DIVERGING = {
    0: "#B0132E",  # Extremely dissatisfied / Strongly disagree
    1: "#E2909D",  # Somewhat dissatisfied / Somewhat disagree
    2: "#D9D5C9",  # Neutral
    3: "#8FC7A0",  # Somewhat satisfied / Somewhat agree
    4: "#2E7D46",  # Extremely satisfied / Strongly agree
}

SURFACE_LIGHT = "#FCFCFB"
TEXT_PRIMARY = "#1F2421"
TEXT_MUTED = "#5B6660"
GRID_LINE = "#E4E2DB"

PLOTLY_LAYOUT = dict(
    paper_bgcolor=SURFACE_LIGHT,
    plot_bgcolor=SURFACE_LIGHT,
    font=dict(family="Inter, -apple-system, Segoe UI, sans-serif", color=TEXT_PRIMARY, size=13),
    margin=dict(l=10, r=10, t=40, b=10),
)

AXIS_STYLE = dict(
    gridcolor=GRID_LINE,
    zerolinecolor=GRID_LINE,
    linecolor=GRID_LINE,
)
