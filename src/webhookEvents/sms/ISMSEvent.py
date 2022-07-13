from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.webhookEvents.IBaseEvent import IBaseEvent
from src.webhookEvents.sms.ISMSMetadata import ISMSMetadata
from src.webhookEvents.sms.ISMSUsage import ISMSUsage


#interface
class ISMSEvent(IBaseEvent):
    channel:str
    usage:ISMSUsage
    sms:ISMSMetadata
