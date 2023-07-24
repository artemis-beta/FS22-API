import pydantic
import typing
import os.path
import defusedxml.ElementTree

class Field(pydantic.BaseModel):
    id: int
    plannedFruit: str


def get_fields(save_game: str) -> typing.Dict[str, Field]:
    """Retrieves information on the fields in the loaded map of the given save file

    Parameters
    ----------
    save_game : str
        directory containing all save game information files
    """
    _fields_file: str = os.path.join(save_game, "fields.xml")

    if not os.path.exists(_fields_file):
        raise FileNotFoundError(f"Failed to find fields file at '{_fields_file}'")

    _data = defusedxml.ElementTree.parse(_fields_file)

    _fields: typing.Dict[int, Field] = {
        int(field.get("id")): Field(**{k: field.get(k) for k in Field.model_fields.keys()})
        for field in _data.getroot()
    }

    return _fields