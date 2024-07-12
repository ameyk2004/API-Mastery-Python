from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas

#SECRET KEY
#Algo
#Expiration Time

# openssl rand -hex 32 - generate SECRET

SECRET_KEY = "2a91fd44ee2581907d59553e9c2dc7f20e18b30f0f9a1394accde7e7ee2c6b12"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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

    except JWTError:
        raise credentialexception