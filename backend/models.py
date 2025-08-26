from pydantic import BaseModel
from typing import Optional

class BannerItem(BaseModel):
    id: str
    title: str
    subtitle: str
    imageUrl: str
    tag: str
    color: str

class ContentItem(BaseModel):
    id: str
    title: str
    price: int
    originalPrice: Optional[int] = None
    rating: float
    imageUrl: str
    category: str
    isNew: Optional[bool] = False
    isSale: Optional[bool] = False
    isRecommended: Optional[bool] = False