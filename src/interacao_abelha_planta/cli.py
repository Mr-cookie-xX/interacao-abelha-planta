import click
from datetime import date
from .images import ImageGenerator


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
    pages: int = 1,
    to_folder: str | None = None,
) -> None:
    to_folder = (
        to_folder if to_folder else f'images/{date.today().strftime("%Y-%m-%d")}'
    )
    generator = ImageGenerator.from_datafile(filename=filename)
    generator.generate(to_folder=to_folder, pages=pages)


if __name__ == "__main__":
    cli()
