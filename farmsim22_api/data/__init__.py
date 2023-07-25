from .collectibles import get_collectibles
from .economy import get_economy, Economy
from .farm import get_farms, Farm
from .fields import get_fields, Field
from .fields import get_farmlands, Farmland
from .meta import Metadata, get_career_data

import pydantic
import typing


class Data(pydantic.BaseModel):
    economy: Economy
    farm: typing.Dict[int, Farm]
    fields: typing.Dict[int, Field]
    farmlands: typing.Dict[int, Farmland]
    collectibles: typing.Dict[int, bool]
    metadata: Metadata


def get_data(save_game: str):
    """Retrieves information on the loaded map of the given save file

    Parameters
    ----------
    save_game : str
        directory containing all save game information files
    """
    return Data(
        economy=get_economy(save_game),
        farm=get_farms(save_game),
        fields=get_fields(save_game),
        farmlands=get_farmlands(save_game),
        collectibles=get_collectibles(save_game),
        metadata=get_career_data(save_game)
    )