from fastapi import APIRouter
from fastapi.websockets import WebSocket

from .service import NotificationsHandler


router = APIRouter( )


'''
    pseudocode


    1. auth

    2. subscribe to channels - chats from user.chats

    3. handle every new message - notification

        message will be json:

        {
            "event": "message",
            "chat": "chat_id",
            "message": "message_id"
        }

    then through rest we will get message and push to chat
'''


@router.websocket( path = '/notifications' )
async def notifications( websocket: WebSocket ):
    await websocket.accept( )

    handler = NotificationsHandler( websocket )

    await handler.subscribe( 'posts' ) # like that we can subscribe for our chats and other

    await handler( )

    del handler