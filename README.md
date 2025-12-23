# 🌲 Forest Fire Risk Mapping & Simulation System  
*(Siberia, Russia)*

## Overview

This project is a **Python-based GIS wildfire simulation platform** focused on forest regions of Siberia, Russia.  
It combines **satellite vegetation data (NDVI)** with **real-time weather information** to assess wildfire risk and simulate wind-driven fire spread on an interactive map.

The system is designed as both:
- an **analytical tool** for understanding wildfire dynamics (can only be used for educational purposes)  
- an **educational platform** for GIS, simulation, and environmental modeling
<img width="1500" height="810" alt="image" src="https://github.com/user-attachments/assets/c2549d5b-5809-4b41-9534-3248c2240a10" />

---

## Running the Project

## ⚠️ Required One-Time Preparation Steps

Before running `main.py` **for the first time**, you must run the following scripts **at least once**.

### 1️⃣ Prepare Regions
```bash
python prepare_regions.py
```

This script:
- Loads raw regional boundary data
- Filters and prepares Siberian regions
- Saves processed region files used by the simulation

---

### 2️⃣ Fetch & Enrich Weather Data
Weather data is retrieved using the **WeatherAPI** service:  
👉 https://www.weatherapi.com/
```bash
python weather_loader.py
```

This script:
- Fetches live weather data for ignition points using WeatherAPI
- Enriches ignition points with temperature, humidity, and wind data
- Saves the enriched ignition dataset required for simulation

---
### 🔥 Generate Fire Ignition & Spread Map

To generate the **interactive map of fire ignitions and simulated spread**, run:

```bash
python main.py
```

This will:
- Load prepared regional data
- Load ignition points enriched with weather data
- Run the fire spread simulation
- Generate an interactive **HTML map** showing ignition points and spread dynamics

---
## ✅ Recommended Execution Order

```text
1. prepare_regions.py      (run once)
2. weather_loader.py       (run once or when updating weather)
3. main.py                 (run to generate the map)
```

You only need to rerun:
- `prepare_regions.py` if region data changes
- `weather_loader.py` if you want updated weather conditions

---

## 📍 Output

After running `main.py`, the resulting **interactive fire map** is generated locally as an HTML file and can be opened directly in a web browser.

## Project Aim

The goal of this project is to build a **modular, object-oriented GIS simulation system** that can:

- Assess forest fire risk across different regions of Russia  
- Simulate potential wildfire spread using real environmental data  
- Visualize results on interactive maps  

The project explores how **wind, humidity, temperature, and vegetation** influence wildfire behavior.

---

## Scope of Work

### Geospatial Data Handling
- Load administrative or ecological regions from **GeoJSON / shapefiles** (e.g. GADM)
- Integrate auxiliary spatial data:
  - Weather data (temperature, humidity, wind speed & direction) via **WeatherAPI**
  - Vegetation indices (**NDVI**) from satellite raster data

### Object-Oriented Design
Reusable Python components:
- `IgnitionPoint` – represents fire ignition points with weather and risk data
- `Region` – encapsulates spatial boundaries and metadata
- `NDVILoader` – extracts NDVI values from raster layers
- `FireSimulator` – core fire spread simulation logic

### Fire Risk Assessment
Each ignition point receives a **risk score** based on:
- Temperature  
- Humidity  
- Wind speed  

NDVI is used to **filter out areas with insufficient vegetation** for combustion.

### Map Visualization
Interactive **Folium maps** featuring:
- Clustered and unclustered ignition & spread markers
- Popups with risk, NDVI, and weather information
- Region overlays and legends
- Zoom-based cluster control

### Fire Spread Simulation
Fire spread is modeled using:
- Wind direction and strength (directionally biased spread)
- Environmental risk score
- NDVI-based flammability

The simulation propagates fire **iteratively over multiple steps**.

---

## Workflow

### 1. Data Loading
- Load forest region boundaries into a GeoDataFrame
- Fetch live weather data for ignition points
- Load NDVI data from GeoTIFF files using `rasterio`

### 2. Object Initialization
- Create `IgnitionPoint` instances (e.g. from NASA FIRMS data)
- Store location, weather, NDVI, and calculated risk attributes

### 3. Risk Calculation
- Compute fire risk using a weighted model of environmental factors

### 4. Fire Simulation
- Simulate fire spread using wind-aligned propagation logic
- Generate new spread points over multiple steps
- Export results to GeoJSON

### 5. Map Rendering
- Load ignition and spread data
- Visualize results on an interactive Folium map
- Enable zoom-based clustering

---

## Project Structure

```
src/
├── scripts/
├────────── prepare_regions.py
├────────── weather_loader.py 
├── config.py
├── data_loader.py
├── ignition_point.py
├── simulator.py
├── ndvi_loader.py
├── map_renderer.py
├── weather_loader.py
├── main.py
```

---

## Fire Spread Logic

- Spread attempts in **8 directions per step**
- Directions randomized within **±90° of wind direction**
- Spread distance biased by **wind alignment**
- Latitude correction applied for geographic accuracy

Spread is blocked if:
- The location is already burned
- The point lies outside valid regions
- NDVI is missing or below a threshold (e.g. `< 0.15`)

---

## Limitations

- Vegetation modeling relies solely on NDVI
- Terrain features (rivers, elevation) are not yet considered
- Wind speed is capped for normalization
- No suppression or firefighting simulation

---

## Future Improvements

- Integrate DEM data to block spread across rivers and mountains
- Introduce time-based simulation steps (e.g. 1 step = 1 hour)
- Expand ignition point metadata (cause, timestamp)
- Add a GUI or web dashboard for parameter tuning

---

## Requirements

- Python **3.10+**
- Libraries:
  - geopandas
  - shapely
  - rasterio
  - folium
  - aiohttp
  - pandas
  - numpy
- WeatherAPI key (for live data)
- MODIS NDVI raster data (GeoTIFF)

---

## Conclusion

This project demonstrates how **environmental data, GIS, and simulation algorithms** can be combined in a Python-based framework to model and visualize wildfire dynamics.  
It provides a flexible foundation for further research, experimentation, and real-world fire risk analysis.

---

## Credits

Developed by **Kharlamov Ilia** as a research and educational project.  
Weather data provided by **WeatherAPI**.  
NDVI data sourced from **MODIS (NASA)**.
