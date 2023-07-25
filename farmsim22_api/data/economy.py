import pydantic
import typing
import os.path
import defusedxml.ElementTree

class Crop(pydantic.BaseModel):
    periods: typing.List[int]


class Economy(pydantic.BaseModel):
    crops: typing.Dict[str, Crop]


def get_economy(save_game: str) -> Economy:
    """Retrieves information on the economy in the loaded map of the given save file

    Parameters
    ----------
    save_game : str
        directory containing all save game information files

    Returns
    -------
    Economy
        class containing information regarding economy status
    """
    _economy_file: str = os.path.join(save_game, "economy.xml")

    if not os.path.exists(_economy_file):
        raise FileNotFoundError(f"Failed to find economy file at '{_economy_file}'")

    _data = defusedxml.ElementTree.parse(_economy_file)

    return Economy(
        crops={crop.get("fillType"): Crop(periods=[int(i.text) for i in crop[0]]) for crop in _data.getroot()[0]}
    )
