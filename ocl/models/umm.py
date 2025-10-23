from pydantic import BaseModel


class UMM(BaseModel):
    title: str

    def model_dump_iso4_json(self) -> str:
        return self.model_dump_json()
