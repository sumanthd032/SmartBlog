from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

# Create all database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/{user_id}/posts/", response_model=schemas.Post)
def create_post_for_user(
    user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)
):
    # For now, we are not creating users, so we will hardcode a user creation
    # to make sure our post has an author.
    # This is temporary and will be replaced by real user auth later.
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        db_user = models.User(id=user_id, username=f"user_{user_id}", hashed_password="fakepassword")
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return crud.create_user_post(db=db, post=post, user_id=user_id)


@app.get("/posts/", response_model=list[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts