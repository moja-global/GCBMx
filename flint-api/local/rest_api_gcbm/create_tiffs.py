import os
import psutil
import random
import shutil
import time
import logging
import simplejson as json
from argparse import ArgumentParser
from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import datetime
from logging import FileHandler
from logging import StreamHandler
from multiprocessing import cpu_count
from multiprocessing import Pool
from collections import defaultdict
from osgeo import gdal

def is_int(x):
    try:
        int(x)
        return True
    except:
        return False

def is_multiband(file):
    tile_block_metadata = file.stem.split("_")[-4:]
    if not all((is_int(x) for x in tile_block_metadata)):
        return True

    for s in tile_block_metadata[:2]:
        if len(s.replace("-", "")) != 3:
            return True

    return False

def get_tile_groups(block_files):
    tiles = defaultdict(list)
    for fn in block_files:
        tile_idx_pos = 3 if is_multiband(fn) else 4
        tile = "_".join(fn.name.rsplit("_", tile_idx_pos)[1:3])
        tiles[tile].append(fn)

    return tiles

def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def generate_config_data(title_list, config_dict, palettes):
    palettes = list(set(palettes))
    random.shuffle(palettes)

    config_data = []
    used_palettes = set()
    missing_titles = []  # List to keep track of titles with missing configs

    for title in title_list:
        if title not in config_dict:
            missing_titles.append(title)  # Add missing title to the list
            continue  # Skip to the next title

        # Retrieve configuration from the dictionary
        config_entry = config_dict[title]
        file_pattern = config_entry.get("file_pattern", "")
        graph_units = config_entry.get("graph_units", "")

        # Pick a palette that hasn't been used yet
        available_palettes = [p for p in palettes if p not in used_palettes]
        if not available_palettes:
            raise ValueError("Ran out of unique palettes")

        palette = random.choice(available_palettes)
        used_palettes.add(palette)

        # Update the palette in the configuration entry
        config_entry["palette"] = palette

        config_data.append(config_entry)

    # log missing titles
    if missing_titles:
        logging.info("Configurations for the following titles were not found:")
        for title in missing_titles:
            logging.info(f"- {title}")

    return config_data

def save_config_to_file(config_data, filename):
    with open(filename, 'w') as file:
        json.dump(config_data, file, indent=4)

def find_indicator_files(indicator, start_year=None):
    indicator_output = defaultdict(list)
    for file in indicator.rglob("*.tif"):
        year = "multiband"
        if not is_multiband(file):
            timestep = int(file.stem.rsplit("_", 1)[1])
            year = str(start_year + timestep - 1) if start_year is not None else timestep

        indicator_output[year].append(file)

    return indicator_output

def get_start_year(output_path):
    config_file = output_path.parent.joinpath("localdomain.json")
    if not config_file.exists():
        return logging.info("file not found")

    simulation_config = json.load(open(config_file, "r"))
    start_date = simulation_config["LocalDomain"]["start_date"]
    logging.info(f"here is {start_date}")

    try:
        return datetime.strptime(start_date, "%Y/%m/%d").year
    except:
        return logging.info(f" error in year")

def init_pool(worker_mem):
    gdal.SetCacheMax(worker_mem)

def process_spatial_output(spatial_output_path, output_path, epsg=None, do_cleanup=True):
    output_path.mkdir(parents=True, exist_ok=True)
    new_dir = Path(output_path).with_name("config")
    new_dir.mkdir(parents=True, exist_ok=True)

    num_workers = cpu_count()
    available_mem = psutil.virtual_memory().available
    worker_mem = int(available_mem * 0.8 / num_workers)
    pool = Pool(num_workers, init_pool, (worker_mem,))

    processed_indicators = []
    start_year = get_start_year(output_path)
    for indicator in spatial_output_path.iterdir():
        if (not indicator.is_dir() or indicator.name == "csv") or indicator.name in ["spatial", "aspatial", "config"]:
            continue

        logging.info(f"  {indicator.name}")
        processed_indicators.append(indicator)
        for year, files in find_indicator_files(indicator, start_year).items():
            logging.info(f"    {year}")
            pool.apply_async(merge_indicator_files, (indicator, year, files, output_path, epsg))

    pool.close()
    pool.join()

    config_path = Path(__file__).parent / "dictionary.json"
    palettes_path = Path(__file__).parent / "colormap.json"

    config_dict = load_json(config_path)
    palettes = load_json(palettes_path)
    indicators = [os.path.basename(path) for path in processed_indicators]
    config_data = generate_config_data(indicators, config_dict, palettes)

    created_config = new_dir / "config.json"
    save_config_to_file(config_data, created_config)
    logging.info("Map Config JSON file created successfully")

    if do_cleanup:
        for indicator in processed_indicators:
            shutil.rmtree(indicator)

