# Scouting America — Program Satisfaction Dashboard

A Streamlit dashboard for exploring the council's Program Satisfaction Survey
results: view any question's distribution, filter by borough / district /
program / unit / demographics, and compare satisfaction across subsets
(e.g. "New members" vs. "5+ years", or "Manhattan" vs. "Queens").

## Features

- **Overview** — headline KPI tiles and satisfaction-aspect charts for the
  currently filtered responses.
- **Question Explorer** — pick any question and see its distribution
  (diverging Likert charts for 5-point items, bar counts for 1-10 scales).
- **Compare Groups** — split the filtered dataset by any dimension (borough,
  program, tenure, satisfaction level, etc.) and compare average scores.
- **A/B Subset Compare** — build two independent, arbitrary subsets (e.g.
  "Cub Scouts in Queens" vs. "Scouts BSA in Brooklyn") and compare them
  side by side, ignoring the sidebar filters.
- **Open-Ended Responses** — browse and search free-text answers.

Filters are available for both **embedded survey data** (Borough, District,
Program, Unit, Gender, Registration Status, Demographic Group, Relationship
to Scouting) and **derived respondent-experience fields** (Time in the
Program, Satisfaction Level based on the overall satisfaction question).

## Data

`survey_responses.csv` (in the same folder as `app.py`) is the exported
survey data with Qualtrics' value labels applied (so categorical answers
like tenure and Likert ratings appear as readable text, not numeric codes).
To refresh with a new export:

1. In Qualtrics, export results as CSV with **"Use choice text"** enabled
   (not numeric values), and download the version **with** the two extra
   header rows Qualtrics adds.
2. Replace `survey_responses.csv` with a version where those two header
   rows are stripped, keeping only the first row (the `Q#` column names) as
   the header. You can do this in Python:

   ```python
   import pandas as pd
   df = pd.read_csv("your_export.csv", skiprows=[1, 2])
   df.to_csv("survey_responses.csv", index=False)
   ```

3. If new questions are added to the survey, update `questions.py` with
   their column IDs, labels, and scale type.

**Note on privacy:** this survey export includes respondent email addresses
and member IDs. Only host this repository somewhere access is restricted to
people who should see that information (e.g. a private GitHub repo), and
never make the repo public without stripping those columns first.

## Running locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens at http://localhost:8501.

## Deploying from GitHub (Streamlit Community Cloud)

1. Push this folder to a GitHub repository (private is recommended — see the
   privacy note above).
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with
   GitHub, and click **"New app"**.
3. Select your repository, branch, and set the main file path to `app.py`.
4. Click **Deploy**. Streamlit Cloud will install `requirements.txt`
   automatically and give you a shareable URL.

To update the live app later, just push new commits to the connected
branch — Streamlit Cloud redeploys automatically.

## Project structure

```
scouting-dashboard/
├── app.py                 # Main Streamlit app (sidebar filters + tabs)
├── charts.py               # Reusable Plotly chart builders
├── theme.py                # Brand color palette (chart-safe + UI chrome)
├── questions.py             # Question metadata: labels, scale types, groups
├── data_utils.py            # Data loading & aggregation helpers
├── survey_responses.csv     # Survey data (same folder as app.py)
├── .streamlit/
│   └── config.toml          # Streamlit theme colors
├── requirements.txt
└── README.md
```

Everything the app needs (code + data) lives flat in this one folder plus
the `.streamlit/` theme subfolder that Streamlit itself expects — there are
no other nested data folders, so pushing this directory as-is to GitHub and
pointing Streamlit Cloud at `app.py` works without any path adjustments.

## Color scheme

Colors are adapted from Scouting America's official brand guidelines (forest
green, gold, and red). Brand hex codes are used for UI chrome (sidebar,
headers); chart data marks use lightness/saturation-adjusted versions of the
same hues so they remain colorblind-safe and readable against a white
background. See the top of `theme.py` for the exact values and rationale.
