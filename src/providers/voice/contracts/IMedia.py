from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.voice.contracts.IAudioSettings import IAudioSettings


#interface
class IMedia(ABC):
    audio_settings:IAudioSettings
    audio:bool
