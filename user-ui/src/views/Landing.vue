<template>
  <div class="parent">
    <!-- Left half: Leaflet Map -->
    <div class="left-half">
      <div ref="mapElement" class="leaflet-map"></div>

      <div class="search-container">
        <div class="search-input-wrapper">
          <input
            type="text"
            v-model="query"
            @input="search"
            placeholder="Enter Area of Interest"
            class="search-input"
          />
          <button class="search-button" @click="search" aria-label="Search">
            <i class="fas fa-search"></i>
          </button>
        </div>

        <ul v-if="suggestions.length" class="suggestions-list">
          <li v-for="(suggestion, index) in suggestions" :key="index" @click="selectSuggestion(suggestion)">
            {{ suggestion.display_name }}
          </li>
        </ul>

        <div class="search-info" v-if="resultInfo">
          <h3>Search Result</h3>
          <p>{{ resultInfo }}</p>
        </div>
      </div>

      <div v-show="infoPaneVisible" class="info-pane">
        <button class="close-button" @click="infoPaneVisible = false" aria-label="Close Information Pane">&times;</button>
        <h3>Information</h3>
        <p>{{ resultInfo }}</p>
      </div>

      <div class="control-panel">
        <button @click="showMyLocation" title="Show My Location" aria-label="Show My Location">
          <i class="fas fa-location-arrow"></i>
        </button>
        <button @click="toggleLayer" title="Toggle Layer" aria-label="Toggle Layer">
          <i class="fas fa-layer-group"></i>
        </button>
        <button @click="showMapKey" title="Map Key" aria-label="Map Key">
          <i class="fas fa-info-circle"></i>
        </button>
      </div>
    </div>

    <!-- Right half: Data Preprocessing -->
    <div class="right-half">
      <!-- Title -->
      <h1 class="data-processing-title">Preprocessing</h1>

      <!-- Sections for Data Preprocessing -->
      <div class="preprocessing-section">
        <h2>Get Administrative Boundaries</h2>
        <div class="input-group">
          <label>Upload Dataset</label>
          <input type="file" @change="uploadFile" class="input-file" />
        </div>
        <div class="input-group">
          <label>Download Dataset</label>
          <input v-model="downloadUrl" placeholder="Enter dataset URL" class="input-text" />
          <button @click="downloadDataset" class="input-button">Download</button>
        </div>
        <div class="input-group">
          <button @click="plotDataset" class="input-button">Plot</button>
          <button @click="clipDataset" class="input-button">Clip</button>
          <button @click="viewAsDataframe" class="input-button">View</button>
        </div>
      </div>

      <div class="preprocessing-section">
        <h2>Get Ecological Zone</h2>
        <div class="input-group">
          <label>Upload Dataset</label>
          <input type="file" @change="uploadFile" class="input-file" />
        </div>
        <div class="input-group">
          <label>Download Dataset</label>
          <input v-model="downloadUrl" placeholder="Enter dataset URL" class="input-text" />
          <button @click="downloadDataset" class="input-button">Download</button>
        </div>
        <div class="input-group">
          <button @click="plotDataset" class="input-button">Plot</button>
          <button @click="clipDataset" class="input-button">Clip</button>
          <button @click="viewAsDataframe" class="input-button">View</button>
        </div>
      </div>

      <div class="preprocessing-section">
        <h2>Get Holdridge Life Zone</h2>
        <div class="input-group">
          <label>Upload Dataset</label>
          <input type="file" @change="uploadFile" class="input-file" />
        </div>
        <div class="input-group">
          <label>Download Dataset</label>
          <input v-model="downloadUrl" placeholder="Enter dataset URL" class="input-text" />
          <button @click="downloadDataset" class="input-button">Download</button>
        </div>
        <div class="input-group">
          <button @click="plotDataset" class="input-button">Plot</button>
          <button @click="clipDataset" class="input-button">Clip</button>
          <button @click="viewAsDataframe" class="input-button">View</button>
        </div>
      </div>

      <div class="preprocessing-section">
        <h2>Get Forest Cover</h2>
        <div class="input-group">
          <label>Upload Dataset</label>
          <input type="file" @change="uploadFile" class="input-file" />
        </div>
        <div class="input-group">
          <label>Download Dataset</label>
          <input v-model="downloadUrl" placeholder="Enter dataset URL" class="input-text" />
          <button @click="downloadDataset" class="input-button">Download</button>
        </div>
        <div class="input-group">
          <button @click="plotDataset" class="input-button">Plot</button>
          <button @click="clipDataset" class="input-button">Clip</button>
          <button @click="viewAsDataframe" class="input-button">View</button>
        </div>
      </div>

      <div class="preprocessing-section">
        <h2>Get Mean Annual Temperature</h2>
        <div class="input-group">
          <label>Upload Dataset</label>
          <input type="file" @change="uploadFile" class="input-file" />
        </div>
        <div class="input-group">
          <label>Download Dataset</label>
          <input v-model="downloadUrl" placeholder="Enter dataset URL" class="input-text" />
          <button @click="downloadDataset" class="input-button">Download</button>
        </div>
        <div class="input-group">
          <button @click="plotDataset" class="input-button">Plot</button>
          <button @click="clipDataset" class="input-button">Clip</button>
          <button @click="viewAsDataframe" class="input-button">View</button>
        </div>
      </div>

      <div class="tiler-configuration">
        <h2>Configure and Run Tiler</h2>

        <!-- Bounding Box Configuration -->
        <div class="input-group">
          <label for="bbox">Bounding Box Shapefile:</label>
          <input type="file" @change="handleFileUpload('bbox')" id="bbox" class="input-file" />
          <input type="text" v-model="bboxAttribute" placeholder="Enter Bounding Box Attribute (e.g., PolyID)" class="input-text" />
        </div>

        <!-- Classifier Layers Configuration -->
        <div class="input-group">
          <h3>Classifier Layers</h3>
          <div v-for="(classifier, index) in classifiers" :key="index">
            <label :for="'classifier' + index">Classifier {{ index + 1 }} Shapefile:</label>
            <input type="file" @change="handleFileUpload('classifier', index)" :id="'classifier' + index" class="input-file" />
            <input type="text" v-model="classifier.attribute" placeholder="Enter Attribute (e.g., Classifier1)" class="input-text" />
          </div>
          <button @click="addClassifier" class="input-button">Add Classifier</button>
        </div>

        <!-- Disturbances Configuration -->
        <div class="input-group">
          <h3>Disturbance Layers</h3>
          <label for="disturbances-shp">Disturbance Shapefile:</label>
          <input type="file" @change="handleFileUpload('disturbances')" id="disturbances-shp" class="input-file" />
          <label for="year-range">Year Range:</label>
          <input type="number" v-model="yearStart" placeholder="Start Year" class="input-text small-input" />
          <input type="number" v-model="yearEnd" placeholder="End Year" class="input-text small-input" />
        </div>

        <!-- Initial Layers (e.g., Age, Temperature) -->
        <div class="input-group">
          <label for="age-shp">Initial Age Shapefile:</label>
          <input type="file" @change="handleFileUpload('initial_age')" id="age-shp" class="input-file" />
          <input type="text" v-model="ageAttribute" placeholder="Enter Age Attribute (e.g., AGE_2010)" class="input-text" />
        </div>
        <div class="input-group">
          <label for="temp-shp">Mean Annual Temperature Shapefile:</label>
          <input type="file" @change="handleFileUpload('mean_annual_temperature')" id="temp-shp" class="input-file" />
          <input type="text" v-model="tempAttribute" placeholder="Enter Temperature Attribute (e.g., AnnualTemp)" class="input-text" />
        </div>

        <!-- Button to Run Tiler -->
        <button @click="runTiler" class="input-button">Run Tiler</button>
      </div>
      </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import 'leaflet/dist/leaflet.css';
