from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.IPayloadWithCallback import IPayloadWithCallback
from src.providers.messages.contracts.IMessageContact import IMessageContact
from src.session.IWrappedCallback import IWrappedCallback


#interface
class IListenEventsPayload(IPayloadWithCallback):
    from_:IMessageContact
    to:IMessageContact
    callback:IWrappedCallback
