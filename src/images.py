class ImageGroup:
    def __init__(self, group_lines) -> None:
        self.images: list["Image"] = []
        self.parse(group_lines)

    def parse(self, lines: str) -> None:
        for line in lines.split("\n")[1:]:
            self.images.append(Image(line))


class Image:
    def __init__(self, raw_line: str) -> None:
        self.parse(raw_line)

    def parse(self, line: str) -> None:
        parts = line.split(" - ")

        if len(parts) < 4:
            return

        self.path = parts[0]
        self.url = None
        self.dimensions = parts[1]
        self.size = parts[2]
        self.similarity = parts[3]
