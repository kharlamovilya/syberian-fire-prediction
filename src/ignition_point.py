from shapely.geometry import Point
import config
from ndvi_loader import NDVILoader
ndvi_loader = NDVILoader(config.NDVI_PATH)

class IgnitionPoint:
    """
    Represents an ignition point on the map where a fire has started or may start.
    Includes environmental conditions and precomputed fire risk.

    Attributes:
        x (float): Longitude in WGS84 coordinates.
        y (float): Latitude in WGS84 coordinates.
        temperature (float): Air temperature in degrees Celsius at this point.
        humidity (float): Relative humidity (%) at this point.
        wind_speed (float): Wind speed in meters per second.
        wind_direction (float): Wind direction in degrees (0° = North, clockwise).
        point (shapely.geometry.Point): Shapely Point object representing this location.
        ndvi (NDVI): NDVI object representing this location.
        risk_score (float): Computed fire risk score based on weather conditions.
    """
    def __init__(self, x, y, temperature, humidity, wind_speed, wind_direction):
        self.x = x
        self.y = y
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.point = Point(x, y)
        self.ndvi = None
        try:
            self.ndvi = round(ndvi_loader.get_ndvi(x, y), 3)
        except:
            pass
        # Calculate risk once and store
        self.risk_score = self.compute_risk_score()

    def compute_risk_score(self):
        """
        Compute the fire risk score for a given point based on environmental factors.

        Parameters:
        - point: An object with attributes `temperature`, `humidity`, and `wind_speed`.

        Returns:
        - A float representing the normalized fire risk score (0 to 1).
        """
        # Weights
        temp_weight = 0.4
        humidity_weight = 0.3
        wind_weight = 0.3

        # Normalization
        temp_norm = self.temperature / 45.0
        humidity_norm = 1 - (self.humidity / 100.0)
        wind_norm = min(self.wind_speed / 10.0, 1.0)

        score = (
                temp_weight * temp_norm +
                humidity_weight * humidity_norm +
                wind_weight * wind_norm
        )
        return round(score, 3)

    def to_point(self):
        return self.point

    def __repr__(self):
        return (f"IgnitionPoint(x={self.x:.4f}, y={self.y:.4f}, "
                f"T={self.temperature}°C, H={self.humidity}%, "
                f"Wind={self.wind_speed} m/s @ {self.wind_direction}°, "
                f"Risk={self.risk_score})")
