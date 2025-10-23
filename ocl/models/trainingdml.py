from pydantic import BaseModel


class TrainingDML(BaseModel):
    title: str

    def model_dump_umm_json(self) -> str:
        return self.model_dump_json()
