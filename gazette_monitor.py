import streamlit as st
import requests
import difflib
import os
from datetime import datetime
from bs4 import BeautifulSoup

# Define the URL to monitor
URL = "https://governmentgazette.sa.gov.au/"
DATA_DIR = "gazette_snapshots"
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_page_content():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        return None

def save_snapshot(content, filename):
    with open(os.path.join(DATA_DIR, filename), "w", encoding="utf-8") as f:
        f.write(content)

def load_snapshot(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None

def summarize_changes(old, new):
    diff = difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm="")
    changes = [line for line in diff if line.startswith("+ ") or line.startswith("- ")]
    if changes:
        return f"There have been updates to the Government Gazette page since last Thursday. Notable changes include {len(changes)} lines of content added or removed."
    else:
        return "No significant changes detected on the Government Gazette page since last Thursday."

# Streamlit UI
st.title("Government Gazette Monitor")
st.write("This app monitors changes on the Government Gazette website and summarizes updates weekly.")

today = datetime.now().strftime("%Y-%m-%d")
current_snapshot = fetch_page_content()

if current_snapshot:
    save_snapshot(current_snapshot, f"{today}.html")

    # Find the most recent previous snapshot
    snapshots = sorted([f for f in os.listdir(DATA_DIR) if f.endswith(".html")])
    if len(snapshots) >= 2:
        previous_snapshot_file = snapshots[-2]
        previous_snapshot = load_snapshot(previous_snapshot_file)
        summary = summarize_changes(previous_snapshot, current_snapshot)
        st.subheader("Summary of Changes")
        st.write(summary)
    else:
        st.write("Not enough historical data to compare changes yet. Please check back next week.")
else:
    st.error("Failed to fetch the Government Gazette website.")
