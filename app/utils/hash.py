from passlib.context import CryptContext

# Argon2를 사용한 CryptContext 설정
pwd_context = CryptContext(
    schemes=["argon2"],
    default="argon2",
    argon2__memory_cost=512000,  # 메모리 사용량 설정 (512MB)
    argon2__time_cost=2,         # 해시 생성에 필요한 시간 설정 (2초)
    argon2__parallelism=2,       # 병렬 처리 단위 설정 
    deprecated="auto"
)

def verify_hashed_text(plain_password: str, hashed_text: str):
    """Verify the hashed text with the plain password."""
    return pwd_context.verify(plain_password, hashed_text)

def hash_text(plain_text: str):
    """Hash the plain text."""
    return pwd_context.hash(plain_text)
