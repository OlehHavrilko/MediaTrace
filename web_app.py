import streamlit as st
import time
from src.tasks import analyze_video_task
from src.vector_search import VectorSearchEngine
from src.database import SessionLocal, VideoAnalysis

# Initialize Vector Search Engine (Singleton-like pattern for demo)
@st.cache_resource
def get_search_engine():
    engine = VectorSearchEngine()
    # Populate index from DB on startup
    db = SessionLocal()
    analyses = db.query(VideoAnalysis).all()
    for a in analyses:
        # Index vision analysis text
        text = f"{a.title} " + " ".join([v.get('analysis', '') for v in (a.vision_results or [])])
        engine.add_analysis(a.video_id, text)
    db.close()
    return engine

st.set_page_config(page_title="MediaTrace Dashboard", page_icon="🎥", layout="wide")

st.title("🎥 MediaTrace Analysis Dashboard")

tab1, tab2 = st.tabs(["Analyze New", "Semantic Search"])

with tab1:
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

with tab2:
    query = st.text_input("Describe a scene or theme (e.g., 'dramatic lighting')", "")
    if st.button("Search"):
        if query:
            engine = get_search_engine()
            results = engine.search(query)
            for res in results:
                st.write(f"**Video ID:** {res['metadata']['video_id']} | **Similarity:** {res['distance']:.2f}")
                st.write(f"Text Snippet: {res['metadata']['text'][:200]}...")
                st.divider()
        else:
            st.warning("Please enter a search query.")
