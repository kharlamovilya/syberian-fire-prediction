import json
import math
import random
from config import WIND_RANDOM_SPREAD

class FireSimulator:
    """
    Simulates the spread of wildfire based on ignition points and weather conditions.
    """

    def __init__(self, regions, output):
        self.regions = regions
        self.ignition_points = []
        self.spread_points = []
        self.output = output

    def simulate_fire(self, ignition_points, ndvi_loader, steps=10, risk_threshold=0.4, max_distance=0.2):
        """
        Simulate fire spread over a series of steps.

        Parameters:
        - ignition_points: List of starting points for the fire (must support required attributes).
        - ndvi_loader: An NDVILoader object with `get_ndvi(x, y)` method.
        - steps: Number of simulation steps to run.
        - risk_threshold: Minimum risk score required for fire to spread.
        - max_distance: Base distance a fire can travel in one step (adjusted by wind).
        """
        self.ignition_points = ignition_points
        self.spread_points = []
        burning_points = ignition_points.copy()
        burned_points = set()
        print("Simulating fire...", end='')
        for step in range(1, steps + 1):
            print(f"\n🔥 Step {step}")
            new_spreads = []
            counter = 0
            for pt in burning_points:
                counter += 1
                print(f'\rPoints done: {counter}/{len(burning_points)}', flush=True, end='')
                pt_key = (round(pt.x, 4), round(pt.y, 4))
                if pt_key in burned_points:
                    continue
                burned_points.add(pt_key)

                # Calculate risk for a point
                if pt.risk_score < risk_threshold:
                    continue

                # Try 8 different directions for fire spread around each burning point
                for _ in range(WIND_RANDOM_SPREAD):  # Wind-centered spread
                    # Generate a random spread angle within ±90° of the wind direction
                    angle = pt.wind_direction + random.uniform(-90, 90)

                    # Calculate how aligned the spread angle is with the wind
                    # (0° difference means aligned, 90° means perpendicular)
                    angle_diff = abs((angle - pt.wind_direction + 180) % 360 - 180)

                    # Compute wind influence: more aligned means longer spread distance
                    wind_factor = math.cos(math.radians(angle_diff))

                    # Calculate spread distance with wind bias
                    distance = max_distance * (1 + 0.6 * wind_factor)

                    # Correct for latitude since degrees of longitude are narrower near poles
                    lat_correction = math.cos(math.radians(pt.y))
                    dx = distance * math.cos(math.radians(angle)) / lat_correction  # longitude adjustment
                    dy = distance * math.sin(math.radians(angle))  # latitude movement

                    # Create the new potential fire spread point
                    new_x = pt.x + dx
                    new_y = pt.y + dy

                    new_pt = type(pt)(
                        new_x, new_y,
                        pt.temperature, pt.humidity,
                        pt.wind_speed, pt.wind_direction
                    )

                    # Check NDVI
                    new_pt.ndvi = ndvi_loader.get_ndvi(new_x, new_y)
                    if new_pt.ndvi is None or new_pt.ndvi < 0.15:
                        continue

                    # Avoid duplicates and ensure the point lies in a valid region
                    new_pt_key = (round(new_x, 4), round(new_y, 4))
                    if new_pt_key not in burned_points and any(r.contains(new_pt.to_point()) for r in self.regions):
                        new_spreads.append(new_pt)


            if not new_spreads:
                print("\nNo further spread.")
                break

            self.spread_points.extend(new_spreads)
            burning_points = new_spreads
        self.save_spread_to_json()

    def save_spread_to_json(self):
        """
        Save spread points to a JSON file for later rendering or analysis.

        Parameters:
        - output_path: Path to output JSON file
        """
        data = [
            {
                "x": pt.x,
                "y": pt.y,
                "temperature": pt.temperature,
                "humidity": pt.humidity,
                "wind_speed": pt.wind_speed,
                "wind_direction": pt.wind_direction,
                "step": getattr(pt, 'step', None),
                "ndvi": getattr(pt, 'ndvi', None),
                "risk_score": getattr(pt, 'risk_score', None)
            }
            for pt in self.spread_points
        ]
        with open(self.output, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        print(f"\nSaved fire spread results to {self.output}")