from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class CSChannelTypes:
    PHONE = "phone"
    APP = "app"
    SIP = "sip"
    VBC = "vbc"
    WEBSOCKET = "websocket"
