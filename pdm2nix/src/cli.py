
import click
from pdm2nix.src.configuration import generate_configuration

@click.command()
@click.argument("pdm_project_path", type=str)
@click.argument("group", type=str, default="default")
def pdm2nix(pdm_project_path: str, group: str) -> None:
    generate_configuration(pdm_project_path, group)
