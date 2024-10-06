from flask import Flask, send_file, flash, redirect, url_for, request, jsonify, Response
import time
import os
import subprocess
import tempfile
from flask_cors import CORS
import logging
import sys
from pathlib import Path

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
    try:
        s = time.time()
        logging.debug("Starting Visualization")
        log_file_path = Path(os.path.join(GCBM_API_OUTPUT, title, "viz_logs.csv"))
        with open(log_file_path, "w") as f:
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
            res.stdout.close()
            res.wait()

            if res.returncode != 0:
                        logging.error(f"Visualization process failed with return code {res.returncode}")
            else:
                logging.info("Visualization completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during visualization: {e}")

    logging.debug("Communicating")
    (output, err) = res.communicate()
    logging.debug("Communicated")

@app.route("/viz/logs/<title>", methods=["GET"])
def gcbm_logs(title):
    title = "".join(c for c in title if c.isalnum())
    log_file_path = os.path.join(GCBM_API_OUTPUT, title, "viz_logs.csv")
    logging.debug("Flushing logs to client")

    def generate():
        retries = 8
        delay = 3  # seconds
        last_position = 0  # To track the last read position in the file

        while retries > 0:
            if os.path.isfile(log_file_path):
                with open(log_file_path, "r") as log_file:
                    log_file.seek(last_position)  # Move to the last read position
                    for line in log_file:
                        yield f"data: {line}\n\n"  # SSE format
                    last_position = log_file.tell()  # Update the last read position
                time.sleep(delay)  # Delay before checking for new lines
            else:
                retries -= 1
                time.sleep(delay)

        if not os.path.isfile(log_file_path):
            # Log error if file is still not found after retries
            app.logger.error(f"Log file not found after retries: {log_file_path}")
            yield "data: Log file not found\n\n"  # SSE format

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
