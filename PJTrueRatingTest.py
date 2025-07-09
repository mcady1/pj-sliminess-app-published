import streamlit as st
import pandas as pd
import os
import sys

# Get the absolute directory of this script (or the .exe)
base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
csv_path = os.path.join(base_dir, "perverted_justice_ratings.csv")

# Load CSV
df = pd.read_csv(csv_path)

# Streamlit UI
st.title("Perverted Justice Sliminess Ratings")
name_query = st.text_input("Enter IM Name or keyword:")

if name_query:
    from difflib import get_close_matches
    lower_names = df["IM Name"].str.lower()
    substr_matches = df[lower_names.str.contains(name_query.lower())]

    if not substr_matches.empty:
        result = substr_matches.iloc[0]
    else:
        close = get_close_matches(name_query.lower(), lower_names.tolist(), n=1, cutoff=0.6)
        result = df[lower_names == close[0]].iloc[0] if close else None

    if result is not None:
        percentile = (df["Average Votes"] < result["Average Votes"]).mean() * 100
        st.success(f"{result['IM Name']} is slimier than {percentile:.2f}% of offenders (rating {result['Average Votes']:.2f})")
    else:
        st.warning("No match found.")
