# install libraries 
import geopandas as gpd
import rioxarray  
from pathlib import Path

# function to clip raster data to shapefile
def clip_to_shapefile(ds, variable, shapefile_path, output_path):
    aoi = gpd.read_file(shapefile_path)

    data = ds[variable]
    data = data.rio.write_crs("Projection")
    data = data.rio.set_spatial_dims(x_dim="lon", y_dim="lat")

    if aoi.crs != data.rio.crs:
        aoi = aoi.to_crs(data.rio.crs)

    clipped = data.rio.clip(aoi.geometry, aoi.crs, drop=True)

    output_path = Path(output_path)
    clipped.to_netcdf(output_path)
    print(f"Saved clipped: {output_path}")
    return clipped