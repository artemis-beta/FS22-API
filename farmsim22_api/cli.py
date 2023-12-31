import click
import json
import os.path
import glob

import farmsim22_api.data

@click.command("farmsim")
@click.argument("save_dir", type=click.Path(exists=True))
@click.option("--save", type=int, default=None)
@click.option("--output", type=click.Path(exists=False), default=None)
def main(save_dir: str, save: int | None, output: str | None) -> None:
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
    if not output:
        output = f"{os.path.basename(_save_dir)}.json"

    with open(output, "w") as out_f:
        json.dump(farmsim22_api.data.get_data(_save_dir).model_dump(), out_f, indent=2)


if __name__ in "__main__":
    main()
