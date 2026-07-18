import click
from pathlib import Path
from datetime import date
from shutil import rmtree

from .sankey import SankeyGraph
from .process import InteractionDataProcessor


@click.group(
    help="Biblioteca base para análise dos dados de interação das abelhas com as plantas.",
)
def cli() -> None: ...


@cli.command(
    help="Comando para geração das imagens de interação de Plantas x Abelhas.",
)
@click.option(
    "--filename",
    help="Nome do arquivo de dados original. Deve conter pelo menos as colunas `Spp. de abelha` e `Spp. da flor`",
)
@click.option(
    "--group-by",
    default="flor",
    help="Indica qual será a relação de agrupamento para considerar o balanceamento das páginas.",
)
@click.option(
    "--pages",
    default=1,
    help="Número de páginas nas quais os dados serão divididos (agrupando pela quantidade de interações únicas). Opcional. Por padrão, os dados são salvos em uma única página.",
)
@click.option(
    "--to-folder",
    default=None,
    help="Diretório para os arquivos de destino. Opcional. Por padrão, os arquivos serão guardados numa pasta `image` com a data atual",
)
def generate_images_from_datafile(
    filename: str,
    group_by: str = "flor",
    pages: int = 1,
    to_folder: str | None = None,
) -> None:
    target = to_folder if to_folder else f'images/{date.today().strftime("%Y-%m-%d")}'

    target = Path(target)

    rmtree(target, ignore_errors=True)

    target.mkdir(exist_ok=True, parents=True)

    processor = InteractionDataProcessor.from_datafile(
        filename=filename, group_by=group_by
    )

    files = processor.export(to_folder=target, pages=pages)

    for file in files:
        graph = SankeyGraph.from_file(file=file, sep="|")
        graph.write_html(file=file.with_suffix(".html"))
        graph.write_image(file=file.with_suffix(".png"))


if __name__ == "__main__":
    cli()
