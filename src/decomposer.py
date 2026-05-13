import os
import subprocess
import logging
import json

logger = logging.getLogger(__name__)

class VideoDecomposer:
    def __init__(self, output_base="temp"):
        self.output_base = output_base
        if not os.path.exists(self.output_base):
            os.makedirs(self.output_base)

    def extract_audio(self, video_path, output_name="audio.wav"):
        """
        Extracts audio from video file.
        """
        output_path = os.path.join(self.output_base, output_name)
        cmd = [
            'ffmpeg', '-y', '-i', video_path,
            '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2',
            output_path
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            logger.info(f"Audio extracted to: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Error extracting audio: {e.stderr.decode()}")
            raise

    def get_scene_changes(self, video_path, threshold=0.4):
        """
        Detects scene changes using ffmpeg.
        Returns a list of timestamps.
        """
        cmd = [
            'ffmpeg', '-i', video_path,
            '-filter:v', f"select='gt(scene,{threshold})',showinfo",
            '-f', 'null', '-'
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            # Parse showinfo output
            timestamps = []
            for line in result.stderr.split('\n'):
                if 'pts_time:' in line:
                    # Example line: [Parsed_showinfo_1 @ 0x...] n:   1 pts: 153600 pts_time:5.12 ...
                    parts = line.split('pts_time:')
                    if len(parts) > 1:
                        ts = float(parts[1].split()[0])
                        timestamps.append(ts)
            return sorted(list(set(timestamps)))
        except Exception as e:
            logger.error(f"Error detecting scenes: {e}")
            return []

    def extract_frames(self, video_path, timestamps, output_dir="frames"):
        """
        Extracts frames at specific timestamps.
        """
        out_path = os.path.join(self.output_base, output_dir)
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        
        frame_paths = []
        for i, ts in enumerate(timestamps):
            frame_name = f"frame_{i:04d}_{ts:.2f}.jpg"
            frame_path = os.path.join(out_path, frame_name)
            cmd = [
                'ffmpeg', '-y', '-ss', str(ts),
                '-i', video_path,
                '-frames:v', '1',
                '-q:v', '2', # High quality
                frame_path
            ]
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                frame_paths.append(frame_path)
            except subprocess.CalledProcessError as e:
                logger.warning(f"Failed to extract frame at {ts}: {e.stderr.decode()}")
        
        logger.info(f"Extracted {len(frame_paths)} frames to {out_path}")
        return frame_paths

    def decompose(self, video_metadata):
        """
        Full decomposition pipeline.
        """
        video_path = video_metadata['file_path']
        
        # 1. Audio
        audio_path = self.extract_audio(video_path)
        
        # 2. Scene Detection
        scene_timestamps = self.get_scene_changes(video_path)
        
        # Add start frame and periodic frames if video is long
        duration = video_metadata.get('duration', 0)
        all_timestamps = {0.0}
        all_timestamps.update(scene_timestamps)
        
        # Periodic sampling every 2 seconds if not already covered
        if duration:
            for t in range(0, int(duration), 2):
                all_timestamps.add(float(t))
        
        sorted_timestamps = sorted(list(all_timestamps))
        
        # 3. Frames
        frame_paths = self.extract_frames(video_path, sorted_timestamps)
        
        return {
            'audio_path': audio_path,
            'scene_timestamps': scene_timestamps,
            'frame_paths': frame_paths,
            'timestamps': sorted_timestamps
        }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
