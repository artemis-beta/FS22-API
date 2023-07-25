import typing
import os.path
import defusedxml.ElementTree


def get_collectibles(save_game: str) -> typing.Dict[int, bool]:
    """Retrieves information on the collectibles status in the loaded map of the given save file

    Parameters
    ----------
    save_game : str
        directory containing all save game information files
    
    Returns
    -------
    Dict[int, bool]
        dictionary containing collectibles by ID and whether they have been found
    """
    _collectibles_file: str = os.path.join(save_game, "collectibles.xml")

    if not os.path.exists(_collectibles_file):
        raise FileNotFoundError(f"Failed to find collectible file at '{_collectibles_file}'")

    _data = defusedxml.ElementTree.parse(_collectibles_file)

    return {int(k.get("index")): bool(k.get("collected")) for k in _data.getroot()}
