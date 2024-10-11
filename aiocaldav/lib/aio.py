from __future__ import annotations

class AsyncInit(type):
    """
    A metaclass that affords an async ``__init__`` method

    Source: https://stackoverflow.com/questions/33128325/#answer-76636725
    """

    async def __call__(cls, *args, **kwargs):
        instance = cls.__new__(cls, *args, **kwargs)
        await instance.__init__(*args, **kwargs)
        return instance


