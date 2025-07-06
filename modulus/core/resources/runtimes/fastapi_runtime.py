from fastapi import FastAPI, Request
import uvicorn
from threading import Thread

from modulus.core.resources.task import Task
from modulus.core.resources.deployment import DeploymentRuntime


class FastAPIRuntime(DeploymentRuntime):
    def start(self, tasks: list[Task], port: int):
        app = FastAPI()

        if not tasks:
            raise ValueError("FastAPI runtime requires at least one task to expose.")

        for task in tasks:
            route_path = f"/{task.name}"

            # Define a handler for each route (closure to capture task)
            async def handler(request: Request, task=task):
                input_data = await request.json()
                result = task.start(input_data)
                return result

            # Register the route with FastAPI
            app.post(route_path)(handler)

        # Run in a separate thread to avoid blocking
        thread = Thread(
            target=uvicorn.run,
            args=(app,),
            kwargs={"host": "0.0.0.0", "port": port},
            daemon=True
        )
        thread.start()
