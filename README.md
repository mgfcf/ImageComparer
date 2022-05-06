# ImageComparer

Make sure to set the proper image mount path in `app.py`!

To run, install dependencies or activate environment, go to the src directory and execute: `python -m uvicorn app:app --reload`

## src/run_remove.py

Run this file and enter the path to the file, containing the list of all images that shall be removed. It moves all files to a given target directory, that can then be easily deleted.
