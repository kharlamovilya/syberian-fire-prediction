import rasterio

class NDVILoader:
    def __init__(self, tif_path):
        self.dataset = rasterio.open(tif_path)
        self.nodata = self.dataset.nodata

    def get_ndvi(self, x, y):
        """Return NDVI value at (x, y) in WGS84 coordinates."""
        try:
            value = list(self.dataset.sample([(x, y)]))[0][0]
            if self.nodata is not None and value == self.nodata:
                return None
            return float(value)
        except Exception:
            return None  # out of bounds or error

    def close(self):
        self.dataset.close()
