from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from images import ImageGroup

# CONFIG
IMAGE_MOUNT_PATH = """O:\onedrive"""


app = FastAPI()

app.mount("/images", StaticFiles(directory=IMAGE_MOUNT_PATH), name="images")
templates = Jinja2Templates(directory="templates")


image_groups: list[ImageGroup] = []


class SetupBody (BaseModel):
    config: str


@app.get("/")
async def index(request: Request):
    if image_groups is not None and len(image_groups) > 0:
        return templates.TemplateResponse("compare.html", {"groups": image_groups, "request": request})
    else:
        return templates.TemplateResponse("setup.html", context={"request": request})


@app.post("/setup")
async def setup_post(body: SetupBody):
    try:
        # Parse results
        results: str = body.config
        if results is None or len(results) <= 0:
            return "No config given."

        global image_groups
        image_groups = [ImageGroup(group_lines)
                        for group_lines in results.split("\n\n")[1:]]

        for group in image_groups:
            for image in group.images:
                image.url = image.path[len(IMAGE_MOUNT_PATH):]
    except Exception as ex:
        return "Something went wrong. " + str(ex)


@app.delete("/compare", response_class=HTMLResponse)
async def compare_post(request: Request):
    data = await request.form()
    src = data["src"].split("/")[-1]
    return "Not implemented yet :c"
