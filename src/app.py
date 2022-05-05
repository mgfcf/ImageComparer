from dataclasses import dataclass
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
import os
import ntpath

# CONFIG
IMAGE_MOUNT_PATH = """O:\OneDrive"""



app = FastAPI()

app.mount("/images", StaticFiles(directory=IMAGE_MOUNT_PATH), name="images")
templates = Jinja2Templates(directory="templates")


@app.get("/viewing", response_class=HTMLResponse)
async def viewing(request: Request):
    results = "Go"
    return templates.TemplateResponse("viewing.html", {"request": request, "results": results})


@app.delete("/viewing", response_class=HTMLResponse)
async def viewing_post(request: Request):
    data = await request.form()
    src = data["src"].split("/")[-1]
    delete_image(src)
    return ""


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def delete_image(l_path):
    os.rename(os.path.join(IMAGE_MOUNT_PATH, l_path),os.path.join("""W:\GoogleDrive\Pics\Anime\Deleted""", path_leaf(l_path)))

@app.post("/viewing", response_class=HTMLResponse)
async def viewing_post(request: Request, where: str = Form(...)):
    sql = where
    if (sql == ""):
        return viewing()
    print(sql)
    conn = sqlite3.connect(db_path, uri=True)
    cur = conn.cursor()

    cur.execute("SELECT FileName, Id FROM AllTaggedConcat WHERE " + sql)
    res = cur.fetchall()
    images = []
    cur.execute("SELECT count(*) FROM AllTaggedConcat WHERE " +
                sql.split("limit")[0])
    cnt = cur.fetchall()[0][0]

    dirs = [x for x in os.listdir(IMAGE_MOUNT_PATH) if not x.endswith(".ini")]
    refimages = []
    for i in dirs:
        subdir = os.path.join(IMAGE_MOUNT_PATH, i)
        refimages.extend([{"path": i, "file": img}
                          for img in os.listdir(subdir)])

    for i in res:
        image = {}
        possible = [os.path.join(img["path"], img["file"])
                    for img in refimages if img["file"] == i[0]]
        if (len(possible) > 0):
            image["file"] = possible[0]
            image["id"] = i[1]
            images.append(image)
        else:
            pass
    results = "Results " + str(cnt)
    print(results)
    return templates.TemplateResponse("viewing.html", {"request": request, "images": images, "searchterm": sql, "results": results})