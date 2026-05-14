# OpenStreetMap Harmonization Workflow

Download [OpenStreetMap](https://www.openstreetmap.org/) network data via OSMNX for a boundary region, rasterize the road/way network, and output a single-band GeoTIFF.

## Quick Start (Jupyter Notebook)

```python
from workflows.osm_harmonization.harmonize_osm import harmonize_osm

# Harmonize OSM data over a boundary shapefile
output = harmonize_osm(
    boundary_shp="path/to/boundary.shp",
    output_dir="output/",
    network_type="all",        # or "drive", "walk", "bike", "drive_service"
    resolution=0.000277,       # ~30m in EPSG:4326
    target_crs="EPSG:4326",
    verbose=True,
)
# output -> Path to "harmonized_osm.tif"
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `boundary_shp` | `str \| Path` | *(required)* | Path to a shapefile containing the polygon to clip to |
| `output_dir` | `str \| Path` | `"output"` | Directory for output GeoTIFF |
| `network_type` | `str` | `"all"` | OSM network type: `"all"`, `"drive"`, `"walk"`, `"bike"`, `"drive_service"` |
| `resolution` | `float \| None` | `None` → ~0.000277° | Target pixel resolution in `target_crs` units |
| `target_crs` | `str` | `"EPSG:4326"` | Target CRS for output |
| `verbose` | `bool` | `True` | Print progress messages |

## Output

- **`harmonized_osm.tif`**: Single-band uint8 GeoTIFF where pixel value `1` = OSM feature present, `0` = background

The raster is clipped to the boundary polygon using `all_touched=True` for line features.

## Dependencies

Requires `osmnx` (install with `pip install osmnx`).

## CLI Usage

```bash
python -m workflows.osm_harmonization.harmonize_osm \
    --boundary-shp path/to/boundary.shp \
    --output-dir output/ \
    --network-type drive \
    --resolution 0.000277
```

## Combining with NLCD

After running both workflows, you can stack the outputs into a multi-band raster:

```python
import rasterio
import numpy as np
from pathlib import Path

osm_tif = Path("output/harmonized_osm.tif")
nlcd_tifs = sorted(Path("output").glob("harmonized_nlcd_*.tif"))

with rasterio.open(osm_tif) as src:
    transform = src.transform
    crs = src.crs
    h, w = src.shape
    osm_band = src.read(1)

with rasterio.open(
    "output/combined_stack.tif", "w",
    driver="GTiff", height=h, width=w, count=1 + len(nlcd_tifs),
    dtype="uint8", crs=crs, transform=transform,
    tiled=True, compress="deflate",
) as dst:
    dst.write(osm_band, 1)
    for idx, nlcd in enumerate(nlcd_tifs, start=2):
        with rasterio.open(nlcd) as src:
            dst.write(src.read(1).astype("uint8"), idx)
```#test
