import json
import logging
from typing import Dict, Any

logger = logging.getLogger("MediaTrace.ReportGenerator")

class ReportGenerator:
    """
    Synthesizes analysis data into a final, human-readable report with sentiment and timeline.
    """
    def _analyze_sentiment(self, text: str) -> str:
        # Simple sentiment dictionary (can be expanded)
        positive = ["любовь", "семья", "дружба", "хорошо", "счастье"]
        negative = ["предательство", "враг", "ненависть", "плохо", "против"]
        
        score = 0
        text_lower = text.lower()
        for word in positive:
            if word in text_lower: score += 1
        for word in negative:
            if word in text_lower: score -= 1
            
        if score > 0: return "Позитивное"
        if score < 0: return "Драматичное/Негативное"
        return "Нейтральное"

    def _create_timeline(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        timeline = []
        scenes = data.get('decomp', {}).get('scene_timestamps', [])
        ocr = data.get('editing', {}).get('text_overlays', [])
        
        for ts in scenes:
            # Find closest OCR
            overlay = next((o['text'] for o in ocr if abs(float(o['frame'].split('_ts')[-1].replace('.jpg','')) - ts) < 2.0), "Нет текста")
            timeline.append({
                "timestamp": round(ts, 2),
                "event": f"Смена сцены. Текст на экране: {overlay}"
            })
        return timeline

    def generate(self, data: Dict[str, Any], output_path: str = "report.json"):
        logger.info(f"Generating final report at {output_path}")
        
        text = data.get('audio', {}).get('transcription', {}).get('text', '')
        
        human_report = {
            "summary": {
                "mood": self._analyze_sentiment(text),
                "themes": ["Семья", "Цитаты"] if "семья" in text.lower() else ["Общее"],
                "pacing": data.get('editing', {}).get('pacing_summary', 'Standard')
            },
            "timeline": self._create_timeline(data),
            "raw_data": data
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(human_report, f, indent=4, ensure_ascii=False)
        logger.info("Report generation complete.")
        return output_path
