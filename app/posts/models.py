from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String

from database import metadata


Post = Table(
    'posts',
    metadata,

    Column( "id", Integer, primary_key = True ),
    Column( "text", String( length = 100 ) ),
)


class PostIn( BaseModel ):
    text: str

class PostOut( BaseModel ):
    id: int

    text: str