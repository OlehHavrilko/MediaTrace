import os
import subprocess
import logging
from typing import List, Dict, Any

logger = logging.getLogger("MediaTrace.Decomposer")

class VideoDecomposer:
    """
    Handles video file decomposition into audio and visual components.
    Uses FFmpeg for processing.
    """
    def __init__(self, output_base: str = "temp"):
        self.output_base = os.path.abspath(output_base)
        if not os.path.exists(self.output_base):
            os.makedirs(self.output_base)
            logger.info(f"Created base output directory: {self.output_base}")

    def _run_ffmpeg(self, args: List[str], desc: str):
        """Helper to run ffmpeg commands safely."""
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error'] + args
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg error ({desc}): {e.stderr}")
            raise RuntimeError(f"FFmpeg failed during {desc}")

    def extract_audio(self, video_path: str, video_id: str) -> str:
        """
        Extracts high-quality audio in WAV format.
        """
        audio_dir = os.path.join(self.output_base, video_id)
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
            
        output_path = os.path.join(audio_dir, "audio.wav")
        args = [
            '-y', '-i', video_path,
            '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2',
            output_path
        ]
        self._run_ffmpeg(args, "audio extraction")
        logger.info(f"Audio extracted: {output_path}")
        return output_path

    def get_scene_changes(self, video_path: str, threshold: float = 0.3) -> List[float]:
        """
        Detects scene change timestamps using FFmpeg's scene detection.
        """
        logger.info(f"Detecting scenes with threshold {threshold}...")
        cmd = [
            'ffmpeg', '-hide_banner', '-i', video_path,
            '-filter:v', f"select='gt(scene,{threshold})',showinfo",
            '-f', 'null', '-'
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            timestamps = []
            for line in result.stderr.split('\n'):
                if 'pts_time:' in line:
                    # Parse pts_time:5.12
                    try:
                        pts_part = line.split('pts_time:')[1].split()[0]
                        timestamps.append(float(pts_part))
                    except (IndexError, ValueError):
                        continue
            
            unique_ts = sorted(list(set(timestamps)))
            logger.info(f"Detected {len(unique_ts)} scene changes.")
            return unique_ts
        except Exception as e:
            logger.error(f"Scene detection failed: {e}")
            return []

    def extract_frames(self, video_path: str, video_id: str, timestamps: List[float]) -> List[str]:
        """
        Extracts frames at specific timestamps with high quality.
        """
        frames_dir = os.path.join(self.output_base, video_id, "frames")
        if not os.path.exists(frames_dir):
            os.makedirs(frames_dir)
        
        frame_paths = []
        for i, ts in enumerate(timestamps):
            frame_name = f"frame_{i:04d}_ts{ts:.2f}.jpg"
            frame_path = os.path.join(frames_dir, frame_name)
            
            # Using -ss before -i for faster seeking
            args = [
                '-y', '-ss', f"{ts:.3f}",
                '-i', video_path,
                '-frames:v', '1',
                '-q:v', '2',
                frame_path
            ]
            try:
                self._run_ffmpeg(args, f"frame extraction at {ts}")
                frame_paths.append(frame_path)
            except Exception:
                continue
        
        logger.info(f"Extracted {len(frame_paths)} frames.")
        return frame_paths

    def decompose(self, video_metadata: Dict[str, Any], scene_threshold: float = 0.3) -> Dict[str, Any]:
        """
        Orchestrates the full decomposition process.
        """
        video_path = video_metadata['file_path']
        video_id = video_metadata['id']
        duration = video_metadata.get('duration', 0)
        
        logger.info(f"Decomposing video: {video_id}")
        
        # 1. Extract Audio
        audio_path = self.extract_audio(video_path, video_id)
        
        # 2. Scene Detection
        scene_ts = self.get_scene_changes(video_path, threshold=scene_threshold)
        
        # 3. Compile list of timestamps to extract (Scenes + Periodic)
        ts_to_extract = {0.0} # Always start
        ts_to_extract.update(scene_ts)
        
        # Add a frame every 5 seconds if not already covered
        if duration:
            for t in range(5, int(duration), 5):
                ts_to_extract.add(float(t))
            ts_to_extract.add(float(duration - 0.1) if duration > 0.1 else 0.0) # Last frame
            
        sorted_ts = sorted(list(ts_to_extract))
        
        # 4. Extract Frames
        frame_paths = self.extract_frames(video_path, video_id, sorted_ts)
        
        return {
            'video_id': video_id,
            'audio_path': audio_path,
            'frame_paths': frame_paths,
            'scene_timestamps': scene_ts,
            'all_timestamps': sorted_ts,
            'output_dir': os.path.join(self.output_base, video_id)
        }
