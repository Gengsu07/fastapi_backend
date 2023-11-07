from pydantic import BaseModel


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    id: int


class UserCommentIn(BaseModel):
    body: str
    post_id: int


class UserComment(UserCommentIn):
    id: int


class UserPostWithComment(BaseModel):
    post: UserPost
    comments: list[UserComment]


# {
#     "post": {"id": 0, "body": "this is post"},
#     "comment": [{"id": 0, "post_id": 0, "body": "first comment"}],
# }
