from src.models.user_model import RefreshToken
from src.utils.repository import SQLAlchemyRepository


class TokenRepository(SQLAlchemyRepository):
    model = RefreshToken