import '@fortawesome/fontawesome-free/css/all.css';
import axios from 'axios';
import L from 'leaflet';

const zoom = ref(5);
const center = ref([51.505, -0.09]);
const osmUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const googleSatelliteUrl = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}';
const currentUrl = ref(osmUrl);
const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';

const markerPosition = ref([51.505, -0.09]);
const resultInfo = ref('');
const infoPaneVisible = ref(false);

const query = ref('');
const suggestions = ref([]);
const map = ref(null);
const mapElement = ref(null);
const bboxAttribute = ref('');
const classifiers = ref([{ attribute: '' }]);
const yearStart = ref(2010);
const yearEnd = ref(2020);
const ageAttribute = ref('');
const tempAttribute = ref('');

const handleFileUpload = (type, index = null) => {
  // Handle file uploads for bounding box, classifiers, disturbances, and other layers.
  // You would typically send the file to the backend or store it in the appropriate ref.
  console.log(`Uploading file for: ${type}`, index);
};

const addClassifier = () => {
  classifiers.value.push({ attribute: '' });
};

const runTiler = () => {
  // Construct the configuration based on user inputs and trigger the backend to run the tiler.
  const tilerConfig = {
    bbox: {
      attribute: bboxAttribute.value,
    },
    classifiers: classifiers.value,
    disturbances: {
      yearStart: yearStart.value,
      yearEnd: yearEnd.value,
    },
    initialLayers: {
      age: ageAttribute.value,
      temperature: tempAttribute.value,
    },
  };
  console.log('Running tiler with config:', tilerConfig);

  // Here you would send tilerConfig to your backend for processing.
};

