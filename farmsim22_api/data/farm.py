import pydantic
import defusedxml.ElementTree
import typing
import os.path


class FinancialStats(pydantic.BaseModel):
    newVehiclesCost: float
    soldVehicles: float
    newAnimalsCost: float
    soldAnimals: float
    constructionCost: float
    soldBuildings: float
    fieldPurchase: float
    fieldSelling: float
    vehicleRunningCost: float
    vehicleLeasingCost: float
    propertyMaintenance: float
    propertyIncome: float
    productionCosts: float
    soldWood: float
    soldBales: float
    soldWool: float
    soldMilk: float
    soldProducts: float
    purchaseFuel: float
    purchaseSeeds: float
    purchaseFertilizer: float
    purchaseSaplings: float
    purchaseWater: float
    purchaseBales: float
    purchasePallets: float
    harvestIncome: float
    incomeBga: float
    missionIncome: float
    wagePayment: float
    other: float
    loanInterest: float


class Player(pydantic.BaseModel):
    uniqueUserId: str
    lastNickname: str
    timeLastConnected: str
    buyVehicle: bool
    sellVehicle: bool
    buyPlaceable: bool
    sellPlaceable: bool
    manageContracts: bool
    tradeAnimals: bool
    createFields: bool
    landscaping: bool
    hireAssistant: bool
    resetVehicle: bool
    manageProductions: bool
    cutTrees: bool
    manageRights: bool
    transferMoney: bool
    updateFarm: bool
    manageContracting: bool


class Statistics(pydantic.BaseModel):
    traveledDistance: float
    fuelUsage: float
    seedUsage: float
    sprayUsage: float
    workedHectares: float
    cultivatedHectares: float
    sownHectares: float
    sprayedHectares: float
    threshedHectares: float
    plowedHectares: float
    harvestedGrapes: float
    harvestedOlives: float
    workedTime: float
    cultivatedTime: float
    sownTime: float
    sprayedTime: float
    threshedTime: float
    plowedTime: float
    baleCount: int
    breedCowsCount: int
    breedSheepCount: int
    breedPigsCount: int
    breedChickenCount: int
    breedHorsesCount: int
    fieldJobMissionCount: int
    fieldJobMissionByNPC: int
    transportMissionCount: int
    revenue: float
    expenses: float
    playTime: float
    plantedTreeCount: int
    cutTreeCount: int
    woodTonsSold: float
    treeTypesCut: int
    petDogCount: int
    repairVehicleCount: int
    repaintVehicleCount: int
    horseJumpCount: int
    soldCottonBales: int
    wrappedBales: int
    tractorDistance: float
    carDistance: float
    truckDistance: float
    horseDistance: float
    numRollercoasterRides: int
    forestryMissionCount: int


class Farm(pydantic.BaseModel):
    name: str
    farmId: int
    color: int
    loan: float
    money: float
    players: typing.List[Player]
    statistics: Statistics
    finances: typing.List[FinancialStats]


def get_farms(save_game: str) -> typing.Dict[int, Farm]:
    """Retrieves information on the farms in the loaded map of the given save file

    Parameters
    ----------
    save_game : str
        directory containing all save game information files
    """
    _farms_file: str = os.path.join(save_game, "farms.xml")

    if not os.path.exists(_farms_file):
        raise FileNotFoundError(f"Failed to find farms file at '{_farms_file}'")

    _data = defusedxml.ElementTree.parse(_farms_file)

    _farms: typing.Dict[int, Farm] = {}
    
    for farm in _data.getroot():
        _players = farm[0]
        _stats = farm[1]
        _finances = farm[2]

        _player_models: typing.List[Player] = [
            Player(**{k: player.get(k) for k in Player.model_fields.keys()})
            for player in _players
        ]
        _stats = Statistics(
            **{s.tag: s.text for s in _stats}
        )
        _finances: typing.List[FinancialStats] = [
            FinancialStats(**{s.tag: s.text for s in day})
            for day in _finances
        ]

        _farms[farm.get("farmId")] = Farm(
            **{k: farm.get(k) for k in Farm.model_fields.keys() if farm.get(k)} | {"finances": _finances, "players": _player_models, "statistics": _stats}
        )

    return _farms

