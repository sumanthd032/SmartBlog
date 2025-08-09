from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordRequestForm 
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

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
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

@app.post("/api/posts/", response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.create_user_post(db=db, post=post, user_id=current_user.id)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")