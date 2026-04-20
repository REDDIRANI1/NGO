from pydantic import BaseModel


class DashboardOut(BaseModel):
    month: str
    total_ngos_reporting: int
    total_people_helped: int
    total_events_conducted: int
    total_funds_utilized: float

