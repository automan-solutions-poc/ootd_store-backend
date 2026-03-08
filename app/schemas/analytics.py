from typing import List, Dict
from pydantic import BaseModel

class AnalyticsOut(BaseModel):
    total_revenue: float
    orders_count: int
    top_selling_skus: List[Dict]
    customer_order_frequency: List[Dict]

class RevenueByDate(BaseModel):
    date: str
    revenue: float

class AnalyticsRevenueOut(BaseModel):
    revenue_by_date: List[RevenueByDate]
