from typing import List, Optional, Union, Literal

from pydantic import BaseModel

from ocl.models.simple.iso4 import ISO4


class UMM(BaseModel):
    # id
    EntryTitle: Optional[str] = None
    # quality

    def model_convert_iso4(self) -> ISO4:
        return ISO4()
