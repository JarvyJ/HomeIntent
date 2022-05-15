from enum import Enum
from exceptions import HomeIntentHTTPException
from pathlib import Path
import subprocess
from typing import Dict

from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel

import aiofiles.os
import os

from config import get_settings
from rhasspy_api import RhasspyAPI

router = APIRouter()
rhasspy_url = (
    "http://rhasspy:12101" if os.environ.get("DOCKER_DEV") == "True" else get_settings().rhasspy.url
)
RhasspyApi = RhasspyAPI(rhasspy_url)

# this doesn't actually work...
# maybe i'll do a status page at some point.
# @router.on_event("startup")
# async def try_rhasspy_api():
#     await RhasspyApi.get("/api/version")


@router.on_event("shutdown")
async def close_rhasspy_api():
    await RhasspyApi.close()


@router.get("/rhasspy/audio/microphones", response_model=Dict[int, str])
async def get_rhasspy_microphones():
    return await RhasspyApi.get("/api/microphones")


@router.get("/rhasspy/audio/test-microphones", response_model=Dict[int, str])
async def test_rhasspy_microphones():
    """
    Hit the endpoint, and speak into the microphones, after a few seconds,
    it'll return the microphones which picked up sound
    """
    rhasspy_microphones = await RhasspyApi.get("/api/test-microphones")
    small_list = {}
    for mic_id, name in rhasspy_microphones.items():
        if "(working!)" in name:
            small_list[mic_id] = name
    return small_list


@router.get("/rhasspy/audio/speakers", response_model=Dict[str, str])
async def get_rhasspy_speakers(show_all: bool = True):
    rhasspy_speakers = await RhasspyApi.get("/api/speakers")
    if show_all:
        return rhasspy_speakers
    else:
        small_list = {}
        for speaker_id, name in rhasspy_speakers.items():
            if speaker_id.startswith("default:"):
                small_list[speaker_id] = name

        return small_list


@router.get("/rhasspy/audio/test-speakers")
def test_speakers(device: str = None):
    test_file = str(Path(__file__).resolve().parent.parent / "test-sound.wav")
    output = play_file(test_file, device)
    if output.returncode != 0:
        raise HomeIntentHTTPException(
            400,
            title=f"Error playing back sound effect from sound device: {device}",
            detail={
                "filename": test_file,
                "stdout": output.stdout.decode("utf-8"),
                "stderr": output.stderr.decode("utf-8"),
            },
        )


def play_file(file, device):
    if device:
        output = subprocess.run(
            ["aplay", "-D", device, "-t", "wav", file], check=False, capture_output=True
        )

    else:
        output = subprocess.run(["aplay", "-t", "wav", file], check=False, capture_output=True)

    return output


class SoundEffect(str, Enum):
    BEEP_HIGH = "beep_high"
    BEEP_LOW = "beep_low"
    ERROR = "error"


@router.get("/rhasspy/audio/play-effects")
def play_effects(sound_effect: SoundEffect, device: str = None):
    filename = f"{sound_effect.value.replace('_', '-')}.wav"
    custom_file_path = Path("/config") / filename
    file_path = (
        Path(__file__).parent.parent.resolve().parent / "home_intent/default_configs" / filename
    )

    if custom_file_path.is_file():
        play_file(custom_file_path, device)
    else:
        play_file(file_path, device)
    return file_path


class CustomOrDefault(str, Enum):
    CUSTOM = "custom"
    DEFAULT = "default"


class SoundEffectMeta(BaseModel):
    custom_or_default: CustomOrDefault


@router.get("/rhasspy/audio/effects", response_model=Dict[SoundEffect, SoundEffectMeta])
async def get_sound_effects_meta():
    output = {}
    for sound_effect in SoundEffect:
        custom_file_path = get_custom_sound_effect_path(sound_effect)

        if await aiofiles.os.path.isfile(custom_file_path):
            output[sound_effect] = SoundEffectMeta(custom_or_default=CustomOrDefault.CUSTOM)
        else:
            output[sound_effect] = SoundEffectMeta(custom_or_default=CustomOrDefault.DEFAULT)

    return output


def get_custom_sound_effect_path(sound_effect: SoundEffect) -> Path:
    filename = f"{sound_effect.value.replace('_', '-')}.wav"
    return Path("/config") / filename


@router.post("/rhasspy/audio/effects")
def upload_sound_effects(sound_effect: SoundEffect, file: UploadFile = File(...)):
    if file.content_type not in ("audio/wave", "audio/wav", "audio/x-wav", "audio/x-pn-wav"):
        raise HomeIntentHTTPException(400, title="Audio has to be in wav type")
    file_path = get_custom_sound_effect_path(sound_effect)
    file_path.write_bytes(file.file.read())  # using file.file since pathlib is not async


@router.post("/rhasspy/audio/set-default")
async def set_sound_effect_to_default(sound_effect: SoundEffect):
    file_path = get_custom_sound_effect_path(sound_effect)
    if await aiofiles.os.path.isfile(file_path):
        await aiofiles.os.remove(file_path)
