#import required libraries
import mesa
import numpy as np
import mesa_geo as mg
import rasterio as rio

class ReefCell(mg.Cell):
    elevation: int | None
    oy_in_cell: int | None

    def __init__(
        self,
        pos: mesa.space.Coordinate | None = None,
        indices: mesa.space.Coordinate | None = None,
    ):
        super().__init__(pos, indices)
        self.og_elevation = None
        self.new_elevation = None

    def step(self):
        pass

class SeaBed(mg.GeoSpace):
    def __init__(self, crs):
        super().__init__(crs = crs)

    def set_elevation_layer(self, crs):
        raster_layer = mg.RasterLayer.from_file(
            "data/oyster_dem.tif", 
            cell_cls = ReefCell, 
            attr_name = "og_elevation"
            )
        raster_layer.crs = crs
        raster_layer.apply_raster(
            data = np.ones(shape = (1, raster_layer.height, raster_layer.width)),
            attr_name = "new_elevation",
        )
        super().add_layer(raster_layer)

    @property
    def raster_layer(self):
        return self.layers[0]

    