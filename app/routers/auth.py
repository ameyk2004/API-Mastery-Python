from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


from .. import schemas, models, utils, oath2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags = ["Authentication Routes"]
)

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="email Not Found")
    
    verifcation = utils.verify(user_credentials.password, user.password)

    if not verifcation:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="incorrect Password")

    access_token =  oath2.create_access_token({"id" : user.id})

    return {"access_token" : access_token, "token_type" : "bearer"}
    

