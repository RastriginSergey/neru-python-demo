from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class RequestMethods:
    GET = "get"
    POST = "post"
    PUT = "put"
    DEL = "delete"
    HEAD = "head"
    PATCH = "patch"
    OPTIONS = "options"
