from dataclasses import dataclass
from typing import List


@dataclass
class AnalysisResponse:
    position: str
    skills: List[str]
    description: str

    def to_dict(self) -> dict:
        return {
            'position': self.position,
            'skills': self.skills,
            'description': self.description
        }
