from fastapi.websockets import WebSocket

from aioredis import from_url as redis_from_url
from aioredis.client import Redis, PubSub

from asyncio import wait as asyncio_wait

from settings import REDIS_URL


class NotificationsHandler:
    redis: Redis = redis_from_url( REDIS_URL, encoding = "utf-8", decode_responses = True )


    @classmethod
    async def send( cls, channel, message ):
        await cls.redis.publish( channel, message )


    def __init__( self, websocket: WebSocket ):
        self.websocket = websocket
        self.destroy = False

        self.pubsub: PubSub = self.redis.pubsub( )

    async def __call__( self ):
        await asyncio_wait( [ self.subscriber( ), self.receiver( ) ] )

    async def subscribe( self, *args: str ):
        await self.pubsub.subscribe( *args )

    async def psubscribe( self, *args: str ):
        await self.pubsub.psubscribe( *args )

    async def subscriber( self ):
        while True:
            try:
                if self.destroy:
                    raise Exception # break cycle

                message = await self.pubsub.get_message( ignore_subscribe_messages = True )

                if message:
                    await self.websocket.send_text( message[ 'data' ] )
            except:
                break

        await self.pubsub.close( )

    async def receiver( self ): # handle disconnect here
        while True:
            try:
                await self.websocket.receive( )
            except:
                self.destroy = True

                break