import os
import requests
import geopandas as gpd
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(
    app,
    origins=[
        "http://127.0.0.1:8080/",
        "http://127.0.0.1:8000",
        "http://localhost:5000",
        "http://localhost:8000",
        r"^https://.+example.com$",
    ],
)

# Utility functions
def download_dataset(url, save_path):
    """Download a file from a given URL and save it locally."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(f"Failed to download dataset from {url}")

def plot_vector_dataset(file_path):
    """Plot a vector dataset (e.g., shapefile, GeoJSON) using geopandas and matplotlib."""
    gdf = gpd.read_file(file_path)
    gdf.plot()
    plt.title(f"Vector Dataset: {os.path.basename(file_path)}")
    plt.show()

def plot_raster_dataset(file_path):
    """Plot a raster dataset (e.g., GeoTIFF) using rasterio and matplotlib."""
    with rasterio.open(file_path) as src:
        show(src)
        plt.title(f"Raster Dataset: {os.path.basename(file_path)}")
        plt.show()

def plot_dataset(file_path, dataset_type):
    """Unified function to plot either raster or vector datasets based on dataset_type."""
    if dataset_type == "vector":
        plot_vector_dataset(file_path)
    elif dataset_type == "raster":
        plot_raster_dataset(file_path)
    else:
        raise ValueError("Unsupported dataset type!")

def clip_vector_dataset(dataset_path, clip_geom_path, output_path):
    """Clip a vector dataset (shapefile) by a geometry."""
    gdf = gpd.read_file(dataset_path)
    clip_geom = gpd.read_file(clip_geom_path)
    clipped = gpd.clip(gdf, clip_geom)
    clipped.to_file(output_path)
    print(f"Clipped vector dataset saved to {output_path}")

def clip_raster_dataset(raster_path, output_path, minx, miny, maxx, maxy):
    """Clip a raster dataset (GeoTIFF) by bounding box (minx, miny, maxx, maxy)."""
    with rasterio.open(raster_path) as src:
        bbox = rasterio.windows.from_bounds(minx, miny, maxx, maxy, src.transform)
        clipped = src.read(window=bbox)
        out_meta = src.meta.copy()
        out_meta.update({
            "height": bbox.height,
            "width": bbox.width,
            "transform": rasterio.windows.transform(bbox, src.transform)
        })
        with rasterio.open(output_path, "w", **out_meta) as dest:
            dest.write(clipped)
    print(f"Clipped raster dataset saved to {output_path}")

def clip_dataset(dataset_path, output_path, dataset_type, clip_geom_path=None, bbox=None):
    """Unified function to clip either raster or vector datasets."""
    if dataset_type == "vector":
        if not clip_geom_path:
            raise ValueError("clip_geom_path is required for vector datasets!")
        clip_vector_dataset(dataset_path, clip_geom_path, output_path)
    elif dataset_type == "raster":
        if not bbox:
            raise ValueError("Bounding box (bbox) is required for raster datasets!")
        clip_raster_dataset(dataset_path, output_path, *bbox)
    else:
        raise ValueError("Unsupported dataset type!")

def view_dataset_as_dataframe(file_path):
    """Convert a vector dataset to a pandas DataFrame."""
    gdf = gpd.read_file(file_path)
    return gdf

# API route handlers
@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        url = data['url']
        save_path = data['save_path']
        download_dataset(url, save_path)
        return jsonify({"message": "Dataset downloaded successfully!"}), 200
    except KeyError:
        return jsonify({"error": "Invalid input data!"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)
        return jsonify({"message": "File uploaded successfully!", "file_path": file_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/plot', methods=['POST'])
def plot():
    try:
        data = request.get_json()
        file_path = data['file_path']
        dataset_type = data.get('dataset_type', 'vector')  # Default to 'vector'

        plot_dataset(file_path, dataset_type)
        return jsonify({"message": f"{dataset_type.capitalize()} dataset plotted!"}), 200
    except KeyError:
        return jsonify({"error": "Invalid input data!"}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clip', methods=['POST'])
def clip():
    try:
        data = request.get_json()
        dataset_path = data['dataset_path']
        output_path = data['output_path']
        dataset_type = data.get('dataset_type', 'vector')  # Default to 'vector'

        # Handle clip based on dataset type
        if dataset_type == 'vector':
            clip_geom_path = data['clip_geom_path']
            clip_dataset(dataset_path, output_path, dataset_type, clip_geom_path=clip_geom_path)
        elif dataset_type == 'raster':
            bbox = data['bbox']  # bounding box as [minx, miny, maxx, maxy]
            clip_dataset(dataset_path, output_path, dataset_type, bbox=bbox)
        else:
            return jsonify({"error": "Unsupported dataset type!"}), 400

        return jsonify({"message": f"{dataset_type.capitalize()} dataset clipped!", "output_path": output_path}), 200
    except KeyError:
        return jsonify({"error": "Invalid input data!"}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dataframe', methods=['POST'])
def dataframe():
    try:
        file_path = request.json['file_path']
        df = view_dataset_as_dataframe(file_path)
        return df.to_json(), 200
    except KeyError:
        return jsonify({"error": "Invalid input data!"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Main entry point
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
