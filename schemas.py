from pydantic import BaseModel 

class BaseUser(BaseModel):
    username : str 
    email : str

class User(BaseModel):
    id : int
    username : str 
    email : str

class CreateUser(BaseUser):
    password : str

class Blog(BaseModel):
    name : str
    body : str
    url : str

class UpdateBlog(BaseModel):
    name : str
    body : str

class ShowUser(BaseUser):
    blogs : list[Blog]=[]

    class Config:
        orm_mode = True

class ShowBlog(Blog):
    id : int
    owner : User

    class Config:
        orm_mode = True

class Login(BaseModel):
    username : str
    password : str

class TokenData(BaseModel):
    username : str