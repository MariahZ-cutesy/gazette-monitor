import streamlit as st
from PIL import Image

st.title("📅 Government Gazette Visual Comparison")

# Load images
last_week = Image.open("screenshots/gazette_2025-08-21.png")
this_week = Image.open("screenshots/gazette_2025-08-28.png")

# Display side-by-side
col1, col2 = st.columns(2)
with col1:
    st.subheader("Last Week")
    st.image(last_week, use_column_width=True)
with col2:
    st.subheader("This Week")
    st.image(this_week, use_column_width=True)
