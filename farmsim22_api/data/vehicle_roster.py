import os
import typing
import defusedxml.ElementTree
import pydantic


class Vehicle(pydantic.BaseModel):
    timeLeft: int
    isGenerated: bool
    xmlFilename: str
    age: int
    price: int
    damage: float
    wear: float
    operatingTime: float

    @pydantic.validator("xmlFilename")
    def get_rel_path(cls, file_path: str) -> str:
        if "Farming Simulator 22" in file_path:
            return file_path.split("Farming Simulator 22/")[1]
        return file_path


def get_vehicles(save_game: str) -> typing.List[Vehicle]:
    """Retrieves information on the vehicles purchased for the given save file

    Parameters
    ----------
    save_game : str
        directory containing all save game information files
    """
    _vehicle_file: str = os.path.join(save_game, "sales.xml")

    if not os.path.exists(_vehicle_file):
        raise FileNotFoundError(f"Failed to find vehicle file at '{_vehicle_file}'")

    _data = defusedxml.ElementTree.parse(_vehicle_file)

    _vehicles: typing.List[Vehicle] = []

    for vehicle in _data.getroot():
        _vehicles.append(
            Vehicle(**{k: vehicle.get(k) for k in Vehicle.model_fields.keys()})
        )

    return _vehicles
    