import os
import shutil
import json
import rasterio as rst


def get_config_templates(input_dir):
    """Check if 'templates' or 'config' exists in input_dir, but only copy 'templates' if missing."""

    try:
        if not os.path.exists(f"{input_dir}/templates") or not os.path.exists(f"{input_dir}/config"):
            shutil.copytree("templates", f"{input_dir}/templates")
    except FileNotFoundError as e:
        print(f"Error: The source directory 'templates' does not exist. {e}")
    except PermissionError as e:
        print(f"Error: Permission denied while accessing directories. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



# TODO: there needs to be a link between the files configured here append
# the ["vars"] attribute of modules_cbm.json -> CBMDisturbanceListener
# current hack is to drop the last five characters, but thats very fragile
def get_modules_cbm_config(input_dir):
    try:
        # Check for the file in templates or config
        templates_path = os.path.join(input_dir, "templates/modules_cbm.json")
        config_path = os.path.join(input_dir, "config/modules_cbm.json")

        if os.path.exists(templates_path):
            modules_cbm_path = templates_path
        elif os.path.exists(config_path):
            modules_cbm_path = config_path
        else:
            raise FileNotFoundError("modules_cbm.json not found in 'templates' or 'config'.")

        with open(modules_cbm_path, "r+") as modules_cbm_config:
            data = json.load(modules_cbm_config)
            disturbances = [file.split(".")[0][:-5] for file in os.listdir(f"{input_dir}/disturbances/")]  # drop `_moja` to match modules_cbm.json template
            modules_cbm_config.seek(0)
            data["Modules"]["CBMDisturbanceListener"]["settings"]["vars"] = disturbances
            json.dump(data, modules_cbm_config, indent=4)
            modules_cbm_config.truncate()
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON in {modules_cbm_path}. {e}")
    except PermissionError as e:
        print(f"Error: Permission denied while accessing the file {modules_cbm_path}. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def get_provider_config(input_dir):

    # Check for the file in templates or config
    templates_path = os.path.join(input_dir, "templates/provider_config.json")
    config_path = os.path.join(input_dir, "config/provider_config.json")

    if os.path.exists(templates_path):
        provider_path = templates_path
    elif os.path.exists(config_path):
        provider_path = config_path
    else:
        raise FileNotFoundError("provider_config.json not found in 'templates' or 'config'.")

    with open(provider_path, "r+") as provider_config:
        lst = []
        data = json.load(provider_config)

        for file in os.listdir(f"{input_dir}/db/"):
            d = dict()
            d["path"] = file
            d["type"] = "SQLite"
            data["Providers"]["SQLite"] = d
        provider_config.seek(0)

        disturbances_path = os.path.join(input_dir, "disturbances")
        if os.path.exists(disturbances_path) and os.listdir(disturbances_path):
            for file in os.listdir(disturbances_path):
                if file.endswith(('.tif', '.tiff', '.img')):  # Only process raster files
                    d = dict()
                    d["name"] = file[:-10]
                    d["layer_path"] = file
                    d["layer_prefix"] = file[:-5]
                    lst.append(d)
        provider_config.seek(0)
        data["Providers"]["RasterTiled"]["layers"] = lst

        for file in os.listdir(f"{input_dir}/classifiers/"):
            if file.endswith(('.tif', '.tiff', '.img')):  # Only process raster files
                d = dict()
                d["name"] = file[:-10]
                d["layer_path"] = file
                d["layer_prefix"] = file[:-5]
                lst.append(d)
        provider_config.seek(0)
        data["Providers"]["RasterTiled"]["layers"] = lst

        for file in os.listdir(f"{input_dir}/miscellaneous/"):
            if file.endswith(('.tif', '.tiff', '.img')):  # Only process raster files
                d = dict()
                d["name"] = file[:-10]
                d["layer_path"] = file
                d["layer_prefix"] = file[:-5]
                lst.append(d)
        provider_config.seek(0)
        data["Providers"]["RasterTiled"]["layers"] = lst

        Rasters = []
        Rastersm = []
        nodatam = []
        nodata = []
        cellLatSize = []
        cellLonSize = []
        paths = []

        # Walk through the directories and collect raster files
        if os.path.exists(disturbances_path) and os.listdir(disturbances_path):
            for root, _, files in os.walk(disturbances_path):
                for file in files:
                    if file.endswith(('.tif', '.tiff', '.img')):  # Only process raster files
                        fp = os.path.join(root, file)
                        Rasters.append(fp)
                        paths.append(fp)

        for root, _, files in os.walk(os.path.abspath(f"{input_dir}/classifiers/")):
            for file in files:
                if file.endswith(('.tif', '.tiff', '.img')):  # Only process raster files
                    fp1 = os.path.join(root, file)
                    Rasters.append(fp1)
                    paths.append(fp1)

        for root, _, files in os.walk(os.path.abspath(f"{input_dir}/miscellaneous/")):
            for file in files:
                if file.endswith(('.tif', '.tiff', '.img')):  # Only process raster files
                    fp2 = os.path.join(root, file)
                    Rastersm.append(fp2)

        for i in Rasters + Rastersm:
            try:
                img = rst.open(i)
                t = img.transform
                x = t[0]
                y = -t[4]
                n = img.nodata
                cellLatSize.append(x)
                cellLonSize.append(y)
                nodata.append(n)
            except rasterio.errors.RasterioIOError:
                print(f"Skipping non-raster file: {i}")
                continue

        result = all(element == cellLatSize[0] for element in cellLatSize)
        if result:
            cellLat = x
            cellLon = y
            nd = n
            blockLat = x * 400
            blockLon = y * 400
            tileLat = x * 4000
            tileLon = y * 4000
        else:
            print("Corrupt files")

        provider_config.seek(0)

        data["Providers"]["RasterTiled"]["cellLonSize"] = cellLon
        data["Providers"]["RasterTiled"]["cellLatSize"] = cellLat
        data["Providers"]["RasterTiled"]["blockLonSize"] = blockLon
        data["Providers"]["RasterTiled"]["blockLatSize"] = blockLat
        data["Providers"]["RasterTiled"]["tileLatSize"] = tileLat
        data["Providers"]["RasterTiled"]["tileLonSize"] = tileLon

        json.dump(data, provider_config, indent=4)
        provider_config.truncate()

        dictionary = {
            "layer_type": "GridLayer",
            "layer_data": "Byte",
            "nodata": nd,
            "tileLatSize": tileLat,
            "tileLonSize": tileLon,
            "blockLatSize": blockLat,
            "blockLonSize": blockLon,
            "cellLatSize": cellLat,
            "cellLonSize": cellLon,
        }

        # should be able to accept variable number of inputs, but requires
        # means for user to specify/verify correct ["attributes"]
        def get_input_layers():
            for root, _, files in os.walk(os.path.abspath(f"{input_dir}/miscellaneous/")):
                for file in files:
                    if file.endswith(('.tif', '.tiff', '.img')):  # Only process raster files
                        fp2 = os.path.join(root, file)
                        Rastersm.append(fp2)

            for i in Rastersm:
                try:
                    img = rst.open(i)
                    d = img.nodata
                    nodatam.append(d)
                except rasterio.errors.RasterioIOError:
                    print(f"Skipping non-raster file: {i}")
                    continue

            # Write JSON files as before
            with open(f"{input_dir}/initial_age_moja.json", "w", encoding="utf8") as json_file:
                dictionary["layer_type"] = "GridLayer"
                dictionary["layer_data"] = "Int16"
                dictionary["nodata"] = 32767
                json.dump(dictionary, json_file, indent=4)

            with open(f"{input_dir}/mean_annual_temperature_moja.json", "w", encoding="utf8") as json_file:
                dictionary["layer_type"] = "GridLayer"
                dictionary["layer_data"] = "Float32"
                dictionary["nodata"] = 32767
                json.dump(dictionary, json_file, indent=4)

            with open(f"{input_dir}/Classifier1_moja.json", "w", encoding="utf8") as json_file:
                dictionary["layer_type"] = "GridLayer"
                dictionary["layer_data"] = "Byte"
                dictionary["nodata"] = nd
                dictionary["attributes"] = {
                    "1": "TA",
                    "2": "BP",
                    "3": "BS",
                    "4": "JP",
                    "5": "WS",
                    "6": "WB",
                    "7": "BF",
                    "8": "GA",
                }
                json.dump(dictionary, json_file, indent=4)

            with open(f"{input_dir}/Classifier2_moja.json", "w", encoding="utf8") as json_file:
                dictionary["layer_type"] = "GridLayer"
                dictionary["layer_data"] = "Byte"
                dictionary["nodata"] = nd
                dictionary["attributes"] = {"1": "5", "2": "6", "3": "7", "4": "8"}
                json.dump(dictionary, json_file, indent=4)

            with open(f"{input_dir}/disturbances_2011_moja.json", "w", encoding="utf8") as json_file:
                dictionary["layer_data"] = "Byte"
                dictionary["nodata"] = nd
                dictionary["attributes"] = {
                    "1": {"year": 2011, "disturbance_type": "Wildfire", "transition": 1}
                }
                json.dump(dictionary, json_file, indent=4)

            # Repeat for other layers...

        get_input_layers()

        def get_study_area():
            study_area = {
                "tile_size": tileLat,
                "block_size": blockLat,
                "tiles": [
                    {
                        "x": int(t[2]),
                        "y": int(t[5]),
                        "index": 12674,
                    }
                ],
                "pixel_size": cellLat,
                "layers": [],
            }

            with open(f"{input_dir}/study_area.json", "w", encoding="utf") as json_file:
                list = []

                for file in os.listdir(f"{input_dir}/miscellaneous/"):
                    d1 = dict()
                    d1["name"] = file[:-10]
                    d1["type"] = "VectorLayer"
                    list.append(d1)
                study_area["layers"] = list

                # Add more layers...

                json.dump(study_area, json_file, indent=4)

        get_study_area()

        paths = []
        disturbances_path = os.path.join(input_dir, "disturbances")
        if os.path.exists(disturbances_path) and os.listdir(disturbances_path):
            for root, _, files in os.walk(disturbances_path):
                for file in files:
                    if file.endswith(('.tif', '.tiff', '.img')):  # Only process raster files
                        fp = os.path.join(root, file)
                        paths.append(fp)

        for root, _, files in os.walk(os.path.abspath(f"{input_dir}/classifiers/")):
            for file in files:
                if file.endswith(('.tif', '.tiff', '.img')):  # Only process raster files
                    fp1 = os.path.join(root, file)
                    paths.append(fp1)

        for root, _, files in os.walk(os.path.abspath(f"{input_dir}/miscellaneous/")):
            for file in files:
                fp2 = os.path.join(root, file)
                paths.append(fp2)

        directories = [
            "disturbances", "classifiers", "miscellaneous", "templates", "db", "config"
        ]

        # Copy files, but only if the directory exists
        for directory in directories:
            directory_path = os.path.join(input_dir, directory)
            if os.path.exists(directory_path):  # Check if the directory exists
                for root, _, files in os.walk(directory_path):
                    for file in files:
                        shutil.copy2(os.path.join(root, file), input_dir)

        # Clean up the directories after copying files, again checking if they exist
        for directory in directories:
            directory_path = os.path.join(input_dir, directory)
            if os.path.exists(directory_path):
                shutil.rmtree(directory_path)
