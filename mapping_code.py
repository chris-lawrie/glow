import folium
import pandas as pd
from matplotlib import cm
from matplotlib.colors import Normalize


def get_color(year: int, norm: Normalize, colormap: cm) -> str:
    """
    Calculates color of a dot based the year it was built
    """
    color = colormap(norm(year))
    # Convert Matplotlib RGBA color to hex
    return f"#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}"


def map_candidates(df: pd.DataFrame) -> folium.Map:
    """
    Creates map of top building candidates

    Args:
        df: dataframe of eligible buildings

    Returns:
        m: the constructed folium map object
    """
    norm = Normalize(vmin=df["yearbuilt"].min(), vmax=df["yearbuilt"].max())
    colormap = cm.get_cmap("viridis")

    m = folium.Map(
        location=[df["latitude"].mean(), df["longitude"].mean()],
        zoom_start=12,
        tiles="cartodb positron",
    )
    # Add points to the map
    for _, row in df.iterrows():
        fill_color = get_color(row["yearbuilt"], norm=norm, colormap=colormap)
        tooltip = folium.Tooltip(
            f"""
        <b>Year Built:</b> {row['yearbuilt']} <br>
        <b>Num Floors:</b> {row['numfloors']} <br>
        <b>Building Area:</b> {row['bldgarea']} <br>
        <b>Building Value:</b> ${round(row['assesstot'] / 1_000_000, 2)}mil <br>  # noqa
        <b>Address:</b> {row['address']} <br>
        """
        )
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=4,
            color=None,
            stroke=False,
            fill=True,
            fill_color=fill_color,
            fill_opacity=0.7,
            tooltip=tooltip,
        ).add_to(m)
    return m
