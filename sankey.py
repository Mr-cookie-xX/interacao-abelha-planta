import pandas as pd
import plotly.graph_objects as go
from functools import cached_property
from typing_extensions import List, Dict, Any, Self

class SankeyGraph:
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
            "pad" : 15,
            "thickness" : 20,
            "color" : ["red","pink", "blue", "blue", "green", "yellow"],
            "line" : {
                "color" : "pink",
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
            'source' : source,
            'target' : target,
            'value'  : values,
        }
        
        return link

    def graph(self, **kwargs) -> go.Figure:
        fig = go.Figure(data=[go.Sankey(node=self.node, link=self.link)])
        kwargs = {
            "title_text": "Interacao das abelhas com as flores",
            "font_size": 10,
            **kwargs,
        }
        fig.update_layout(**kwargs)
        return fig

    def write_html(self, file: str, **kwargs) -> None:
        fig = self.graph(**kwargs)
        fig.write_html(file)
