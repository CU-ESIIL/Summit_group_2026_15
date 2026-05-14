# install libraries
import planetary_computer
import pystac_client
import xarray as xr
from pathlib import Path

# function to download terra climate data 
STAC_API_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"

def download_terraclimate(variable, year_start, year_end, output_path, bbox=None):
    """Search Planetary Computer for TerraClimate data and save to NetCDF."""
    catalog = pystac_client.Client.open(
        STAC_API_URL,
        modifier=planetary_computer.sign_inplace,
    )

    search = catalog.search(
        collections=["terraclimate"],
        datetime=f"{year_start}-01-01/{year_end}-12-31",
        bbox=bbox,
        query={"terraclimate:variable": {"eq": variable}},
    )

    items = list(search.items())
    print(f"Found {len(items)} items for '{variable}' ({year_start}–{year_end})")

    datasets = [
        xr.open_dataset(item.assets[variable].href, engine="rasterio", chunks={})
        for item in items
    ]
    ds = xr.concat(datasets, dim="time")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ds.to_netcdf(output_path)
    print(f"Saved raw: {output_path}")
    return ds

