import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from ydata_profiling import ProfileReport

st.set_page_config(page_title="EDA App", layout="wide")

# App title
st.markdown('''
# **Exploratory Data Analysis Web Application**
This app is developed by Dawood Hussain called **EDA App**.
            ''')

# Upload a file from pc, or load one from a URL
with st.sidebar.header("Upload your dataset (.csv)"):
    uploaded_file = st.sidebar.file_uploader("Upload your file", type=['csv'])
    st.sidebar.markdown("**OR**")
    csv_url = st.sidebar.text_input("Load from a URL", placeholder="https://example.com/data.csv")
    load_url_clicked = st.sidebar.button("Load dataset from URL")


# Cache keyed on the actual uploaded file so switching files works correctly
@st.cache_data
def load_csv(file):
    return pd.read_csv(file)


# Cache keyed on the URL string
@st.cache_data
def load_csv_from_url(url):
    return pd.read_csv(url)


# Cache keyed on the dataframe itself, avoids recomputing on every rerun
@st.cache_resource(show_spinner=False)
def generate_report(df):
    # Full explorative report: includes correlations, interactions, missing
    # value diagrams, duplicates, etc. This is the most complete report but
    # is also the most memory/CPU intensive — on constrained hosting (e.g.
    # Streamlit Community Cloud's free tier) this can be slow or fail on
    # large/wide datasets. If that happens, swap back to the lighter config
    # (correlations on, interactions off) described in README.md.
    return ProfileReport(df, title='Pandas Profiling Report', explorative=True)


def show_report(df):
    st.header('**Input DataFrame**')
    st.write(df)
    st.write('---')
    st.header('**Pandas Profiling Report**')
    try:
        with st.spinner('Generating profiling report, this can take a moment...'):
            pr = generate_report(df)

        with st.spinner('Rendering report...'):
            html = pr.to_html()

        # Render via Streamlit's built-in HTML component instead of the
        # third-party streamlit-ydata-profiling widget, which can silently
        # hang if its JS bridge is out of sync with newer Streamlit versions.
        st.components.v1.html(html, height=1200, scrolling=True)
    except Exception as e:
        st.error(f"Failed to generate the profiling report: {e}")
        st.exception(e)


if uploaded_file is not None:
    df = load_csv(uploaded_file)
    st.session_state.pop("url_df", None)
    show_report(df)
else:
    if load_url_clicked and csv_url:
        try:
            with st.spinner('Downloading dataset from URL...'):
                st.session_state["url_df"] = load_csv_from_url(csv_url)
        except Exception as e:
            st.session_state.pop("url_df", None)
            st.error(f"Could not load a CSV from that URL: {e}")

    if "url_df" in st.session_state:
        show_report(st.session_state["url_df"])
    else:
        st.info('Awaiting for CSV file to be uploaded.')
        if st.button('Press to use Example Dataset'):
            df = sns.load_dataset('titanic')
            show_report(df)