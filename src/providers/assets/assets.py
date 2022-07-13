from dataclasses import dataclass, field
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from src.services.commandService.ICommandService import ICommandService
from src.services.config.IConfig import IConfig
from src.session.ISession import ISession
from src.providers.assets.getAssetLinkPayload import GetAssetLinkPayload
from src.providers.assets.IAssets import IAssets
from src.providers.assets.IGetAssetLinkPayload import IGetAssetLinkPayload

@dataclass
class Assets(IAssets):
    commandService: ICommandService
    config: IConfig
    provider: str = field(default = "Assets")
    def __init__(self,session):
        self.config = session.config
        self.commandService = session.commandService
    
    async def getAssetLink(self,assetPath,duration = "5m"):
        data = GetAssetLinkPayload(assetPath,duration)
        url = self.config.getExecutionUrl(self.provider)
        result = await self.commandService.executeCommand(url,data,None)
        return self.config.assetUrl + result
    
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