def merge_indicator_files(indicator, year, files, output_path, epsg=None):
    available_mem = psutil.virtual_memory().total
    gdal_mem = int(available_mem * 0.75 / cpu_count())
    gdal.SetCacheMax(gdal_mem)
    gdal.UseExceptions()
    gdal.SetConfigOption("GDAL_SWATH_SIZE",              str(gdal_mem))
    gdal.SetConfigOption("VSI_CACHE",                    "TRUE")
    gdal.SetConfigOption("VSI_CACHE_SIZE",               str(int(gdal_mem / len(files))))
    gdal.SetConfigOption("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
    gdal.SetConfigOption("GDAL_PAM_ENABLED",             "NO")
    gdal.SetConfigOption("GDAL_GEOREF_SOURCES",          "INTERNAL,NONE")
    gdal.SetConfigOption("GTIFF_DIRECT_IO",              "YES")
    gdal.SetConfigOption("GDAL_MAX_DATASET_POOL_SIZE",   "50000")

    with TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        merged_tiles = []
        for tile, tile_files in get_tile_groups(files).items():
            if len(tile_files) == 1:
                merged_tiles.extend(tile_files)
                continue

            tile_vrt_filename = str(tmp_path.joinpath(f"{indicator.name}_{tile}_{year}.vrt"))
            gdal.BuildVRT(tile_vrt_filename, [str(f) for f in tile_files])

            tile_tif_filename = str(tmp_path.joinpath(f"{indicator.name}_{tile}_{year}.tif"))
            merged_tiles.append(tile_tif_filename)

            gdal.Translate(
                tile_tif_filename, tile_vrt_filename, maskBand="none",
                creationOptions=["BIGTIFF=YES", "TILED=YES", "SPARSE_OK=YES"])

        vrt_filename = str(tmp_path.joinpath(f"{indicator.name}_{year}.vrt"))
        gdal.BuildVRT(vrt_filename, [str(f) for f in merged_tiles])

        tif_filename = str(output_path.joinpath(f"{indicator.name}_{year}.tif"))

        if epsg:
            dest_srs = osr.SpatialReference()
            dest_srs.ImportFromEPSG(self._epsg)
            gdal.Warp(
                tif_filename, vrt_filename, dstSrs=dest_srs, maskBand="none",
                creationOptions=[
                    "BIGTIFF=YES", "TILED=YES", "COMPRESS=DEFLATE",
                    f"NUM_THREADS={int(cpu_count() / 2)}"
                ])
        else:
            gdal.Translate(
                tif_filename, vrt_filename, maskBand="none",
                creationOptions=[
                    "BIGTIFF=YES", "TILED=YES", "COMPRESS=DEFLATE",
                    f"NUM_THREADS={int(cpu_count() / 2)}"
                ])

if __name__ == "__main__":
    gdal.PushErrorHandler("CPLQuietErrorHandler")

    parser = ArgumentParser(description="Generate final layers from raw spatial output.")
    parser.add_argument("indicator_root", help="path to the spatial output root directory")
    parser.add_argument("output_path", help="path to store generated tiffs in - will be created if it doesn't exist")
    parser.add_argument("--log_path", required=False, default="logs", help="path to create log file in")
    parser.add_argument("--epsg", required=False, help="alternate EPSG code to project final layers in")
    parser.add_argument("--no_cleanup", required=False, help="do not clean up original output files", action="store_true")
    args = parser.parse_args()

    log_path = Path(args.log_path)
    log_path.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s", datefmt="%m/%d %H:%M:%S", handlers=[
        FileHandler(log_path.joinpath("create_tiffs.log"), mode="w"),
        StreamHandler()
    ])

    spatial_output_path = Path(args.indicator_root)
    output_path = Path(args.output_path)
    do_cleanup = not args.no_cleanup

    logging.info(f"Processing spatial output from {spatial_output_path} into {output_path}")
    process_spatial_output(spatial_output_path, output_path, args.epsg, do_cleanup)
    logging.info("Done")
