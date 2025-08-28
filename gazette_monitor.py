import streamlit as st
import requests
from bs4 import BeautifulSoup
import difflib
import os
from datetime import datetime

# Constants
URL = "https://governmentgazette.sa.gov.au/"
SNAPSHOT_DIR = "gazette_snapshots"
CURRENT_SNAPSHOT = os.path.join(SNAPSHOT_DIR, "current.html")
PREVIOUS_SNAPSHOT = os.path.join(SNAPSHOT_DIR, "previous.html")

# Ensure snapshot directory exists
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# Fetch HTML content
def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

# Extract file links from HTML
def extract_file_links(html):
    soup = BeautifulSoup(html, "html.parser")
    return sorted(set(a['href'] for a in soup.find_all("a", href=True)))

# Save HTML snapshot
def save_snapshot(content, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# Load HTML snapshot
def load_snapshot(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# Load previous snapshot
previous_html = load_snapshot(CURRENT_SNAPSHOT)
if previous_html:
    save_snapshot(previous_html, PREVIOUS_SNAPSHOT)

# Fetch current snapshot
try:
    current_html = fetch_html(URL)
    save_snapshot(current_html, CURRENT_SNAPSHOT)
except Exception as e:
    st.error(f"Error fetching the website: {e}")
    st.stop()

# Extract and compare links
previous_links = extract_file_links(previous_html)
current_links = extract_file_links(current_html)

new_links = [link for link in current_links if link not in previous_links]
removed_links = [link for link in previous_links if link not in current_links]

# Streamlit UI
st.title("📰 Government Gazette Monitor")
st.subheader("🔗 File Change Summary")

if new_links:
    st.markdown("**New Files Added:**")
    for link in new_links:
        st.markdown(f"- 📄 {link}")
else:
    st.markdown("No new files added.")

if removed_links:
    st.markdown("**Removed Files:**")
    for link in removed_links:
        st.markdown(f"- ~~{link}~~")
else:
    st.markdown("No files removed.")

# Visual HTML comparison
st.subheader("🏛️ Visual HTML Comparison")
diff = difflib.HtmlDiff().make_file(
    previous_html.splitlines(),
    current_html.splitlines(),
    fromdesc="Last Snapshot",
    todesc="Current Snapshot"
)
st.components.v1.html(diff, height=600, scrolling=True)
