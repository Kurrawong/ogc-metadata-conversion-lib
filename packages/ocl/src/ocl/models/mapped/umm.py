from typing import Annotated, Any

from pydantic import RootModel, Field, AliasPath, BeforeValidator, model_validator

class UMM(RootModel):
    root: dict
