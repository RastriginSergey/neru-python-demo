from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class LogLevels:
    error = "error"
    warn = "warn"
    info = "info"
    debug = "debug"
