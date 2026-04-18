from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

app = FastAPI(title="Calc", version="1.0.0")
templates = Jinja2Templates(directory="templates")


class AddRequest(BaseModel):
    a: int = Field(..., examples=[2])
    b: int = Field(..., examples=[3])


class AddResponse(BaseModel):
    result: int
    computed_at: str


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/api/add", response_model=AddResponse)
def api_add(body: AddRequest) -> AddResponse:
    return AddResponse(
        result=body.a + body.b,
        computed_at=datetime.now(timezone.utc).isoformat(),
    )
