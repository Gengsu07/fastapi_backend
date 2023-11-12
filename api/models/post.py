from pydantic import BaseModel, ConfigDict


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UserCommentIn(BaseModel):
    body: str
    post_id: int


class UserComment(UserCommentIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UserPostWithComment(BaseModel):
    post: UserPost
    comments: list[UserComment]


# {
#     "post": {"id": 0, "body": "this is post"},
#     "comment": [{"id": 0, "post_id": 0, "body": "first comment"}],
# }
