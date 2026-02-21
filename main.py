from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from pydantic import BaseModel
from pathfinding import k_shortest_paths
from graph import cities_graph
from visualizer import visualize_route
import uvicorn

app = FastAPI()

# Mount static files and setup templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# List of cities for dropdown menus
CITY_NAMES = sorted(list(cities_graph.keys()))


class RouteRequest(BaseModel):
    start_city: str
    end_city: str


class PathInfo(BaseModel):
    numero: int
    chemin: list
    route_str: str
    distance: float
    difference: float
    pourcentage: float
    est_optimal: bool


class RouteResponse(BaseModel):
    error: str | None = None
    image_data: str | None = None
    selected_start: str | None = None
    selected_end: str | None = None
    all_paths: list[PathInfo] = []
    cities: list = []


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    """Serve the main page"""
    return templates.TemplateResponse("index.html", {"request": request, "cities": CITY_NAMES})


@app.post("/api/routes")
async def find_routes(route_request: RouteRequest):
    """Find routes between two cities"""
    selected_start = route_request.start_city
    selected_end = route_request.end_city
    error = None
    image_data = None
    all_paths = []

    # Basic validation
    if not selected_start or not selected_end:
        error = "Start and end cities must be selected."
        return RouteResponse(error=error, selected_start=selected_start, selected_end=selected_end, cities=CITY_NAMES)

    if selected_start == selected_end:
        error = "Start and end cities must be different."
        return RouteResponse(error=error, selected_start=selected_start, selected_end=selected_end, cities=CITY_NAMES)

    if selected_start not in CITY_NAMES or selected_end not in CITY_NAMES:
        error = "Invalid city selection."
        return RouteResponse(error=error, selected_start=selected_start, selected_end=selected_end, cities=CITY_NAMES)

    # Find the k shortest paths (maximum 3)
    paths = k_shortest_paths(cities_graph, selected_start, selected_end, k=3, max_ratio=1.5)

    if paths:
        # Prepare data for display
        optimal_distance = paths[0][0]

        for i, (distance, path) in enumerate(paths):
            route_str = ' → '.join(path)
            difference = distance - optimal_distance
            percentage = ((distance / optimal_distance) - 1) * 100 if i > 0 else 0

            all_paths.append(PathInfo(
                numero=i + 1,
                chemin=path,
                route_str=route_str,
                distance=distance,
                difference=difference,
                pourcentage=percentage,
                est_optimal=i == 0
            ))

        # Visualization (returns PNG image in base64)
        try:
            image_data = visualize_route(cities_graph, paths, selected_start, selected_end)
        except Exception as e:
            # If visualization fails, continue without image but don't crash the application
            print(f"Visualization error: {e}")
            image_data = None
    else:
        error = f"Cannot find a path from {selected_start} to {selected_end}."

    return RouteResponse(
        error=error,
        image_data=image_data,
        selected_start=selected_start,
        selected_end=selected_end,
        all_paths=all_paths,
        cities=CITY_NAMES
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)