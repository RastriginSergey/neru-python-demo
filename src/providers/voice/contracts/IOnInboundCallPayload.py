from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.session.IPayloadWithCallback import IPayloadWithCallback
from src.providers.voice.contracts.IChannelPhoneEndpoint import IChannelPhoneEndpoint


#interface
class IOnInboundCallPayload(IPayloadWithCallback):
    to:IChannelPhoneEndpoint
    from_:IChannelPhoneEndpoint