onMounted(() => {
  if (mapElement.value) {
    map.value = L.map(mapElement.value).setView(center.value, zoom.value);

    L.tileLayer(osmUrl, {
      attribution: attribution
    }).addTo(map.value);
  }
});

const search = async () => {
  const searchQuery = query.value.trim().toLowerCase();
  if (searchQuery.length < 3) {
    suggestions.value = [];
    return;
  }

  try {
    const response = await axios.get('https://nominatim.openstreetmap.org/search', {
      params: {
        q: searchQuery,
        format: 'json',
        addressdetails: 1,
        limit: 1
      }
    });

    if (response.data.length > 0) {
      const suggestion = response.data[0];
      const lat = parseFloat(suggestion.lat);
      const lon = parseFloat(suggestion.lon);
      center.value = [lat, lon];
      markerPosition.value = [lat, lon];
      resultInfo.value = `Place: ${suggestion.display_name}`;
      infoPaneVisible.value = true;

      map.value.setView(center.value, 13); // Dynamically zoom to the searched area

      const boundariesData = await fetchBoundaries(suggestion.osm_id);
      displayBoundaries(boundariesData);
    }

    suggestions.value = response.data;
  } catch (error) {
    console.error(error);
    suggestions.value = [];
  }
};


const fetchBoundaries = async (osmId) => {
  const overpassUrl = 'https://overpass-api.de/api/interpreter';
  const queryStr = `
    [out:json];
    relation(${osmId});
    out geom;
  `;

  try {
    const response = await axios.post(overpassUrl, `data=${encodeURIComponent(queryStr)}`, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching boundaries:', error);
    return null;
  }
};

const displayBoundaries = (data) => {
  if (!data || !data.elements) return;

  if (map.value && map.value.eachLayer) {
    map.value.eachLayer(layer => {
      if (layer instanceof L.GeoJSON) {
        map.value.removeLayer(layer);
      }
    });

    const boundaries = data.elements.map(element => {
      if (element.type === 'relation' && element.geometry) {
        return {
          type: 'Feature',
          geometry: {
            type: 'Polygon',
            coordinates: [element.geometry.map(geom => [geom.lon, geom.lat])]
          },
          properties: {
            name: element.tags.name || 'Unnamed'
          }
        };
      }
    }).filter(Boolean);

    if (boundaries.length > 0) {
      L.geoJSON(boundaries, {
        style: {
          color: 'blue',
          weight: 2
        }
      }).addTo(map.value);
    }
  } else {
    console.error('Map instance is not initialized or not valid');
  }
};

const selectSuggestion = (suggestion) => {
  const lat = parseFloat(suggestion.lat);
  const lon = parseFloat(suggestion.lon);
  center.value = [lat, lon];
  markerPosition.value = [lat, lon];
  query.value = suggestion.display_name;
  suggestions.value = [];

  map.value.setView(center.value, 13); // Dynamically zoom to the selected area

  if (suggestion.boundingbox) {
    const bbox = suggestion.boundingbox.map(Number);
    const bounds = [
      [bbox[0], bbox[2]],
      [bbox[1], bbox[3]]
    ];
    map.value.fitBounds(bounds); // Fit the map to the bounding box
  }

  resultInfo.value = `Place: ${suggestion.display_name}`;
  infoPaneVisible.value = true;
};

const showMyLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        center.value = [position.coords.latitude, position.coords.longitude];
        markerPosition.value = [position.coords.latitude, position.coords.longitude];
        map.value.setView(center.value, 13); // Dynamically zoom to the current location
      },
      (error) => {
        console.error('Error getting location:', error);
      }
    );
  }
};

