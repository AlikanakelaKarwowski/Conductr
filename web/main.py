# web/main.py
import os
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from prometheus_client import (
    CollectorRegistry,
    Counter,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

app = FastAPI(title="web")

# simple templating + (optional) static dir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
static_path = os.path.join(BASE_DIR, "static")
if not os.path.exists(static_path):
    os.makedirs(static_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_path), name="static")

# minimal metrics
registry = CollectorRegistry()
page_hits = Counter("web_page_hits_total", "Homepage hits", registry=registry)


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.get("/", response_class=PlainTextResponse)
def index(request: Request):
    page_hits.inc()
    # render an html template:
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": "Symphony Web",
            "env": os.getenv("ENV", "dev"),
        },
    )


@app.get("/metrics")
def metrics():
    return PlainTextResponse(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)
