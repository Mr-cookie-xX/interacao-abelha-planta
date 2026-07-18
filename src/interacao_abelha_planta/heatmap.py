import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Optional


@dataclass
class HeatmapTheme:
    cmap: str = "viridis"
    figsize: tuple[int, int] = (12, 10)
    dpi: int = 300
    annot: bool = False
    linewidths: float = 0.1
    title: Optional[str] = "Interações: Flores x Abelhas"
    xtick_rotation: int = 90
    ytick_rotation: int = 0


class HeatmapRenderer:
    """
    Render interaction matrices as publication-quality heatmaps.
    """

    def __init__(self, theme: Optional[HeatmapTheme] = None):
        self.theme = theme or HeatmapTheme()

    def render(self, df: pd.DataFrame, **kwargs):
        theme = self.theme

        plt.figure(figsize=theme.figsize)

        sns.heatmap(
            df,
            cmap=theme.cmap,
            annot=theme.annot,
            linewidths=theme.linewidths,
            **kwargs,
        )

        if theme.title:
            plt.title(theme.title)

        plt.xticks(rotation=theme.xtick_rotation)
        plt.yticks(rotation=theme.ytick_rotation)

        plt.tight_layout()
        return plt

    def write_image(self, df: pd.DataFrame, file: str, **kwargs):
        plt_obj = self.render(df=df, **kwargs)
        plt_obj.savefig(fname=file, dpi=self.theme.dpi)
        plt_obj.close()
