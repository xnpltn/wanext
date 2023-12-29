from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pwd(password) -> str:
    return pwd_context.hash(password)


def verify_pwd(plain: str| None = None, hashed: str| None = None) -> bool:
    return pwd_context.verify(plain, hashed)
