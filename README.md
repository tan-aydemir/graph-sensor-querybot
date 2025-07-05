# Dorm AI Monitoring System

This project demonstrates how large language models (LLMs) can be applied to structured data environments involving both graph and time-series components. It models a dormitory building with sensors and equipment, simulates environmental and occupancy data, and allows users to query the system in natural language via an interactive interface.

---

## Project Overview

This system integrates three components:

1. **Graph-based modeling** of a dormitory building and its infrastructure (e.g., rooms, AC units, sensors).
2. **Time-series simulation** of occupancy and temperature data over a 7-day period.
3. **LLM-based query interface** that enables users to ask natural language questions and receive data-driven insights.

The goal is to simulate a smart facility setting, where a user can explore building data through intuitive queries.

---

## Key Features

* Models physical relationships between rooms, AC units, and sensors using a JSON-based graph format.
* Simulates realistic sensor data at 5-minute intervals, using custom occupancy and temperature profiles.
* Parses natural language questions into structured filters (e.g., room, time range, sensor type).
* Retrieves and filters relevant data, formats context, and queries an LLM to generate responses.
* Provides a web-based interface for user interaction.

---

## Components

### `relations.json`

Defines the graph structure of the dormitory:

* 6 dorm rooms, 2 mechanical rooms
* Each dorm room has both a temperature and occupancy sensor
* Each mechanical room contains an AC unit that services 3 dorm rooms

### `generate_timeseries.py`

Simulates 7 days of sensor readings at 5-minute intervals. Each dorm room is assigned:

* A temperature profile (based on sun exposure and time of day)
* An occupancy profile (either full-time or night-shift pattern)

> This script can be used independently to generate compatible time-series datasets:

```bash
python generate_timeseries.py
```

### `slice_json.py`

Handles LLM-based querying. Responsibilities include:

* Extracting filters from user queries (e.g., time range, room ID)
* Reading and filtering sensor data
* Merging the graph and sensor data into a prompt
* Sending the prompt to OpenAI’s API and returning the response

> Note: You must add your own OpenAI API key in this file to use it.

### `streamlit_app.py`

Provides a simple Streamlit interface:

* Accepts natural language queries
* Shows output from the model
* Includes sample questions for reference

Launch using:

```bash
streamlit run app/ui.py
```

---
---

## Example Queries

* What rooms are serviced by AC Unit 1?
* What is the average temperature in Dorm\_103?
* Which rooms are typically hot in the afternoon?
* Can I forecast occupancy in Dorm\_105?
* What sensors are in Dorm\_106?

---

## Notes
* The project uses `gpt-4o-mini` for both filter extraction and answering user queries
---
