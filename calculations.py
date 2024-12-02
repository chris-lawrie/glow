import pandas as pd

# cap features to remove outliers
# TODO: derive more rigourous caps based on feature distributions
MIN_YEAR = 1880
MAX_ASSET_TOT = 1e8
MAX_BUILDING_AREA = 1e5




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

    df_norm['latest_year'] = df[['yearbuilt', 'yearalter1','yearalter2']].max(axis=1)
    
    # Clip to remove outliers
    df_norm['yearbuilt_capped'] = df_norm['latest_year'].clip(lower=MIN_YEAR)
    df_norm['assettot_capped'] = df_norm['assesstot'].clip(upper=MAX_ASSET_TOT)
    df_norm['bldgarea_capped'] = df_norm['bldgarea'].clip(upper=MAX_BUILDING_AREA)
    
    # Normalize & calc score
    df_norm["yearbuilt_norm"] = 1 - (df_norm['yearbuilt_capped'] - MIN_YEAR) / (df_norm['yearbuilt_capped'].max() - MIN_YEAR)
    df_norm["assettot_norm"] = df_norm['assettot_capped'] / MAX_ASSET_TOT
    df_norm["bldgarea_norm"] = df_norm['bldgarea_capped'] / MAX_BUILDING_AREA
    df_norm["score"] = df_norm[["yearbuilt_norm", "assettot_norm", "bldgarea_norm"]].mean(axis=1)
    return df.loc[df_norm.sort_values(by="score", ascending=False).head(n).index]
