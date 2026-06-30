from dataclasses import dataclass


@dataclass
class BoundingBox:
    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    @property
    def center(self):
        return (
            (self.x1 + self.x2) // 2,
            (self.y1 + self.y2) // 2,
        )

    @property
    def area(self):
        return self.width * self.height