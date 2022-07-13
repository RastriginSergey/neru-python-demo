from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.providers.voice.contracts.ITransferMemberPayload import ITransferMemberPayload
from src.providers.voice.memberActions import MemberActions
from src.providers.voice.memberStates import MemberStates
from src.providers.voice.contracts.IUser import IUser
from src.providers.voice.csChannelTypes import CSChannelTypes
from src.providers.voice.contracts.user import User
from src.providers.voice.contracts.IChannel import IChannel
from src.providers.voice.contracts.channel import Channel

@dataclass
class TransferMemberPayload(ITransferMemberPayload):
    user: IUser
    state: str
    channel: IChannel
    action: str
    def __init__(self,userId,legId):
        self.action = MemberActions.Join
        self.channel = Channel()
        self.channel.id = legId
        self.channel.type_ = CSChannelTypes.PHONE
        self.state = MemberStates.Joined
        user = User()
        user.id = userId
        self.user = user
    
    def reprJSON(self):
        dict = {}
        keywordsMap = {"from_":"from","del_":"del","import_":"import","type_":"type"}
        for key in self.__dict__:
            val = self.__dict__[key]

            if type(val) is list:
                parsedList = []
                for i in val:
                    if hasattr(i,'reprJSON'):
                        parsedList.append(i.reprJSON())
                    else:
                        parsedList.append(i)
                val = parsedList

            if hasattr(val,'reprJSON'):
                val = val.reprJSON()
            if key in keywordsMap:
                key = keywordsMap[key]
            dict.__setitem__(key.replace('_hyphen_', '-'), val)
        return dict
