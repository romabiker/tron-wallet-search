from abc import ABC, abstractmethod


class ServiceBase(ABC):
    
    @abstractmethod
    async def __call__(self, *args, **kwargs):
        ...
