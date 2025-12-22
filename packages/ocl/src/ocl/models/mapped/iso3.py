from typing import Annotated, Any

from pydantic import RootModel, Field, AliasPath, BeforeValidator, model_validator

class ISO3(RootModel):
    root: dict
