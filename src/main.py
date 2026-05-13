import os
import sys
import logging
import argparse

from downloader import VideoDownloader
from decomposer import VideoDecomposer
from vision_analyzer import VisionAnalyzer
from audio_analyzer import AudioAnalyzer
from source_id import SourceIdentifier
from editing_analyzer import EditingAnalyzer
from report_generator import ReportGenerator
from cache import PipelineCache

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("MediaTrace")

def run_pipeline(url):
    cache = PipelineCache()
    cached_data = cache.get(url)
    if cached_data:
        logger.info("Cache hit!")
        return cached_data

    # Initialize components
    downloader = VideoDownloader()
    decomposer = VideoDecomposer()
    vision = VisionAnalyzer()
    audio = AudioAnalyzer()
    source_id = SourceIdentifier()
    editing = EditingAnalyzer()
    reporter = ReportGenerator()

    # Step 1: Download
    logger.info(f"Starting analysis for URL: {url}")
    metadata = downloader.download(url)
    
    # Step 2: Decompose
    logger.info("Decomposing video...")
    decomp_data = decomposer.decompose(metadata)
    
    # Step 3 & 4: Vision & Audio Analysis
    logger.info("Analyzing vision...")
    vision_results = vision.analyze_frames(decomp_data['frame_paths'], decomp_data['all_timestamps'])
    
    logger.info("Analyzing audio...")
    audio_results = audio.analyze(decomp_data['audio_path'])
    
    # Step 5: Source Identification
    logger.info("Identifying source...")
    analysis_data = {'vision': {'source_hint': vision_results[0].get('analysis', '') if vision_results else ""}}
    source_info = source_id.identify(analysis_data)
    
    # Step 6: Editing Analysis
    logger.info("Analyzing editing techniques...")
    editing_info = editing.analyze(metadata['file_path'], decomp_data['frame_paths'])
    
    # Step 7: Report Generation
    logger.info("Generating report...")
    final_data = {
        'metadata': metadata,
        'decomp': decomp_data,
        'vision': vision_results,
        'audio': audio_results,
        'source': source_info,
        'editing': editing_info
    }
    
    cache.set(url, final_data)
    reporter.generate(final_data, "report.json")
    return final_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MediaTrace Analysis Pipeline")
    parser.add_argument("url", help="TikTok video URL")
    args = parser.parse_args()
    run_pipeline(args.url)
