import os
import sys
import logging
import argparse

from downloader import TikTokDownloader
from decomposer import VideoDecomposer
from vision_analyzer import VisionAnalyzer
from audio_analyzer import AudioAnalyzer
from source_id import SourceIdentifier
from editing_analyzer import EditingAnalyzer
from report_generator import ReportGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("MediaTrace")

def main(url):
    try:
        # Initialize components
        downloader = TikTokDownloader()
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
        
        # Step 3 & 4: Vision & Audio Analysis (Sequential for now, can be parallel)
        logger.info("Analyzing vision...")
        vision_results = vision.analyze_scenes(decomp_data['frame_paths'], decomp_data['scene_timestamps'])
        
        logger.info("Analyzing audio...")
        audio_results = audio.analyze(decomp_data['audio_path'])
        
        # Step 5: Source Identification
        logger.info("Identifying source...")
        source_info = source_id.identify(vision_results, audio_results)
        
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
        
        report = reporter.generate(final_data)
        reporter.save_json(report, "report.json")
        
        print("\n--- ANALYSIS COMPLETE ---")
        print(reporter.format_markdown(report))
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TikTok Video Reviewer")
    parser.add_argument("url", help="TikTok video URL")
    args = parser.parse_args()
    
    main(args.url)
