from abc import ABC, abstractmethod
from typing import AsyncIterator, Any


class MessageConsumer(ABC):
    @abstractmethod
    async def start(self) -> None:
        ...

    @abstractmethod
    async def stop(self) -> None:
        ...

    @abstractmethod
    async def consume(self) -> AsyncIterator[Any]:
        ...
