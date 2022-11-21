from fastapi import APIRouter, Body, Path

from database import database
from .models import Post, PostIn, PostOut

from sqlalchemy import select, insert

from notifications import send


router = APIRouter( )


@router.get(
    path = '/',
    description = 'All posts',
    response_model = list[ PostOut ]
    )
async def _list( ):
    query = select( Post ).order_by( Post.c.id.desc( ) )
    raw = await database.fetch_all( query )

    return raw


@router.get(
    path = '/{id}',
    description = 'All posts',
    response_model = PostOut
    )
async def get( id: int = Path( default = ..., title = 'Post id' ) ):
    query = select( Post ).where( Post.c.id == id )
    raw = await database.fetch_one( query = query )

    return raw


@router.post(
    path = '/',
    description = 'Create post',
    response_model = PostOut,
    status_code = 201
    )
async def create( post: PostIn = Body( title = 'Post' ) ):
    post_dict = post.dict( )

    query = insert( Post )
    id = await database.execute( query, post_dict )

    await send( 'posts', str( id ) )

    return PostOut( id = id, **post_dict )