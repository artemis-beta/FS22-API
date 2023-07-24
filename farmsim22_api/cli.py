import click
import typing
import os.path
import glob
import re

import farmsim22_api.vehicle_roster as fs22_vec
import farmsim22_api.fields as fs22_field
import farmsim22_api.farm as fs22_farm

@click.group("farmsim")
@click.argument("save_dir", type=click.Path(exists=True))
@click.option("--save", type=int, default=None)
@click.pass_context
def main(ctx: typing.Dict, save_dir: str, save: int | None) -> None:
    ctx.ensure_object(dict)
    if not save:
        _save_dirs = glob.glob(os.path.join(save_dir, "savegame*"))

        if not _save_dirs:
            raise FileNotFoundError(f"No save games found in {save_dir}")
        
        _save_dirs = list(i for i in sorted(_save_dirs) if os.path.exists(os.path.join(i, "sales.xml")))

        if not _save_dirs:
            raise FileNotFoundError("No save sessions found")
        _save_dir = _save_dirs[-1]
    else:
        if not os.path.exists(_save_dir := os.path.join(save_dir, f"savegame{save}")):
            raise FileNotFoundError(f"No such file '{_save_dir}'")
    ctx.obj["SAVE_DIR"] = _save_dir


@main.command
@click.pass_context
def vehicles(ctx: typing.Dict) -> None:
    _vehicles = fs22_vec.get_vehicles(ctx.obj["SAVE_DIR"])
    print(_vehicles)

@main.command
@click.pass_context
def fields(ctx: typing.Dict) -> None:
    _fields = fs22_field.get_fields(ctx.obj["SAVE_DIR"])
    print(_fields)

@main.command
@click.pass_context
def farms(ctx: typing.Dict) -> None:
    _farms = fs22_farm.get_farms(ctx.obj["SAVE_DIR"])
    print(_farms)


if __name__ in "__main__":
    main()
