from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Create a router for login-related pages
router = APIRouter()

# Tell FastAPI where HTML templates are located
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )