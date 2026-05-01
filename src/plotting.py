from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def save_celltype_composition_heatmap(
    composition_df: pd.DataFrame,
    output_path: str
) -> None:
    plot_df = composition_df.set_index("spot_id")

    fig, ax = plt.subplots(figsize=(8, 4.5))
    im = ax.imshow(plot_df.values, aspect="auto")
    ax.set_xticks(range(len(plot_df.columns)))
    ax.set_xticklabels(plot_df.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(plot_df.index)))
    ax.set_yticklabels(plot_df.index)
    ax.set_title("Spot-level cell type composition")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def save_region_barplot(
    region_summary_df: pd.DataFrame,
    output_path: str
) -> None:
    plot_df = region_summary_df.set_index("region")

    fig, ax = plt.subplots(figsize=(9, 5))
    plot_df.plot(kind="bar", ax=ax)
    ax.set_title("Mean cell type composition by region")
    ax.set_ylabel("Mean proportion")
    ax.set_xlabel("Region")
    ax.legend(title="Cell type", bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)