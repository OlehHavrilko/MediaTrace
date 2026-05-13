import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self):
        pass

    def generate(self, data):
        """
        Synthesizes all analysis data into a structured report.
        """
        report = {
            'generated_at': datetime.now().isoformat(),
            'video_info': data.get('metadata'),
            'source_identification': data.get('source'),
            'scene_analysis': data.get('vision'),
            'audio_analysis': {
                'transcription': data.get('audio', {}).get('transcription', {}).get('text'),
                'music': data.get('audio', {}).get('music', [])
            },
            'editing_techniques': data.get('editing'),
            'summary': self._create_summary(data)
        }
        return report

    def _create_summary(self, data):
        source = data.get('source', {})
        name = source.get('source_name', 'Unknown')
        conf = source.get('confidence', 'low')
        return f"This video is likely from '{name}' with {conf} confidence. It features {len(data.get('vision', []))} analyzed scenes and various editing techniques."

    def save_json(self, report, file_path):
        with open(file_path, 'w') as f:
            json.dump(report, f, indent=4)
        logger.info(f"Report saved to {file_path}")

    def format_markdown(self, report):
        md = f"# Video Review Report\n\n"
        md += f"**Generated at:** {report['generated_at']}\n\n"
        
        src = report['source_identification']
        md += f"## Source Identification\n"
        md += f"- **Source:** {src.get('source_name')} ({src.get('year')})\n"
        md += f"- **Type:** {src.get('type')}\n"
        md += f"- **Confidence:** {src.get('confidence')}\n"
        md += f"- **Reasoning:** {src.get('reasoning')}\n\n"
        
        md += f"## Summary\n{report['summary']}\n\n"
        
        md += f"## Audio Context\n"
        md += f"**Transcription:** {report['audio_analysis']['transcription'][:500]}...\n\n"
        
        md += f"## Editing Techniques\n"
        editing = report['editing']
        md += f"- **Motion:** Avg Magnitude {editing.get('motion_analysis', {}).get('avg_motion_magnitude', 0):.2f}\n"
        md += f"- **Text Overlays:** {len(editing.get('text_overlays', []))} detected\n"
        
        return md
