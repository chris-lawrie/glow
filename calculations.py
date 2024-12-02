import pandas as pd


YEAR_BUILT = "yearbuilt"
ASSET_TOT = "assesstot"
BUILDING_AREA = "bldgarea"


def find_top_n_candidates(df: pd.DataFrame, n) -> pd.DataFrame:
    """
    Placeholder heuristic which finds the top N candidate buildings

    Features considered with equal relative weighting are:
        - Building age
        - Number of floors
        - Building value

    Args:
        df: data frame containing the full set of candidates

    Returns:
        candidates: dataframe containing top N candidates
    """
    df_norm = df.copy(deep=True)
    df_norm["yearbuilt_norm"] = (df[YEAR_BUILT].max() - df[YEAR_BUILT]) / (
        df[YEAR_BUILT].max() - df[YEAR_BUILT].min()
    )
    df_norm["assesstot_norm"] = (df[ASSET_TOT] - df[ASSET_TOT].min()) / (
        df[ASSET_TOT].max() - df[ASSET_TOT].min()
    )
    df_norm["bldgarea_norm"] = (
        df[BUILDING_AREA] - df[BUILDING_AREA].min()
    ) / (df[BUILDING_AREA].max() - df[BUILDING_AREA].min())
    df_norm["score"] = df_norm[
        ["yearbuilt_norm", "assesstot_norm", "bldgarea_norm"]
    ].mean(axis=1)
    return df.loc[
        df_norm.sort_values(by="score", ascending=False).head(n).index
    ]
