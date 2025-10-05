from dataclasses import dataclass


@dataclass
class ErrorResponse:
    error: str

    def to_dict(self) -> dict:
        return {'error': self.error}
