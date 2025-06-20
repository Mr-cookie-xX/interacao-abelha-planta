import pandas as pd
import plotly.graph_objects as go
from functools import cached_property
from typing_extensions import List, Dict, Any, Self

class SankeyGraph:
    """Criação de gráficos Sankey para modelos de duas colunas"""

    def __init__(self, df: pd.DataFrame):
        self._df = df

    @classmethod
    def from_file(cls, file: str, sep: str = "|", limit: int | None = None) -> Self:
        df = pd.read_csv(filepath_or_buffer=file, sep=sep, header=0, index_col=0)
        return cls(df=df.head(limit)) if limit else cls(df=df)

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @cached_property
    def labels(self) -> List[str]:
        return self.df.index.to_list() + self.df.columns.to_list()

    @cached_property
    def node(self) -> Dict[str, Any]:
        return {
            "pad" : 5,
            "thickness" : 20,
            "color" : [
                *self.df.shape[0]*["#E78413"],
                *self.df.shape[1]*["#B913D2"],
            ],
            "line" : {
                "color" : "#000000",
                "width" : 0.5,
            },
            "label" : self.labels,
        }

    @cached_property
    def link(self) -> Dict[str, List[str] | List[int]]:
        source = []
        target = []
        values = []

        for index in self.df.index:
            for col in self.df.columns:
                source.append(self.labels.index(index))
                target.append(self.labels.index(col))
                values.append(self.df.loc[index][col])

        link = {
            'source': source,
            'target': target,
            'value' : values,
            # 'color' : "#000000",
        }
        
        return link

    def graph(self, **kwargs) -> go.Figure:
        fig = go.Figure(data=[go.Sankey(node=self.node, link=self.link)])
        kwargs = {
            "title_text": "Interações: Abelhas x Flores",
            # "height": 1280,
            # "width": 720,
            "font": {
                "color": "#000000",
                "family": "Comic Sans",
                "size": 10,
                "style": "italic",
                "weight": 500,
            },
            "margin": {
                "l": 10,
                "r": 10,
                "t": 30,
                "b": 20,
            },
            **kwargs,
        }
        fig.update_layout(**kwargs)
        return fig

    def write_image(self, file: str, **kwargs) -> None:
        fig = self.graph(**kwargs)
        fig.write_image(file=file, scale=10, height=1280, width=720)

    def write_html(self, file: str, **kwargs) -> None:
        fig = self.graph(**kwargs)
        fig.write_html(file)
