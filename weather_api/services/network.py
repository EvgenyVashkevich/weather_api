import aiohttp
from fastapi import HTTPException, status


class Network:
    """ Simplified interface for `aiohttp.ClientSession` """

    def __init__(self, **kwargs):
        self.session = aiohttp.ClientSession(**kwargs)

    async def __aenter__(self) -> 'Network':
        return self

    async def __aexit__(self, *_) -> None:
        await self.session.close()

    async def _request(self, method: str, **kwargs) -> dict:
        """ Alias for `aiohttp.ClientSession._request` method with custom errors handling """

        async with getattr(self.session, method)(**kwargs) as response:
            result = await response.json()
            if response.status != status.HTTP_200_OK:
                raise HTTPException(detail=result['message'], status_code=response.status)
        return result

    async def post(self, **kwargs) -> dict:
        """ Alias for `self._request` method with predefined method (POST) """

        return await self._request(method='post', **kwargs)

    async def get(self, **kwargs) -> dict:
        """ Alias for `self._request` method with predefined method (GET) """

        return await self._request(method='get', **kwargs)
