import pandas as pd
from dataclasses import dataclass
import plotly.graph_objects as go
from typing import List, Optional, Self


@dataclass
class SankeyData:
    labels: List[str]
    node_colors: List[str]
    source: List[int]
    target: List[int]
    values: List[int]


@dataclass
class SankeyTheme:
    title: str = "Interações: Flores x Abelhas"
    color_left: str = "#79E353"
    color_right: str = "#DB7500"
    line_color: str = "#000000"
    font_family: str = "Comic Sans"
    font_color: str = "#000000"
    font_size: int = 10


class SankeyDataBuilder:
    """
    Converts a matrix (flowers x bees or vice‑versa)
    into Sankey node/link structures.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def build(self, theme: SankeyTheme) -> SankeyData:
        labels = self.df.index.to_list() + self.df.columns.to_list()

        node_colors = [theme.color_left for _ in self.df.index] + [
            theme.color_right for _ in self.df.columns
        ]

        source = []
        target = []
        values = []

        for i, row in enumerate(self.df.index):
            for j, col in enumerate(self.df.columns):
                source.append(i)
                target.append(len(self.df.index) + j)
                values.append(int(self.df.loc[row, col]))

        return SankeyData(
            labels=labels,
            node_colors=node_colors,
            source=source,
            target=target,
            values=values,
        )


class SankeyRenderer:
    """
    Responsible only for rendering SankeyData using Plotly.
    """

    def render(self, data: SankeyData, theme: SankeyTheme, **kwargs) -> go.Figure:
        node = {
            "pad": 5,
            "thickness": 20,
            "color": data.node_colors,
            "line": {"color": theme.line_color, "width": 0.5},
            "label": data.labels,
        }

        link = {
            "source": data.source,
            "target": data.target,
            "value": data.values,
        }

        fig = go.Figure(data=[go.Sankey(node=node, link=link)])

        layout = {
            "title_text": theme.title,
            "font": {
                "color": theme.font_color,
                "family": theme.font_family,
                "size": theme.font_size,
            },
            "margin": {"l": 10, "r": 10, "t": 30, "b": 20},
            **kwargs,
        }

        fig.update_layout(**layout)
        return fig


class SankeyGraph:

    def __init__(
        self,
        df: pd.DataFrame,
        theme: Optional[SankeyTheme] = None,
        renderer: Optional[SankeyRenderer] = None,
    ):
        self.df = df
        self.theme = theme or SankeyTheme()
        self.renderer = renderer or SankeyRenderer()

    @classmethod
    def from_file(cls, file: str, sep: str = "|", limit: Optional[int] = None) -> Self:
        df = pd.read_csv(
            file,
            sep=sep,
            header=0,
            index_col=0,
        )
        if limit:
            df = df.head(limit)
        return cls(df=df)

    def build_data(self) -> SankeyData:
        return SankeyDataBuilder(self.df).build(self.theme)

    def figure(self, **kwargs) -> go.Figure:
        data = self.build_data()
        return self.renderer.render(data, self.theme, **kwargs)

    def to_html(self, **kwargs) -> str:
        return self.figure(**kwargs).to_html()

    def to_image(self, **kwargs):
        return self.figure(**kwargs).to_image(format="png")

    def write_image(self, file: str, **kwargs) -> None:
        fig = self.figure(**kwargs)
        fig.write_image(file=file, scale=2, width=600, height=800)

    def write_html(self, file: str, **kwargs) -> None:
        fig = self.figure(**kwargs)
        fig.write_html(file)
