import streamlit as st

st.title("📅 Gazette Issue Comparison")

st.markdown("Compare this week's Gazette issue with last week's:")

st.image(
    ["gazette_images/2025-08-21.png", "gazette_images/2025-08-28.png"],
    caption=["Last Thursday (2025-08-21)", "Today (2025-08-28)"],
    width=600
)
