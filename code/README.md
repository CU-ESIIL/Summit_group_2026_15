# Code Folder Structure

## Overview

This folder contains all code and modules for the project.

## Project Organization

```mermaid
flowchart TD
    NB["📓 notebook/\nJupyter Notebook"]

    NB --> M1["📦 module_nlcd_osm/"]
    NB --> M2["📦 module_example/"]
    NB -.-> MN["📦 module_*/\n(future modules)"]

    M1 --> F1a["nlcd_osm_harmonizer.py"]
    M1 --> F1b["nlcd_osm_text.md"]
    M1 --> F1c["nlcd_osm_diagram.png"]
    M1 --> F1d["nlcd_osm_README.md"]

    M2 --> F2a["example_harmonizer.py"]
    M2 --> F2b["example_text.md"]
    M2 --> F2c["example_diagram.png"]
    M2 --> F2d["example_README.md"]

    MT["📋 module_tracking/\nmodules.csv"]

    MT -. "tracks all" .-> M1
    MT -. "tracks all" .-> M2
    MT -. "tracks all" .-> MN
```

## Folders

### `notebook/`
Holds all files related to the Jupyter notebook that pulls together the individual modules into a single analysis workflow.

### `module_*/` (e.g. `module_example/`)
Each module is its own folder. See `module_example/` for the standard structure:

| File | Description |
|------|-------------|
| `*_README.md` | Overview and documentation for the module |
| `*_text.md` | Written explanation of methods and context |
| `*_diagram.png` | Visual diagram of the module workflow |
| `*_harmonizer.py` | Python script containing the module's core functions |

### `module_tracking/`
Holds metadata about all modules, including `modules.csv` which tracks the status, inputs, outputs, and dependencies of each module.
