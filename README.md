<div align="center">
<img src="https://moja.global/wp-content/uploads/2021/03/Asset-66@4x.png" alt="FLINT UI logo" height ="auto" width="200" />
<br />
<h1>GCBMx</h1>
<p>
  🚧🚧🚧🚧

  A FLINT client, written in Vue, to provide an awesome user interface for configuring simulations using the FLINT.Cloud APIs

  This is experimental and incomplete. The framework may be a useful starting point for new users who wish to create their own interface

  🚧🚧🚧🚧
</p>
<a href="https://github.com/moja-global/FLINT-UI"><img src="https://img.shields.io/github/contributors/moja-global/FLINT-UI.svg?color=74e8a3&style=flat-square" /></a>
<a href="https://github.com/moja-global/FLINT-UI/network/members"><img src="https://img.shields.io/github/forks/moja-global/FLINT-UI?color=74e8a3&style=flat-square" /></a>
<a href="https://github.com/moja-global/FLINT-UI/stargazers"><img src="https://img.shields.io/github/stars/moja-global/FLINT-UI?color=74e8a3&style=flat-square" /></a>
<a href="https://github.com/moja-global/FLINT-UI/blob/master/LICENSE"><img src="https://img.shields.io/github/license/moja-global/FLINT-UI?color=74e8a3&style=flat-square" /></a>
</div>

<br />

# GCBMx - Greenhouse Gas Accounting Automation Tool

## Project Overview

The **GCBMx** project is focused on developing and deploying a comprehensive tool that automates various tasks related to Greenhouse Gas (GHG) accounting using the **Generic Carbon Budget Model (GCBM)**. The tool integrates multiple functionalities, including:

- **Configuration Management**
- **Data Management**
- **Simulation Configuration**
- **Data Preprocessing**
- **Visualization of Results**
- **Data Export**

By streamlining these processes, **GCBMx** aims to facilitate efficient GHG accounting and help users analyze environmental data more effectively.

## Key Features

- **Automated Data Fetching**: GCBMx automates the process of fetching relevant datasets.
- **Data Preprocessing**: Provides preprocessing functionality for both vector and raster datasets.
- **Simulation Configuration**: Automates the configuration of simulation models using GCBM, simplifying the setup process.
- **Visualization Tools**: Supports visualizing results through intuitive plots and dashboards.
- **Data Export**: Enables easy export of results for further analysis or reporting purposes.

## Project Phases

The project follows a phased approach to ensure proper planning, development, and deployment:

1. **Design and Planning**
   In this phase, the project scope, features, and technical requirements are defined. It includes:
   - Identifying project goals and target users.
   - Drafting a technical plan for integrating GCBM with data management and visualization tools.

2. **Development**
   The core functionalities of GCBMx are implemented in this phase, including:
   - Creating APIs for fetching and processing data.
   - Building interfaces for managing configurations and visualizing results.

3. **Testing**
   During this phase, the tool is rigorously tested to ensure all functionalities work as expected, including:
   - Unit and integration tests for APIs and components.
   - End-to-end testing of the GHG accounting workflow.

4. **Deployment**
   The final phase involves deploying the tool into a production environment using **Docker Compose**. The deployed tool will be publicly accessible and ready for use by end users.

## System Requirements

- **Docker** and **Docker Compose** are required to build and run the services.
- Basic knowledge of **GHG accounting** and the **GCBM** model is recommended for users.

## Setup and Installation

### Prerequisites

1. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).
2. At least 4GB RAM
3. 10GB free disk space
4. Internet connection

### Installation Options

#### Option 1: Building from Source (Typical developer option)
1. Clone the project repository:

   ```bash
   git clone https://github.com/yourusername/GCBMx.git
   cd gcbmx

2. Build and run using docker-compose
   ```bash
   docker-compose up -d --build

#### Option 2: Using Pre-built Images from Docker Hub (Typical user option)
1. Copy the docker-compose.yml from the repo [GCBMx docker compose](https://github.com/moja-global/GCBMx/blob/main/docker-compose.yml)
   ```bash
   docker-compose -f docker-compose.yml up -d

### Verification and usage
 - Check if containers are running
   ```bash
   docker-compose ps

### Common commands
 - Start the application
   ```bash
   docker-compose up -d

 - Stop the application
   ```bash
   docker-compose down

### Updating the Application
 - For source-built version
   ```bash
   git pull
   docker-compose down
   docker-compose up -d --build

 - For Docker Hub version
   ```bash
   docker-compose -f docker-compose.yml down
   docker-compose -f docker-compose.yml pull
   docker-compose -f docker-compose.yml up -d

### Read More

Find more comprehensive details about Moja Global Contributing Guidelines [here.](https://github.com/moja-global/About_moja_global/tree/master/Contributing#community-contributions).

## How to Get Involved?

moja global welcomes a wide range of contributions as explained in [Contributing document](https://github.com/moja-global/About-moja-global/blob/master/CONTRIBUTING.md) and the [About moja-global Wiki](https://github.com/moja-global/.github/wiki).

## FAQ and Other Questions

- You can find FAQs on the [Wiki](https://community.moja.global/docs/about-moja-global).
- If you have a question about the code, submit [user feedback](https://github.com/moja-global/About-moja-global/blob/master/Contributing/How-to-Provide-User-Feedback.md) in the relevant repository
- If you have a general question about a project or repository or moja global, [join moja global](https://github.com/moja-global/About-moja-global/blob/master/Contributing/How-to-Join-moja-global.md) and
  - [submit a discussion](https://help.github.com/en/articles/about-team-discussions) to the project, repository or moja global [team](https://github.com/orgs/moja-global/teams)
  - [submit a message](https://get.slack.help/hc/en-us/categories/200111606#send-messages) to the relevant channel on [moja global's Slack workspace](https://mojaglobal.slack.com/).
- If you have other questions, please write to info@moja.global

## Contributors

Thanks go to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
<table><tr><td align="center"><a href="http://moja.global"><img src="https://avatars1.githubusercontent.com/u/19564969?v=4" width="100px;" alt="moja global"/><br /><sub><b>moja global</b></sub></a><br /><a href="#projectManagement-moja-global" title="Project Management">📆</a></td></tr></table>

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind are welcome!

## Maintainers Reviewers Ambassadors Coaches

The following people are Maintainers, Reviewers, Ambassadors, or Coaches.

<table><tr><td align="center"><a href="http://moja.global"><img src="https://avatars1.githubusercontent.com/u/19564969?v=4" width="100px;" alt="moja global"/><br /><sub><b>moja global</b></sub></a><br /><a href="#projectManagement-moja-global" title="Project Management">📆</a></td></tr></table>

- **Maintainers** review and accept proposed changes
- **Reviewers** check proposed changes before they go to the Maintainers
- **Ambassadors** are available to provide training related to this repository
- **Coaches** are available to provide information to new contributors to this repository

## License

This project is released under the [Mozilla Public License Version 2.0](https://github.com/moja-global/FLINT-UI/blob/master/LICENSE).
