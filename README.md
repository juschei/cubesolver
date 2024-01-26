# Basic Cubesolver

Provides a FastAPI backend with an internal representation of the 3x3x3 Rubik's cube.

## Usage

The webservice can be either locally started via uvicorn (see Dockerfile) or you can use the [Docker image](https://hub.docker.com/r/juschei/cubesolver).

To get started, run

```
docker run --publish 0.0.0.0:2900:2900 juschei/cubesolver:latest
```

After successful startup,  see the API documentation at `localhost:2900/docs`.