import os

from fastapi import File

# File path to images to remove
delete_file = None
while delete_file is None:
    delete_file = input("Path to file containing paths of images to move: ")

    if not os.path.exists(delete_file) or not os.path.isfile(delete_file):
        print("Please enter valid path to file")
        delete_file = None

# Target directory path
target_dir = None
while target_dir is None:
    target_dir = input("Path to directory to move files into: ")

    if not os.path.exists(target_dir) or not os.path.isdir(target_dir):
        print("Please enter valid path to directory")
        target_dir = None

# Read file
image_paths = []
with open(delete_file, "r") as f:
    image_paths = [l.strip() for l in f.readlines()]

# Ask to confirm
print("\nSamples:")
if len(image_paths) > 15:
    print("\n".join(image_paths[:15]))
else:
    print("\n".join(image_paths))

print("\n")
choice = input("WARNING: Do you really want to move " +
               str(len(image_paths)) + " image(s)? (y/N) ")

if choice != "y":
    exit(0)

# Delete images
print("\n\n")
fails = []
for l in image_paths:
    try:
        full_target = os.path.join(target_dir, l.split(os.sep)[-1])
        os.rename(l, full_target)
    except Exception as ex:
        if ex.winerror == 183:  # File with same name already in target directory, so add counter to name
            counter = 1
            first_part = ".".join(full_target.split(".")[:-1])
            extension = full_target.split(".")[-1]
            new_target = first_part + "_" + str(counter) + "." + extension
            while os.path.exists(new_target):
                counter += 1
                new_target = first_part + "_" + str(counter) + "." + extension

            os.rename(l, new_target)
        else:
            print("Something went wrong.", ex,
                  "Could not move", l, "to", full_target)
            fails.append(l)

print("\n\nDone.")
print("Successfully moved", len(image_paths) -
      len(fails), "images to", target_dir)

if len(fails) > 0:
    print("\nFailed to move", len(fails))
    print("\n".join(fails))
