from pydantic import BaseModel

from ocl.models.simple.iso4 import ISO4


class TrainingDML(BaseModel):
    id: str
    # title: str
    # quality

    def model_convert_iso4(self) -> ISO4:
        return ISO4(
            id=self.id
        )
