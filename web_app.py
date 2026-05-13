import streamlit as st
import time
from src.tasks import analyze_video_task

st.set_page_config(page_title="MediaTrace Dashboard", page_icon="🎥")

st.title("🎥 MediaTrace Analysis Dashboard")
url = st.text_input("TikTok/Video URL", "")

if st.button("Analyze Video"):
    if url:
        task = analyze_video_task.delay(url)
        st.info(f"Task submitted! ID: {task.id}")
        
        # Poll for status
        placeholder = st.empty()
        while not task.ready():
            placeholder.text("Pipeline running... Please wait.")
            time.sleep(2)
            
        result = task.result
        if result['status'] == 'completed':
            st.success("Analysis complete!")
            st.json(result['result'])
        else:
            st.error(f"Analysis failed: {result.get('error')}")
    else:
        st.warning("Please enter a URL.")
