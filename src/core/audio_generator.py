from pathlib import Path
from datetime import datetime, timezone
from elevenlabs.client import ElevenLabs
from elevenlabs import save

from core.config import settings
from core.logger import get_logger

logger = get_logger(__name__)


class AudioGenerator:
    root_dir = Path.cwd()
    tmp_dir = root_dir / "tmp"
    client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)

    @classmethod
    def generate_audio_file(cls, summary: str, job_id: str) -> str:
        cls.tmp_dir.mkdir(parents=True, exist_ok=True)
        logger.info(summary)

        time = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        file_name = f"audio_{time}_{job_id}.mp3"
        file_path = cls.tmp_dir / file_name
        logger.info(f"Generating audio for file {file_name}")

        audio = cls.client.text_to_speech.convert(
            voice_id="Xb7hH8MSUJpSbSDYk0k2",
            text=summary,
            model_id=settings.ELEVENLABS_MODEL,
            output_format="mp3_44100_128",
        )

        save(audio, file_path)

        return file_path
