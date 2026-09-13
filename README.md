# Exploratory Data Analysis (EDA) Web Application

A Streamlit web app that generates an automated exploratory data analysis report for any CSV file you upload, powered by [ydata-profiling](https://github.com/ydataai/ydata-profiling) (formerly pandas-profiling).

Live app: https://exploratory-data-analysis-report-app-o8xxdrdwkg2w48wef6egb4.streamlit.app

## Features

- Upload any `.csv` file (up to 200MB) from the sidebar
- Or load a dataset directly from an online URL (paste a link and click "Load dataset from URL")
  - GitHub file links are auto-handled: paste a normal `github.com/.../blob/...` URL and the app converts it to the raw file link automatically
  - For other sources, make sure the URL points directly to the raw CSV file, not an HTML viewer/preview page
- Or try it instantly with the built-in Titanic example dataset
- View the raw dataframe before the report
- Auto-generated profiling report including:
  - Per-column summary statistics and distributions
  - Correlations (Pearson, Spearman, and others)
  - Interactions (pairwise relationships between columns)
  - Missing value bar chart and matrix
  - Duplicate row detection
  - Sample rows (head/tail)

## Tech Stack

- [Streamlit](https://streamlit.io/) — web app framework
- [pandas](https://pandas.pydata.org/) — data loading and manipulation
- [ydata-profiling](https://github.com/ydataai/ydata-profiling) — automated report generation
- [seaborn](https://seaborn.pydata.org/) — provides the built-in example dataset

## Getting Started

### Prerequisites

- Python 3.10 to 3.13
- pip

### Installation

```bash
git clone <https://github.com/dawoodofficial04/streamlit-eda-report-app.git>
cd <streamlit-eda-report-app>
pip install -r requirements.txt
```

### Run locally

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Usage

1. Choose one of three ways to provide data:
   - Upload a CSV file using the sidebar uploader
   - Paste a URL to an online CSV file and click "Load dataset from URL"
   - Click "Press to use Example Dataset" to try it with the Titanic dataset
2. Wait for the report to generate — this can take anywhere from a few seconds to a couple of minutes depending on the size of your data.
3. Scroll through the input dataframe and the generated report below it.

## Deployment

This app is deployed on [Streamlit Community Cloud](https://streamlit.io/cloud). To deploy your own copy:

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), connect your repo, and point it at `app.py`.
3. Go to `Advanced Settings` and select `Python 3.10 to 3.13` because ydata-profiling works on these Python versions.
4. Streamlit Cloud will install everything in `requirements.txt` automatically.

## Notes on Report Configuration

Streamlit Community Cloud's free tier has limited memory (~1GB). Running `ProfileReport` with all features enabled (`explorative=True`) gives the most complete report — correlations, interactions, missing value diagrams, duplicates, etc. — but is also the most memory/CPU intensive, and can be slow or fail to render on large or wide datasets.

This project currently uses `explorative=True` in `generate_report()` for the fullest possible report. If you run into slowness, hangs, or crashes on larger datasets, swap in this lighter configuration instead:

```python
return ProfileReport(
    df,
    title='Pandas Profiling Report',
    correlations={
        "auto": {"calculate": True},
        "pearson": {"calculate": True},
        "spearman": {"calculate": True},
        "kendall": {"calculate": False},
        "phi_k": {"calculate": False},
        "cramers": {"calculate": False},
    },
    interactions=None,  # disables the O(n^2) pairwise scatter plots — the biggest memory cost
    missing_diagrams={"bar": True, "matrix": True, "heatmap": False, "dendrogram": False},
    samples={"head": 5, "tail": 5},
    duplicates=None,
)
```

The report is rendered using Streamlit's built-in `st.components.v1.html()` rather than the third-party `streamlit-ydata-profiling` package, which can silently fail to render on newer Streamlit versions due to its custom-component JS bridge going out of sync.

## Loading Data from a URL

The sidebar "Load from a URL" field accepts a direct link to a CSV file. A few notes:

- **GitHub links**: pasting a normal file page link (e.g. `https://github.com/<user>/<repo>/blob/<branch>/data.csv`) works out of the box — the app automatically rewrites it to the corresponding `raw.githubusercontent.com` URL before loading.
- **Other sources**: the URL must point directly to the raw CSV bytes, not an HTML page that displays or previews the file. If you get a tokenizing/parsing error, double-check you're not pointing at a viewer page.
- The loaded dataset is cached by URL and persists across reruns (e.g. when interacting with checkboxes inside the report) until you upload a file or refresh the page.

## Known Limitations

- Very large CSV files (tens of thousands of rows or hundreds of columns) may be slow or resource-intensive to profile, especially with `explorative=True`. Switch to the lighter config above if this becomes an issue.
- URLs that require authentication, or that point to non-raw/preview pages (other than GitHub, which is auto-handled), will fail to load.

## Author

Developed by **Dawood Hussain**.

## License

Add your preferred license here (e.g., MIT).
