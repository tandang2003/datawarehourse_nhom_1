from dataclasses import dataclass
from datetime import datetime


@dataclass
class EstateEntity:
    id: str
    natural_id: str
    subject: str
    start_date: datetime
    end_date: datetime
    width: float
    height: float
    area: float
    area_used:float
    price: float
    address: str
