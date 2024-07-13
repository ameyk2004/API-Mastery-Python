from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

# openssl rand -hex 32 - generate SECRET

SECRET_KEY = "2a91fd44ee2581907d59553e9c2dc7f20e18b30f0f9a1394accde7e7ee2c6b12"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token, credentialexception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get("id")

        if not id: 
            raise credentialexception
        
        token_data = schemas.TokenData(id=id)

        return token_data

    except JWTError:
        raise credentialexception
    

# pass this is as a dependency in path operation
# take the token from the request
# extract the id
# verify the token
# get current user
    
def get_current_user(token: str = Depends(oauth2_schema)):
    credential_exception = HTTPException(
        detail="Could not validate", 
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate" : "Bearer"})
    
    return verify_token(token, credential_exception)
    