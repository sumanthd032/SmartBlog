from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordRequestForm 
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import ai

import crud, models, schemas, auth 
from database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

from database import get_db

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = crud.authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/users/", response_model=schemas.User)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/api/users/{user_id}/posts/", response_model=schemas.Post)
def create_post_for_user(
    user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_post(db=db, post=post, user_id=user_id)

@app.get("/api/posts/", response_model=list[schemas.Post])
def read_posts(
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    db: Session = Depends(get_db)
):
    posts = crud.get_posts(db, skip=skip, limit=limit, search=search)
    return posts

@app.post("/api/posts/", response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.create_user_post(db=db, post=post, user_id=current_user.id)

@app.post("/api/ai/suggest-title", response_model=dict)
def suggest_title_endpoint(
    request: schemas.AIRequest,
    current_user: models.User = Depends(auth.get_current_user)
):
    title = ai.generate_title(request.content)
    return {"title": title}

@app.post("/api/ai/summarize", response_model=dict)
def summarize_content_endpoint(
    request: schemas.AIRequest,
    current_user: models.User = Depends(auth.get_current_user)
):
    summary = ai.generate_summary(request.content)
    return {"summary": summary}

@app.get("/api/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.post("/api/posts/{post_id}/comments", response_model=schemas.Comment)
def create_comment_for_post(
    post_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.create_comment(db=db, comment=comment, post_id=post_id, author_id=current_user.id)

@app.get("/api/users/me/posts/", response_model=list[schemas.Post])
def read_own_posts(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_user_posts(db=db, user_id=current_user.id)

@app.delete("/api/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_endpoint(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_post = crud.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")

    crud.delete_post(db=db, post=db_post)
    return {"detail": "Post deleted successfully"} 

@app.put("/api/posts/{post_id}", response_model=schemas.Post)
def update_post_endpoint(
    post_id: int,
    post_data: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_post = crud.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if db_post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")

    return crud.update_post(db=db, post=db_post, updated_data=post_data)

@app.get("/api/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.put("/api/users/me", response_model=schemas.User)
def update_profile(
    profile_data: schemas.ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.update_user_profile(db=db, user_id=current_user.id, profile_data=profile_data)

@app.get("/api/users/{username}", response_model=schemas.UserPublicProfile)
def read_user_profile(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_profile(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not db_user.is_public:
        raise HTTPException(status_code=403, detail="This profile is private")
    return db_user

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
