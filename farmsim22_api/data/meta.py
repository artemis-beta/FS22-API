import pydantic
import typing
import os.path
import defusedxml.ElementTree

class Settings(pydantic.BaseModel):
    savegameName: str
    creationDate: str
    mapId: str
    mapTitle: str
    saveDateFormatted: str
    saveDate: str
    resetVehicles: bool
    trafficEnabled: bool
    stopAndGoBraking: bool
    trailerFillLimit: bool
    automaticMotorStartEnabled: bool
    growthMode: int
    plannedDaysPerPeriod: int
    fruitDestruction: bool
    plowingRequiredEnabled: bool
    stonesEnabled: bool
    weedsEnabled: bool
    limeRequired: bool
    isSnowEnabled: bool
    fuelUsage: int
    helperBuyFuel: bool
    helperBuySeeds: bool
    helperBuyFertilizer: bool
    helperSlurrySource: int
    helperManureSource: int
    densityMapRevision: int
    terrainTextureRevision: int
    terrainLodTextureRevision: int
    splitShapesRevision: int
    tipCollisionRevision: int
    placementCollisionRevision: int 
    navigationCollisionRevision: int
    mapDensityMapRevision: int 
    mapTerrainTextureRevision: int
    mapTerrainLodTextureRevision: int
    mapSplitShapesRevision: int
    mapTipCollisionRevision: int
    mapPlacementCollisionRevision: int 
    mapNavigationCollisionRevision: int
    difficulty: int 
    economicDifficulty: int
    dirtInterval: int
    timeScale: float
    autoSaveInterval: float


class Statistics(pydantic.BaseModel):
    money: int
    playTime: float


class Mod(pydantic.BaseModel):
    modName: str
    title: str
    version: str
    required: bool
    fileHash: str


class GuidedTour(pydantic.BaseModel):
    active: bool
    currentStepIndex: int
    state: str | None

class Metadata(pydantic.BaseModel):
    mods: typing.Dict[str, Mod]
    statistics: Statistics
    guided_tour: GuidedTour
    settings: Settings


def get_career_data(save_game: str) -> Metadata:
    """Retrieves information on the career save

    Parameters
    ----------
    save_game : str
        directory containing all save game information files
    
    Returns
    -------
    Dict[int, Farm]
        dictionary with classes containing information regarding status of each farm
    """
    _save_meta_file: str = os.path.join(save_game, "careerSavegame.xml")

    if not os.path.exists(_save_meta_file):
        raise FileNotFoundError(f"Failed to find economy file at '{_save_meta_file}'")

    _data = defusedxml.ElementTree.parse(_save_meta_file).getroot()
    
    _settings = _data[0]
    _tour = _data[1]
    _stats = _data[3]

    _settings_model = Settings(**{
        k.tag: k.text for k in _settings
    })

    _tour_model = GuidedTour(
        **{k: _tour.get(k) for k in GuidedTour.model_fields.keys()}
    )

    _stats_model = Statistics(**{
        k.tag: k.text for k in _stats
    })

    _mods = {k.get("title"): Mod(**{n: k.get(n) for n in Mod.model_fields.keys()}) for k in _data[6:]}

    return Metadata(
        mods=_mods,
        statistics=_stats_model,
        settings=_settings_model,
        guided_tour=_tour_model
    )