from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api.v1.endpoints import router as api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
templates = Jinja2Templates(directory="templates")

# Include API routes
app.include_router(api_router, prefix="/api/v1")
# For backward compatibility if needed, or just redirect. 
# Let's keep the old /api for now or use the new /api/v1 in templates.
app.include_router(api_router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
