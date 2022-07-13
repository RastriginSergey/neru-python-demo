from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class WebhookEventTypes:
    text = "text"
    image = "image"
    video = "video"
    file = "file"
    audio = "audio"
    reply = "reply"
    unsupported = "unsupported"
    vcard = "vcard"
