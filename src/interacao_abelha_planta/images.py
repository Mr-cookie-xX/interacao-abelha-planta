import os
import pandas as pd
from pathlib import Path
from shutil import rmtree
from functools import cached_property
from typing_extensions import List, Self

from .sankey import SankeyGraph


class ImageGenerator:
    def __init__(self, *, df: pd.DataFrame) -> None:
        rename = {
            "Spp. de abelha": "abelha",
            "Spp. da flor": "flor",
        }
        df_renamed = df.rename(columns=rename)[[*rename.values()]]
        df_renamed["abelha"] = df_renamed["abelha"].str.capitalize()
        df_renamed["flor"] = df_renamed["flor"].str.capitalize()
        self._df = df_renamed.dropna().drop_duplicates().reset_index(drop=True)

    @classmethod
    def from_datafile(cls, filename: str) -> Self:
        df = pd.read_csv(filepath_or_buffer=filename, header=0)
        return cls(df=df)

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @cached_property
    def df_count(self) -> pd.DataFrame:
        return (
            self.df.groupby(["flor"])
            .count()
            .rename({"abelha": "count"}, axis=1)
            .sort_values(by=["count"], ascending=False)
        )

    def split_data_into_pages(self, pages: int) -> List[pd.DataFrame]:
        if pages <= 1:
            return [self.df]

        i = 0
        size = 0
        indexes = []

        max_size = self.df_count.sum(axis=0).iloc[0] / pages

        for _, row in self.df_count.iterrows():
            size += row["count"]
            i += 1
            if size >= max_size:
                indexes.append(i)
                size = 0

        if not indexes:
            return [self.df]

        bounds = [0] + indexes + [None]

        tuples = [(bounds[j], bounds[j + 1]) for j in range(len(bounds) - 1)]

        dfs = [
            self.df[self.df["flor"].isin(self.df_count.iloc[x:y].index)]
            for x, y in tuples
        ]

        return dfs

    def generate(self, to_folder: str | Path, pages: int = 1) -> None:

        to_folder = Path(to_folder) if isinstance(to_folder, str) else to_folder

        rmtree(path=to_folder, ignore_errors=True)

        os.makedirs(name=to_folder, exist_ok=True)

        self.df.to_csv(
            path_or_buf=to_folder / "interacoes-unicas.csv",
            mode="w",
            header=True,
            index=False,
            sep=",",
        )

        dfs = self.split_data_into_pages(pages=pages)

        for i in range(len(dfs)):

            df_interacoes = pd.DataFrame(
                0,
                index=dfs[i]["flor"].drop_duplicates().to_list(),
                columns=dfs[i]["abelha"].drop_duplicates().to_list(),
            )

            for _, row in dfs[i].iterrows():
                df_interacoes.at[row["flor"], row["abelha"]] = 1

            df_interacoes = df_interacoes[
                df_interacoes.sum().sort_values(ascending=False).index
            ]

            df_interacoes.to_csv(
                path_or_buf=to_folder / f"matriz_interacoes-{i}.csv",
                sep="|",
                header=True,
                index=True,
            )

            graph = SankeyGraph(df=df_interacoes)

            graph.write_html(file=to_folder / f"interacoes-{i}.html")

            graph.write_image(file=to_folder / f"interacoes-{i}.png")
