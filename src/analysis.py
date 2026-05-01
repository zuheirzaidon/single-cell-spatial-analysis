from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

GENE_COLUMNS = ["GeneA", "GeneB", "GeneC", "GeneD", "GeneE"]


def load_reference(path:str) -> pd.DataFrame:
    return pd.read_csv(path)


def load_spatial_expression(path:str) -> pd.DataFrame:
    return pd.read_csv(path)


def load_spatial_metadata(path:str) -> pd.DataFrame:
    return pd.read_csv(path)


def compute_celltype_signatures(
    reference_df: pd.DataFrame,
    gene_columns: list[str] | None = None
) -> pd.DataFrame:
    genes = gene_columns or GENE_COLUMNS
    signatures = (
        reference_df.groupby("cell_type")[genes]
        .mean()
        .reset_index()
    )
    return signatures


def score_spots_against_signatures(
    spatial_df: pd.DataFrame,
    signatures_df: pd.DataFrame,
    gene_columns: list[str] | None = None
) -> pd.DataFrame:
    genes = gene_columns or GENE_COLUMNS

    spot_matrix = spatial_df[genes].to_numpy()
    signature_matrix = signatures_df[genes].to_numpy()

    similarity = cosine_similarity(spot_matrix, signature_matrix)

    scores = pd.DataFrame(
        similarity,
        columns=signatures_df["cell_type"].tolist()
    )
    scores.insert(0, "spot_id", spatial_df["spot_id"].values)
    return scores


def normalise_scores_to_composition(scores_df: pd.DataFrame) -> pd.DataFrame:
    composition = scores_df.copy()
    celltype_cols = [c for c in composition.columns if c != "spot_id"]

    values = composition[celltype_cols].clip(lower=0)
    row_sums = values.sum(axis=1).replace(0, 1)

    composition[celltype_cols] = values.div(row_sums, axis=0)
    return composition


def summarise_by_region(
    composition_df: pd.DataFrame,
    metadata_df: pd.DataFrame
) -> pd.DataFrame:
    merged = composition_df.merge(metadata_df, on="spot_id", how="left")
    celltype_cols = [c for c in composition_df.columns if c != "spot_id"]

    summary = (
        merged.groupby("region")[celltype_cols]
        .mean()
        .reset_index()
    )
    return summary


def melt_composition_for_plotting(composition_df: pd.DataFrame) -> pd.DataFrame:
    return composition_df.melt(
        id_vars="spot_id",
        var_name="cell_type",
        value_name="proportion"
    )


def melt_region_summary_for_plotting(region_summary_df: pd.DataFrame) -> pd.DataFrame:
    return region_summary_df.melt(
        id_vars="region",
        var_name="cell_type",
        value_name="mean_proportion"
    )