from flask import Flask, send_file, flash, redirect, url_for, request, jsonify
import time
import os
import subprocess
import tempfile
from flask_cors import CORS
import logging
import sys

app = Flask(__name__)
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

# Define the paths to the output directories
GCBM_API_OUTPUT = '/shared-output'

@app.route("/viz", methods=["POST"])
def run_visualization():
    # Get simulation name from request
    title = request.form.get("title").strip()
    if not title:
        return jsonify({"error": "Simulation name is required"}), 400

    # Construct paths
    SPATIAL = os.path.join(GCBM_API_OUTPUT, title, "spatial")
    ASPATIAL = os.path.join(GCBM_API_OUTPUT, title, "aspatial", "compiled_gcbm_output.db")
    CONFIG = os.path.join(GCBM_API_OUTPUT, title, "config", "config.json")
    simulation_folder = os.path.join(GCBM_API_OUTPUT, title)

    if not os.path.exists(ASPATIAL):
        return jsonify({"error": "Simulation database not found"}), 404
    if not os.path.exists(CONFIG):
        return jsonify({"error": "Config file not found"}), 404
    if not os.path.exists(SPATIAL):
                return jsonify({"error": "Spatial output files not found"}), 404

    # Construct the command
    s = time.time()
    logging.debug("Starting Visualization")
    with open(f"{GCBM_API_OUTPUT}/{title}/viz_logs.csv", "w") as f:
        res = subprocess.Popen(
            [
                "taswira",
                "--allow-unoptimized",
                f"{CONFIG}",
                f"{SPATIAL}",
                f"{ASPATIAL}",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            cwd=f"{simulation_folder}",
        )
        for line in res.stdout:
            sys.stdout.write(line)
            f.write(line)
            f.flush()
        res.wait()

    logging.debug("Communicating")
    (output, err) = res.communicate()
    logging.debug("Communicated")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
