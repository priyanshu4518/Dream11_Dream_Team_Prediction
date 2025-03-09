import numpy as np
import pandas as pd
import streamlit as st
import dill
import os

# Load DataFrame and models
dt = pd.read_csv("combined_data2.csv")
with open("reason.pkl", "rb") as f:
    reason = dill.load(f)
with open("proceed.pkl", "rb") as f:
    proceed = dill.load(f)

st.title("Dream Team Preddiction For ODI Mens (model is trained until 2022/06/08)")

# --- Team Selection Section ---
all_teams = set(dt['team1']).union(set(dt['team2']))
all_teams = sorted(all_teams)

selected_team1 = st.selectbox("Select Team 1", options=all_teams, index=0)

mask_team1 = (dt['team1'] == selected_team1) | (dt['team2'] == selected_team1)
possible_opponents = set()
for idx, row in dt[mask_team1].iterrows():
    if row['team1'] == selected_team1:
        possible_opponents.add(row['team2'])
    else:
        possible_opponents.add(row['team1'])
possible_opponents = sorted(possible_opponents)

selected_team2 = st.selectbox("Select Team 2", options=possible_opponents)

mask_match = (
    ((dt['team1'] == selected_team1) & (dt['team2'] == selected_team2)) |
    ((dt['team1'] == selected_team2) & (dt['team2'] == selected_team1))
)
match_dates = dt[mask_match]['date'].unique()
match_dates = sorted(match_dates)

selected_date = st.selectbox("Select Date", options=match_dates)

# --- Predict and Detailed Information Section ---
if st.button("Predict"):
    # Retrieve the file_path for the selected match
    mask_final = mask_match & (dt['date'] == selected_date)
    if dt[mask_final].empty:
        st.error("No match found for the selected combination.")
    else:
        selected_path = dt[mask_final].iloc[0]['file_path']
        # Normalize Windows path to Unix-style
        selected_path_norm = os.path.normpath(selected_path).replace("\\", "/")
        file_id = os.path.splitext(os.path.basename(selected_path_norm))[0]
        # Optional: update selected_path as well if needed
        selected_path = selected_path.replace("\\", "/")
        
        # Call your functions
        y, x = proceed(selected_path)
        reason_player = reason(x, y, file_id)
        
        # Combine all details with an empty line between each
        all_details = "\n\n".join(reason_player)
        
        # Display the combined details in a scrollable text area
        st.text_area("Player and Reason For Selecting Player In Dream Team", all_details, height=300)
