import folium
from folium.plugins import HeatMap
import plotly.express as px

def create_global_heatmap(df, save_path=None):
    """Spatial heatmap generation."""
    city_summary = df.groupby(["location_name", "latitude", "longitude"])["temperature_celsius"].mean().reset_index().dropna()
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")
    heat_data = [[row["latitude"], row["longitude"], row["temperature_celsius"]] for _, row in city_summary.iterrows()]
    HeatMap(heat_data, radius=15, blur=10, min_opacity=0.3).add_to(m)
    if save_path:
        m.save(save_path)
    return m

def create_choropleth(df, save_path=None):
    """Country level choropleth map."""
    country_temps = df.groupby("country")["temperature_celsius"].mean().reset_index()
    fig = px.choropleth(country_temps, locations="country", locationmode="country names", color="temperature_celsius")
    if save_path:
        fig.write_html(save_path)
    return fig