const toggleLayer = () => {
  if (!map.value) return;

  const newLayerUrl = currentUrl.value === osmUrl ? googleSatelliteUrl : osmUrl;
  L.tileLayer(newLayerUrl, {
    attribution: attribution
  }).addTo(map.value);

  currentUrl.value = newLayerUrl;
};

const showMapKey = () => {
  alert('Map key functionality to be implemented.');
};
</script>

<style scoped>
.tiler-configuration {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.input-group {
  margin-bottom: 15px;
}

.input-text {
  padding: 5px;
  border: 1px solid #ccc;
  width: 100%;
}

.small-input {
  width: 100px;
  margin-right: 10px;
}

.input-button {
  padding: 5px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.input-file {
  margin-bottom: 10px;
}

.parent {
  display: flex;
  height: 100vh;
}

.left-half {
  flex: 1;
  position: relative;
}

.leaflet-map {
  height: 100%;
  width: 100%;
}

.search-container, .info-pane, .control-panel {
  position: absolute;
  z-index: 1000;
}

.search-container {
  top: 20px;
  left: 50px;
  width: 300px;
}

.search-input-wrapper {
  display: flex;
}

.search-input {
  flex: 1;
  padding: 5px;
  border: 1px solid #ccc;
}

.search-button {
  padding: 5px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.suggestions-list {
  margin: 0;
  padding: 5px;
  background: white;
  border: 1px solid #ccc;
}

.suggestions-list li {
  cursor: pointer;
  padding: 5px;
}

.search-info {
  margin-top: 10px;
}

.info-pane {
  top: 80px;
  right: 10px;
  background: white;
  padding: 10px;
  border: 1px solid #ccc;
}

.control-panel {
  top: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.control-panel button {
  background: white;
  border: 1px solid #ccc;
  padding: 5px;
  cursor: pointer;
}

.right-half {
  flex: 1;
  padding: 20px;
  background-color: #f4f4f4;
  overflow-y: auto;
}

.data-processing-title {
  font-size: 32px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
}

.preprocessing-section {
  margin-bottom: 30px;
  background-color: #ffffff;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.preprocessing-section h2 {
  margin-bottom: 15px;
  font-size: 24px;
}

.input-group {
  margin-bottom: 15px;
}

.input-text {
  width: calc(100% - 100px);
  padding: 5px;
  border: 1px solid #ccc;
}

.input-button {
  padding: 5px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.input-file {
  padding: 5px;
  border: 1px solid #ccc;
  display: inline-block;
  margin-right: 10px;
}
</style>