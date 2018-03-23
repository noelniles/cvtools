class PointList:
    def __init__(self):
        self._points = []

    def append(self, point):
        if point not in self._points:
            self._points.append(point)