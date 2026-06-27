"""Schemas describing the dashboard response."""

from datetime import datetime

from pydantic import BaseModel


class CustomersByStatus(BaseModel):
    prospect: int
    active: int
    at_risk: int
    churned: int


class SentimentBreakdown(BaseModel):
    positive: int
    neutral: int
    negative: int


class RecentInteraction(BaseModel):
    id: int
    customer_id: int
    type: str
    title: str
    occurred_at: datetime


class DashboardResponse(BaseModel):
    total_customers: int
    customers_by_status: CustomersByStatus
    at_risk_customers: int
    total_interactions: int
    interactions_last_7_days: int
    sentiment_breakdown: SentimentBreakdown
    recent_interactions: list[RecentInteraction]
