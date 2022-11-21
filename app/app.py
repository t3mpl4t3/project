from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from notifications.router import router as notifications_router
from posts.router import router as posts_router

from database import database


app = FastAPI( )


@app.on_event( 'startup' )
async def startup( ):
    await database.connect( )

@app.on_event( 'shutdown' )
async def shutdown( ):
    await database.disconnect( )


app.include_router( router = notifications_router )
app.include_router( router = posts_router, prefix = '/posts', tags = [ 'Posts' ] )


@app.get( "/" )
async def get( ):
    return HTMLResponse(
        """
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Messages</title>
                </head>
                <body>
                <form onsubmit="onPost(event)">
                    <input type="text" id="messageText" autocomplete="off"/>
                    <button>Send</button>
                </form>
                <ul id='messages'>
                    <ul id='messages'>
                    </ul>
                    <script>
                        postData = (async (body) => {
                            const rawResponse = await fetch('http://127.0.0.1:8000/posts/', {
                                method: 'POST',
                                headers: {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json'
                                },
                                body: body
                            });
                        })

                        insertPost = function(data, before) {
                            var messages = document.getElementById('messages')
                            var message = document.createElement('li')
                            var content = document.createTextNode(data)
                            message.appendChild(content)

                            if (before)
                                messages.insertBefore(message, messages.firstChild)
                            else
                                messages.appendChild( message )
                        };

                        var ws = new WebSocket("ws://localhost:8000/notifications");

                        ws.onmessage = function(event) {
                            const id = event.data
                            fetch( 'http://127.0.0.1:8000/posts/' + id ).then((response) => response.json())
                            .then((data) => {
                                insertPost( data.text, true )
                            });
                        };

                        fetch( 'http://127.0.0.1:8000/posts' ).then((response) => response.json())
                            .then((data) => {
                                for (let i = 0; i < data.length; i++) {
                                    insertPost( data[i].text )
                                }
                            });

                        async function onPost( event ) {
                            event.preventDefault()
                            var input = document.getElementById("messageText")

                            const data = {
                                text: input.value
                            }

                            await postData( JSON.stringify( data ) );

                            input.value = ''
                        }
                    </script>
                    <style>
                        * {
                            margin: 0px;
                            padding: 0px;
                        }
                        body {
                            padding: 20px;
                        }
                        ul {
                            margin-top: 20px;
                            list-style: none;
                        }
                        li {
                            margin-top: 5px;
                        }
                    </style>
                </body>
            </html>
        """
    )