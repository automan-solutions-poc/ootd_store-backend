import time
import httpx
from typing import Optional, Dict, Any
from app.core.config import settings
from app.core.logging import logger

class QikinkService:
    _token: Optional[str] = None
    _token_expiry: float = 0

    @classmethod
    async def _get_token(cls) -> str:
        if cls._token and time.time() < cls._token_expiry - 60:
            return cls._token

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{settings.QIKINK_API_URL}/api/token",
                    json={
                        "api_key": settings.QIKINK_API_KEY,
                        "api_secret": settings.QIKINK_API_SECRET
                    }
                )
                response.raise_for_status()
                data = response.json()
                cls._token = data["access_token"]
                cls._token_expiry = time.time() + data.get("expires_in", 3600)
                return cls._token
            except Exception as e:
                logger.error("qikink_token_error", error=str(e))
                raise

    @classmethod
    async def create_order(cls, order_data: Dict[str, Any]) -> Optional[str]:
        token = await cls._get_token()
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{settings.QIKINK_API_URL}/api/order/create",
                    headers={"Authorization": f"Bearer {token}"},
                    json=order_data
                )
                response.raise_for_status()
                data = response.json()
                return data.get("qikink_order_id")
            except Exception as e:
                logger.error("qikink_order_create_error", error=str(e), order_data=order_data)
                return None
