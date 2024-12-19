# FLINT/GCBMx Web Application Documentation

## Overview
FLINT/GCBMx is a web-based tool for running forest carbon modeling simulations and visualizations. The application helps users analyze and understand forest carbon dynamics through various models including RothC (soil carbon) and GCBM (forest carbon budget).

## System Components

### 1. User Interface (`user-ui/`)
- Modern web interface built with Vue.js
- Provides interactive forms for model configuration
- Visualization tools for simulation results
- Support for both point-based and spatial simulations

### 2. FLINT API (`flint-api/`)
- REST API for running FLINT simulations
- Supports different modeling modules:
  - Point-based simulations
  - RothC soil carbon modeling
  - GCBM forest carbon budget modeling
- Handles configuration management and simulation execution

### 3. Data API (`data-api/`)
- Manages data storage and retrieval
- Handles simulation input/output data

### 4. Visualization API (`viz-api/`)
- Processes and serves visualization data
- Supports various data visualization formats

## Key Features
1. **Multiple Simulation Types**
   - Point-based carbon modeling
   - RothC soil carbon simulations
   - GCBM spatial forest carbon modeling

2. **Interactive Configuration**
   - User-friendly configuration interfaces
   - Parameter validation and preset templates
   - Support for multiple input formats

3. **Visualization Tools**
   - Interactive maps for spatial data
   - Time series graphs for results
   - Customizable data views

4. **Data Management**
   - Input data validation
   - Result storage and retrieval
   - Export capabilities

## Setup Guide

### Prerequisites
- Docker and Docker Compose
- Node.js (for UI development)
- Modern web browser

### Installation Steps

1. Clone the repository

2. Start the backend services:
```bash
docker-compose up
```

3. For UI development:
```bash
cd user-ui
npm install
npm run serve
```

The application will be available at http://localhost:8080 by default.

## Usage Workflows

### GCBM Simulation
1. Upload spatial input data
2. Configure simulation parameters
3. Run the simulation
4. View and analyze results

### RothC Soil Carbon Modeling
1. Input soil and climate parameters
2. Configure simulation timeframe
3. Execute the model
4. Analyze carbon pool results

### Point-Based Simulation
1. Set point parameters
2. Configure temporal settings
3. Run simulation
4. View time series results

This comprehensive web application serves as a powerful tool for forest carbon modeling and analysis, making complex simulations accessible through an intuitive web interface.