from concurrent.futures.process import _ExceptionWithTraceback
import os
from typing import Set
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from images import ImageGroup

# CONFIG
IMAGE_MOUNT_PATH = """O:\onedrive"""
DELETE_LOG_PATH = "deleted_images.txt"


app = FastAPI()

app.mount("/images", StaticFiles(directory=IMAGE_MOUNT_PATH), name="images")
templates = Jinja2Templates(directory="templates")


image_groups: list[ImageGroup] = []
deleted_images: Set[str] = set()


class SetupBody (BaseModel):
    config: str


class CompareBody (BaseModel):
    path: str
    delete: bool


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

        # Generate
        global image_groups
        image_groups = [ImageGroup(group_lines)
                        for group_lines in results.split("\n\n")[1:]]
        # Filter empty groups
        image_groups = [
            group for group in image_groups if len(group.images) > 0]

        # Load last state from delete_images file
        global deleted_images
        if os.path.exists(DELETE_LOG_PATH):
            try:
                with open(DELETE_LOG_PATH, "r") as f:
                    deleted_images = deleted_images.union(
                        set(l.strip() for l in f.readlines()))
            except Exception as ex:
                print("Could not load previous delete file.", ex)

        # Apply last state and create proper url
        for group in image_groups:
            for image in group.images:
                image.url = image.path[len(IMAGE_MOUNT_PATH):]
                image.deleted = image.path in deleted_images

        # Sort by path
        image_groups = sorted(image_groups, key=lambda g: g.images[0].path)
    except Exception as ex:
        print(ex)
        return "Something went wrong. " + str(ex)


@ app.post("/compare")
async def compare_post(body: CompareBody):
    if body.delete:
        deleted_images.add(body.path)
    else:
        deleted_images.remove(body.path)

    # Update file
    with open(DELETE_LOG_PATH, "w") as f:
        f.write("\n".join(deleted_images))
