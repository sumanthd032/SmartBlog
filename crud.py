from sqlalchemy.orm import Session
import models, schemas, auth

def authenticate_user(db: Session, username: str, password: str):
    """Finds a user and verifies their password."""
    user = get_user_by_username(db, username=username)
    if not user:
        return False
    if not auth.verify_password(password, user.hashed_password):
        return False
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()

def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def authenticate_user(db: Session, username: str, password: str):
    """Finds a user and verifies their password."""
    user = get_user_by_username(db, username=username)
    if not user:
        return False
    if not auth.verify_password(password, user.hashed_password):
        return False
    return user