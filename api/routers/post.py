from fastapi import APIRouter, HTTPException

from api.models.post import (
    UserComment,
    UserCommentIn,
    UserPost,
    UserPostIn,
    UserPostWithComment,
)

router = APIRouter()


post_data = {}
comment_data = {}


def find_post(postId: int):
    post = post_data.get(postId)
    if not post:
        raise HTTPException(status_code=404, detail="Post Not Found")
    return post


@router.get("/post", response_model=list[UserPost])
async def get_all_post():
    data = list(post_data.values())
    return data


@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    body_data = post.model_dump()
    last_post_id = len(post_data)
    new_post = {**body_data, "id": last_post_id}
    post_data[last_post_id] = new_post
    return new_post


@router.get("/comment", response_model=list[UserComment])
async def get_all_comment():
    data = list(comment_data.values())
    return data


@router.post("/comment", response_model=UserComment, status_code=201)
async def create_comment(comment: UserCommentIn):
    post = find_post(comment.post_id)
    if post:
        body_data = comment.model_dump()
        last_comment_id = len(comment_data)
        new_comment = {**body_data, "id": last_comment_id}
        comment_data[last_comment_id] = new_comment
    return new_comment


@router.get("/post/{post_id}/comment", response_model=list[UserComment])
async def get_comment_on_post(post_id: int):
    post = find_post(post_id)
    if post:
        return [
            comment
            for comment in comment_data.values()
            if comment["post_id"] == post_id
        ]


@router.get("/post/{post_id}", response_model=UserPostWithComment)
async def get_post_with_comment(post_id: int):
    post = find_post(post_id)
    if post:
        return {"post": post, "comments": await get_comment_on_post(post_id)}
