"""A queue that holds points"""
from Queue import Queue


class PointQueue(Queue):
    def __init__(self):
        Queue.__init__(self)

    def 