from fastapi import APIRouter, HTTPException

from api.database import comment_table, database, post_table
from api.models.post import (
    UserComment,
    UserCommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComment,
)

router = APIRouter()


async def find_post(postId: int):
    query = post_table.select().where(post_table.c.id == postId)

    return await database.fetch_one(query)


@router.get("/post", response_model=list[UserPost])
async def get_all_post():
    query = post_table.select()
    return await database.fetch_all(query)


@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    body_data = post.model_dump()
    query = post_table.insert().values(body_data)
    last_record_id = await database.execute(query)
    return {**body_data, "id": last_record_id}


@router.get("/comment", response_model=list[UserComment])
async def get_all_comment():
    query = comment_table.select()
    return await database.fetch_all(query)


@router.post("/comment", response_model=UserComment, status_code=201)
async def create_comment(comment: UserCommentIn):
    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post Not Found")

    body_data = comment.model_dump()
    query = comment_table.insert().values(body_data)
    last_comment_id = await database.execute(query)
    return {**body_data, "id": last_comment_id}


@router.get("/post/{post_id}/comment", response_model=list[UserComment])
async def get_comment_on_post(post_id: int):
    query = comment_table.select().where(comment_table.c.post_id == post_id)
    return await database.fetch_all(query)


@router.get("/post/{post_id}", response_model=UserPostWithComment)
async def get_post_with_comment(post_id: int):
    post = await find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post Not Found")
    return {"post": post, "comments": await get_comment_on_post(post_id)}
