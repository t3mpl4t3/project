# FastAPI notifications system
#### Video Demo:  https://youtu.be/m33F19qFrxI
#### Description:
This is notifications system build with websockets and Redis Pub/Sub.
It is suitable for highloaded apps.
Posts app just made to show how it can be used.

Use case:

Chats. You can do notification body like:
     {
       'event': 'new_message',
       'chat_id': 'chat_id',
       'message_id': 'message_id',
     }
