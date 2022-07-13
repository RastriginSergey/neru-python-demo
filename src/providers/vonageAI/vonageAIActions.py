from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class VonageAIActions:
    Analyze = "analyze"
    ImportModel = "import"
