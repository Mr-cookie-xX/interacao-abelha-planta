import click
from pathlib import Path
from datetime import date
from shutil import rmtree

from .sankey import SankeyGraph
from .heatmap import HeatmapRenderer
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
def generate_images(
    filename: str,
    group_by: str = "flor",
    pages: int = 1,
    to_folder: str | None = None,
) -> None:
    target = to_folder if to_folder else f"images/{date.today().strftime('%Y-%m-%d')}"

    target = Path(target)

    rmtree(target, ignore_errors=True)

    target.mkdir(exist_ok=True, parents=True)

    processor = InteractionDataProcessor.from_datafile(
        filename=filename,
        group_by=group_by,
    )

    processor.export_csvs(to_folder=target)

    heatmap = HeatmapRenderer()

    heatmap.write_image(df=processor.build_matrix(), file=target / "heatmap.png")

    sankey = SankeyGraph()

    for i, df in processor.paginate(pages=pages):

        file = target / f"matriz-interacoes-{i}"

        df.to_csv(
            path_or_buf=file.with_suffix(".csv"),
            sep="|",
            header=True,
            index=True,
        )

        sankey.write_html(
            df=df,
            file=file.with_suffix(".html"),
        )
        sankey.write_image(
            df=df,
            file=file.with_suffix(".png"),
        )

        heatmap.render(df=df)


if __name__ == "__main__":
    cli()
