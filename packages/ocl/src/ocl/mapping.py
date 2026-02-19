from typing import TypedDict, Callable, Any, NotRequired

from pydantic import BaseModel

type MappingFuncType = Callable[[Any, type[BaseModel]], Any]


class Mapping(TypedDict):
    key: str
    to: str
    to_func: NotRequired[MappingFuncType]


class MappingDict(TypedDict):
    source_model: type[BaseModel]
    target_model: type[BaseModel]
    mappings: list[Mapping]


def get_value_from_key_path(path: str, obj: dict) -> Any | None:
    x = obj
    for key in path.split("."):
        x = x.get(key)
        if x is None:
            break
    return x


def set_value_from_key_path(path: str, value: Any, obj: dict):
    x = obj
    for i, key in enumerate(path.split(".")):
        if i < len(path.split(".")) - 1:
            x = x.setdefault(key, dict())
        else:
            x[key] = value


def get_source_array_value(
        from_chunks: list[str],
        to_chunks: list[str],
        source: dict,
        target: dict,
        chunk_index: int,
):
    if chunk_index < len(from_chunks) - 1:
        source_array = get_value_from_key_path(from_chunks[chunk_index], source)
        target_array = get_value_from_key_path(to_chunks[chunk_index], target)
        a = []
        if source_array is not None:
            if not isinstance(source_array, list):
                source_array = [source_array]
            for i, source_element in enumerate(source_array):
                a.append(get_source_array_value(
                    from_chunks,
                    to_chunks,
                    source_element,
                    target_array[i] if target_array is not None and len(target_array) > 0 else {},
                    chunk_index + 1,
                ))
            return a
    else:
        v = get_value_from_key_path(from_chunks[chunk_index], source)
        # might need to run function here instead
        if v is not None:
            set_value_from_key_path(to_chunks[chunk_index], v, target)
        return target


def convert_model(source, mapping_dict: MappingDict):
    # TODO: implement better typing with generics

    if not isinstance(source, mapping_dict["source_model"]):
        raise ValueError(f"Invalid input model - expecting instance of {str(mapping_dict["source_model"])}")

    source_dict = source.model_dump()
    obj: dict[str, Any] = {}

    # sort by increasing "to" path depth, then alphabetically
    for mapping in sorted(mapping_dict["mappings"], key=lambda m: (len(m["to"].split(".")), m["to"])):
        if "@." in mapping["key"]:
            from_chunks = mapping["key"].split("@.")

            if "@." not in mapping["to"]:
                raise ValueError("@ array flag must also be used in 'to' path")

            to_chunks = mapping["to"].split("@.")

            if len(to_chunks) != len(from_chunks):
                raise ValueError("Unequal number of arrays in key paths")

            # returns array value of top-level path chunk
            value = get_source_array_value(from_chunks, to_chunks, source_dict, obj, 0)
            if mapping.get("to_func"):
                value = mapping["to_func"](value, source)
            # TODO: might need before & after hook
            if value is not None:
                set_value_from_key_path(to_chunks[0], value, obj)

        else:
            # TODO: handle root object
            value = get_value_from_key_path(mapping["key"], source_dict)
            if mapping.get("to_func"):
                value = mapping["to_func"](value, source)
            if value is not None:
                set_value_from_key_path(mapping["to"], value, obj)

    return mapping_dict["target_model"].model_validate(obj)


class SourceModel(BaseModel):
    source_nested_dict: dict
    source_str: str


class TargetModel(BaseModel):
    target_nested_dict: dict
    target_str: str
