import folium
from folium.plugins import MarkerCluster
from shapely.geometry import mapping
import config


def render_fire_map_html(regions, ignition_points=None, spread_points=None, output_path='fire_map.html'):
    # Calculate map center
    if ignition_points:
        center_lat = sum(p.y for p in ignition_points) / len(ignition_points)
        center_lon = sum(p.x for p in ignition_points) / len(ignition_points)
    else:
        center_lat, center_lon = 60.0, 90.0  # fallback

    m = folium.Map(location=[center_lat, center_lon], zoom_start=5, tiles='cartodbpositron')

    # Add region polygons
    for region in regions:
        geom = mapping(region.geometry)
        folium.GeoJson(
            data=geom,
            name=region.region_id,
            style_function=lambda x: {
                'fillColor': 'gray',
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.3,
            },
            tooltip=region.region_id
        ).add_to(m)

    # 🔴 Ignition points with fast-cluster breakup
    if ignition_points:
        ignition_cluster = MarkerCluster(name="Ignition Points", disableClusteringAtZoom=config.MAP_CLUSTERING).add_to(
            m)
        for pt in ignition_points:
            popup_text = (
                f"<b>Ignition Point</b><br>"
                f"NDVI: {getattr(pt, 'ndvi', '—')}<br>"
                f"Risk: {getattr(pt, 'risk_score', '—')}<br>"
                f"Temp: {getattr(pt, 'temperature', '—')} °C<br>"
                f"Humidity: {getattr(pt, 'humidity', '—')}%<br>"
                f"Wind: {getattr(pt, 'wind_speed', '—')} m/s @ {getattr(pt, 'wind_direction', '—')}°"
            )
            folium.CircleMarker(
                location=[pt.y, pt.x],
                radius=4,
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.8,
                popup=popup_text
            ).add_to(ignition_cluster)

    # 🟠 Spread points with fast-cluster breakup
    if spread_points:
        spread_cluster = MarkerCluster(name="Spread Points", disableClusteringAtZoom=config.MAP_CLUSTERING).add_to(m)
        for pt in spread_points:
            popup_text = (
                f"<b>Ignition Point</b><br>"
                f"NDVI: {getattr(pt, 'ndvi', '—')}<br>"
                f"Risk: {getattr(pt, 'risk_score', '—')}<br>"
                f"Temp: {getattr(pt, 'temperature', '—')} °C<br>"
                f"Humidity: {getattr(pt, 'humidity', '—')}%<br>"
                f"Wind: {getattr(pt, 'wind_speed', '—')} m/s @ {getattr(pt, 'wind_direction', '—')}°"
            )
            folium.CircleMarker(
                location=[pt.y, pt.x],
                radius=4,
                color='orange',
                fill=True,
                fill_color='orange',
                fill_opacity=0.8,
                popup=popup_text
            ).add_to(spread_cluster)

    # 🧭 Map legend
    legend_html = """
    <div style="
        position: fixed;
        bottom: 40px; left: 40px; width: 170px; height: 110px;
        background-color: white;
        border:2px solid gray;
        z-index:9999;
        font-size:13px;
        padding: 10px;
    ">
        <b>Legend</b><br>
        🔴 Ignition Point<br>
        🟠 Spread Point<br>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    folium.LayerControl().add_to(m)
    m.save(output_path)
    print(f"Fire map saved to {output_path}")
