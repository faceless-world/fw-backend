"""
Main file to start Faceless World backend
"""

import importlib
import os
import threading
from typing import List
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute, APIRouter
from modules.api.auth import schedule_key_rotation


def import_routers_from_directory(directory: str = "routes") -> APIRouter:
    """
    Import all routes from modules
    :param directory: Directory with routes
    :type directory: str
    :return: Api router
    :rtype: APIRouter
    """
    main_router = APIRouter()

    for filename in os.listdir(directory):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"{directory}.{filename[:-3]}"
            module = importlib.import_module(module_name)

            if hasattr(module, "router"):
                main_router.include_router(module.router)

    return main_router


if __name__ == "__main__":
    app = FastAPI()
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(import_routers_from_directory())


    @app.get("/")
    def get_routes() -> List[dict]:
        """
        Return all routes from FastApi
        :return: All routes from FastApi
        :rtype: List[dict]
        """
        routes_list = []
        for route in app.routes:
            if isinstance(route, APIRoute):
                routes_list.append({
                    "path": route.path,
                    "methods": list(route.methods),
                    "name": route.name,
                })
        return routes_list

    # Start key rotation in a separate thread
    rotation_interval_seconds = 3600  # Rotate key every hour (adjust as needed)
    rotation_thread = threading.Thread(target=schedule_key_rotation, args=(rotation_interval_seconds,))
    rotation_thread.daemon = True
    rotation_thread.start()

    uvicorn.run(app, host="0.0.0.0", port=12420)
