import streamlit as st
import os
import sys
from main import run_pipeline

st.set_page_config(page_title="MediaTrace Dashboard", page_icon="🎥")

st.title("🎥 MediaTrace Analysis Dashboard")
st.markdown("Enter a video URL to start the multimodal analysis pipeline.")

url = st.text_input("TikTok/Video URL", "")

if st.button("Analyze Video"):
    if url:
        with st.spinner("Pipeline running... This may take a while."):
            try:
                # Assuming run_pipeline is adapted to return results or output to json
                # For simplicity here, calling the existing pipeline
                run_pipeline(url)
                st.success("Analysis complete! Check report.json")
                
                # Show report preview
                import json
                with open("report.json", "r") as f:
                    data = json.load(f)
                st.json(data)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a URL.")
