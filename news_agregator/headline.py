from dataclasses import dataclass
from datetime import datetime


@dataclass
class Headline:
    """Information about news."""

    source: str
    url: str
    title: str
    release_time: datetime
