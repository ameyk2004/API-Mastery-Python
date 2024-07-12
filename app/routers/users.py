from fastapi import Depends, HTTPException, status, APIRouter
from .. import schemas, models, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/users')



@router.post('/', status_code=status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    password = utils.hash(user.password)

    new_user = models.User(name=user.name, email=user.email, password=password,)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/')
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return {"users" : users}

@router.get('/{id}', response_model= schemas.UserOut)
def get_one_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Id {id} not found")

    return user
    