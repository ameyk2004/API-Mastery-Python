from fastapi import Depends, HTTPException, status, APIRouter
from .. import schemas, models, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags = ["Authentication Routes"]
)

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="email Not Found")
    
    verifcation = utils.verify(user_credentials.password, user.password)

    if not verifcation:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="incorrect Password")

    return {"token" : "Your Token"}
    

