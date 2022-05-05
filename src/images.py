class ImageGroup:
    def __init__(self, group_lines) -> None:
        self.images: list["Image"] = []
        self.parse(group_lines)

    def parse(self, lines: str) -> None:
        for line in lines.split("\n")[1:]:
            self.images.append(Image(line))

        if len(self.images) <= 0:
            return

        self.images = sorted(self.images, key=lambda i: i.path)

        # Get biggest shared prefix for all images
        self.path_prefix = ""
        path_parts = self.images[0].path.split("\\")
        for part in path_parts:
            new_prefix = self.path_prefix + part + "\\"
            if not all(image.path.startswith(new_prefix) for image in self.images):
                # Adjust unique prefix based on shared prefix
                for image in self.images:
                    image.unique_path = image.path[len(self.path_prefix):]
                break

            self.path_prefix = new_prefix


class Image:
    def __init__(self, raw_line: str) -> None:
        self.parse(raw_line)

    def parse(self, line: str) -> None:
        parts = line.split(" - ")

        if len(parts) < 4:
            return

        self.path = parts[0]
        self.unique_path = self.path
        self.url = None
        self.dimensions = parts[1]
        self.size = parts[2]
        self.similarity = parts[3]
        self.deleted = False
