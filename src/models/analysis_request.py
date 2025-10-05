from dataclasses import dataclass
from typing import List


@dataclass
class AnalysisRequest:
    position: str
    skills: List[str]

    @classmethod
    def from_dict(cls, data: dict) -> 'AnalysisRequest':
        return cls(
            position=data.get('position', ''),
            skills=data.get('skills', [])
        )
