# Path Finder API (FastAPI)

## Overview

Path Finder is a web application built with **FastAPI** that computes the **k shortest simple routes between cities** using graph algorithms. It uses:

* **Dijkstra’s algorithm** to compute the shortest path
* **Yen’s algorithm** to compute multiple alternative shortest paths
* **Jinja2 templates** for the frontend interface

The application allows users to select a start city and a destination city and visualize the available routes.

---

## Features

* FastAPI backend
* Implementation of Yen’s algorithm (manual, without external graph libraries)
* Multiple route computation between cities
* Simple web interface
* Automatic API documentation at `/docs`
* Easily configurable graph structure

---

## Project Structure

```
path-finder/
│
├── main.py              # FastAPI application
├── pathfinding.py      # Dijkstra and Yen algorithms
├── graph.py            # Graph definition (cities and distances)
│
├── templates/          # HTML templates
├── static/             # CSS / JS files
│
├── requirements.txt
├── README.md
```

---

## Installation

Clone the repository:

```
git clone https://github.com/abderrahmane-beyah/path-finder-fastapi
cd path-finder-fastapi
```

Create a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## Run the application

Start the FastAPI server:

```
uvicorn main:app --reload
```

Open in your browser:

```
http://127.0.0.1:8000
```

API documentation:

```
http://127.0.0.1:8000/docs
```

---

## Changing or Adding Cities

The cities and distances are defined in:

```
graph.py
```

Example:

```
graph = {
    "Nouakchott": {
        "Atar": 400,
        "Boutilimit": 150
    },
    "Atar": {
        "Nouakchott": 400
    }
}
```

You can easily:

* Add new cities
* Remove cities
* Change distances
* Replace the entire graph with your own data
* change the positions with the new cities positions (lat,long)

The algorithm will automatically work with the updated graph.

---

## Algorithm

This project implements:

* **Dijkstra’s algorithm** for computing shortest paths
* **Yen’s algorithm** for computing k shortest simple paths

These algorithms ensure correct and efficient route computation.

---

## Author

Abderrahmane Beyah
