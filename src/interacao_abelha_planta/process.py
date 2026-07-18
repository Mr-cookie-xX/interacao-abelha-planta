import pandas as pd
from pathlib import Path
from functools import cached_property
from typing import List, Literal, Self, Iterator, Tuple


class InteractionDataProcessor:
    """
    Process interaction data and export interaction matrices.
    Graph building is delegated to external classes (e.g., SankeyGraph).
    """

    def __init__(
        self,
        *,
        df: pd.DataFrame,
        group_by: Literal["flor", "abelha"] = "flor",
    ) -> None:
        self._df = df
        self.group_by = group_by

    @classmethod
    def from_datafile(
        cls,
        filename: str,
        group_by: Literal["flor", "abelha"] = "flor",
    ) -> Self:
        df = pd.read_csv(filename, header=0)
        return cls(df=df, group_by=group_by)

    @cached_property
    def df(self) -> pd.DataFrame:
        rename = {
            "Spp. de abelha": "abelha",
            "Spp. da flor": "flor",
        }

        df = self._df.rename(columns=rename, errors="raise")
        df = df[list(rename.values())]

        df["abelha"] = df["abelha"].astype(str).str.strip().str.capitalize()
        df["flor"] = df["flor"].astype(str).str.strip().str.capitalize()

        return df.dropna().drop_duplicates().reset_index(drop=True)

    @cached_property
    def df_count(self) -> pd.DataFrame:
        return (
            self.df.groupby(by=self.group_by)
            .size()
            .rename("count")
            .sort_values(ascending=False)
            .to_frame()
        )

    def _split_data_into_pages(self, pages: int) -> List[pd.DataFrame]:
        if pages <= 1:
            return [self.df]

        total = self.df_count["count"].sum()
        target = total / pages

        boundaries = []
        running = 0

        for idx, count in self.df_count["count"].items():
            running += count
            if running >= target and len(boundaries) < pages - 1:
                boundaries.append(idx)
                running = 0

        page_keys = []
        start = 0
        for b in boundaries:
            end = self.df_count.index.get_loc(b) + 1
            page_keys.append(self.df_count.index[start:end])
            start = end
        page_keys.append(self.df_count.index[start:])

        return [self.df[self.df[self.group_by].isin(keys)] for keys in page_keys]

    def _build_matrix_for_page(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.group_by == "flor":
            rows = df["flor"].unique()
            cols = df["abelha"].unique()
            row_col = ("flor", "abelha")
        else:
            rows = df["abelha"].unique()
            cols = df["flor"].unique()
            row_col = ("abelha", "flor")

        matrix = pd.DataFrame(0, index=rows, columns=cols)

        for r, c in df[list(row_col)].itertuples(index=False):
            matrix.at[r, c] = 1

        return matrix[matrix.sum().sort_values(ascending=False).index]

    def build_matrix(self) -> pd.DataFrame:
        return self._build_matrix_for_page(df=self.df)

    def paginate(self, pages: int = 1) -> Iterator[Tuple[int, pd.DataFrame]]:

        dfs = self._split_data_into_pages(pages=pages)

        for i, df in enumerate(dfs):
            yield i, self._build_matrix_for_page(df=df)

    def export_csvs(self, to_folder: Path) -> None:
        self.df.to_csv(
            path_or_buf=to_folder / "interacoes-unicas.csv",
            index=True,
            header=True,
            sep=",",
        )

        self.df_count.to_csv(
            path_or_buf=to_folder / "count.csv",
            index=True,
            header=True,
            sep=",",
        )
