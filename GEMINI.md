# Project Overview: MediaTrace

This project is a comprehensive technical plan and architectural design for an automated script capable of analyzing video content (originally focused on TikTok). The primary goal is to identify the source of the content (e.g., specific movies, TV series, or known media) and describe the editing techniques used in the video.

## Core Capabilities
- **Video Acquisition:** Downloading videos from TikTok URLs.
- **Decomposition:** Splitting videos into frames and separate audio tracks.
- **Multimodal Analysis:**
    - **Vision:** Identifying characters, settings, costumes, and visual styles using vision models (GPT-4o, Gemini, CLIP).
    - **Audio:** Transcribing speech (Whisper), identifying music (AcoustID), and analyzing sound effects.
- **Source Identification:** Matching extracted features against media databases (TMDB, OMDb) via semantic and full-text search.
- **Editing Analysis:** Detecting scene transitions, optical flow (slow-mo/speed-up), color grading, and overlays (OCR).
- **Report Generation:** Producing structured JSON or Markdown reports summarizing the findings.

## Project Structure
The project currently consists of foundational documentation:
- `ideaprompt`: The initial high-level requirement and role definition for the project.
- `plan`: A detailed 8-stage development plan covering everything from video acquisition to error handling and final report generation.

## Development Workflow
As per the `plan`, the development follows a stateless pipeline architecture:
1. **Downloader:** Fetches the video.
2. **Decomposer:** Prepares frames and audio.
3. **Vision & Audio Analyzers:** Parallel processing of visual and auditory data.
4. **Source Identification:** LLM-based reasoning and API lookups.
5. **Editing Analyzer:** Technical analysis of the montage.
6. **Report Generator:** Synthesis of all data into a final output.

## Key Technologies (Inferred/Planned)
- **AI Models:** GPT-4o, Gemini Vision, CLIP, Whisper.
- **Video Processing:** FFmpeg (implied for decomposition and optical flow).
- **APIs:** TMDB, OMDb, TikTok oEmbed.
- **Data Handling:** Vector similarity search, OCR, histogram analysis.

## Current Status
This is a **Non-Code Project** in its current state, serving as a blueprint for implementation. Future interactions should focus on implementing the stages outlined in the `plan`.
