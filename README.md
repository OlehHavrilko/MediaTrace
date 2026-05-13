# 🎥 MediaTrace

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenAI Whisper](https://img.shields.io/badge/AI-Whisper-green.svg)](https://github.com/openai/whisper)
[![Google Gemini](https://img.shields.io/badge/AI-Gemini-blue.svg)](https://ai.google.dev/)
[![PyTorch](https://img.shields.io/badge/Framework-PyTorch-ee4c2c.svg)](https://pytorch.org/)

**MediaTrace** is an advanced multimodal analysis engine designed to deconstruct video content, identify its original source, and analyze professional editing techniques. Whether it's a TikTok clip, a movie snippet, or social media content, MediaTrace traces it back to its roots.

---

## 🌟 Key Features

- **🔍 Source Identification:** Automatically detects movies, TV shows, and music using AI-driven semantic search and database matching (TMDB, OMDb, AcoustID).
- **🧠 Multimodal Analysis:**
  - **Vision:** Character recognition, costume analysis, and scene setting detection using Gemini Vision & GPT-4o.
  - **Audio:** High-accuracy transcription via Whisper and music identification via fingerprinting.
- **🎬 Editing Forensics:** Analyzes transitions, color grading, optical flow (slow-mo/speed-up), and text overlays (OCR).
- **📊 Structured Reports:** Generates comprehensive JSON or Markdown reports with all extracted insights.

---

## 🚀 Architecture

MediaTrace follows a stateless pipeline architecture for maximum reliability and scalability:

1.  **Downloader:** Efficiently fetches video content from various sources.
2.  **Decomposer:** Splits video into high-quality frames and synchronized audio tracks.
3.  **Analyzers:** Parallel processing of visual and auditory data streams.
4.  **Source Identifier:** LLM-based reasoning combined with API lookups.
5.  **Montage Analyzer:** Deep dive into the technical aspects of the video's creation.
6.  **Synthesizer:** Aggregates findings into a final, human-readable report.

---

## 🛠 Installation

### Prerequisites
- Python 3.13+
- FFmpeg installed on your system
- API Keys for Gemini/GPT-4o and TMDB (optional but recommended)

### Setup
```bash
git clone https://github.com/yourusername/MediaTrace.git
cd MediaTrace
./install.sh
```

---

## 📖 Usage

Run the main analyzer by providing a video URL or local path:

```bash
source venv/bin/activate
python src/main.py --url "https://www.tiktok.com/@example/video/123456789"
```

---

## 🗺 Roadmap

- [x] Core Architecture Design
- [ ] Multimodal Analysis Implementation
- [ ] Source Identification API Integration
- [ ] Editing Technique Analysis Engine
- [ ] Advanced Web Dashboard for Reports

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by the MediaTrace Team
</p>
