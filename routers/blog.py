from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from utils.oauth2 import get_current_user

import schemas, models, database, uuid

getdb = database.getdb
router = APIRouter(tags=["blog"])

@router.get("/images/{filename}")
def get_image(filename:str):
    return FileResponse(f"images/{filename}")

@router.get("/blog", response_model=list[schemas.ShowBlog])
def list_blog(db:Session=Depends(getdb), current_user:schemas.BaseUser=Depends(get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get("/blog/{id}", response_model=schemas.ShowBlog)
def detail_blog(id:int, db:Session=Depends(getdb)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return blog.first()


@router.post("/blog", response_model=schemas.ShowBlog)
async def create_blog(name:str=Form(...), body:str=Form(...), owner_id:int=Form(...), file:UploadFile=File(...), db:Session=Depends(getdb)):
    
    content = await file.read()
    filename = f"images/{uuid.uuid4()}.jpg"

    with open(filename, "wb") as f:
        f.write(content)

    new_blog = models.Blog(name=name, body=body, owner_id=owner_id, url=f"https://blog-1-k4272118.deta.app/{filename}")

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

@router.put("/blog/{id}", response_model=schemas.ShowBlog)
def update_blog(req:schemas.UpdateBlog, id:int, db:Session=Depends(getdb)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    blog.update(req.dict())

    db.commit()

    return blog.first() 

@router.delete("/blog/{id}")
def delete_blog(id:int, db:Session=Depends(getdb)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    blog.delete()
    db.commit()

    return "done"
