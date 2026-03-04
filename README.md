# Path Finder

## Overview

Path Finder is a web application that computes the **k shortest simple routes between cities** using graph algorithms. It uses:

* **Dijkstra's algorithm** to compute the shortest path
* **Yen's algorithm** to compute multiple alternative shortest paths
* **FastAPI** backend with REST API
* **React + TypeScript** frontend (Vite)

The application allows users to select a start city and a destination city and visualize the available routes.

---

## Features

* FastAPI backend with JSON API
* React + TypeScript frontend
* Implementation of Yen's algorithm (manual, without external graph libraries)
* Multiple route computation between cities
* Route visualization with graph images
* Automatic API documentation at `/docs`
* Easily configurable graph structure

---

## Project Structure

```
path-finder/
│
├── main.py              # FastAPI application
├── pathfinding.py       # Dijkstra and Yen algorithms
├── graph.py             # Graph definition (cities and distances)
├── visualizer.py        # Route visualization
│
├── frontend/            # React + TypeScript frontend (Vite)
│   ├── src/
│   │   ├── App.tsx      # Main React component
│   │   ├── App.css      # Application styles
│   │   ├── index.css    # Global styles
│   │   └── main.tsx     # Entry point
│   ├── index.html
│   ├── vite.config.ts
│   └── package.json
│
├── requirements.txt
├── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/abderrahmane-beyah/path-finder-fastapi
cd path-finder-fastapi
```

### Backend

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend

Install Node.js dependencies:

```bash
cd frontend
npm install
```

---

## Run the Application

Start the backend (port 8000):

```bash
python main.py
```

Start the frontend dev server (port 5173):

```bash
cd frontend
npm run dev
```

Open in your browser:

```
http://localhost:5173
```

API documentation:

```
http://localhost:8000/docs
```

---

## Production Build

Build the frontend for production:

```bash
cd frontend
npm run build
```

The output will be in `frontend/dist/`.

---

## Changing or Adding Cities

The cities and distances are defined in:

```
graph.py
```

Example:

```python
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
* Change the positions with the new cities positions (lat, long)

The algorithm will automatically work with the updated graph.

---

## Algorithm

This project implements:

* **Dijkstra's algorithm** for computing shortest paths
* **Yen's algorithm** for computing k shortest simple paths

These algorithms ensure correct and efficient route computation.

---

## Author

Abderrahmane Beyah
