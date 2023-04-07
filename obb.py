import numpy as np
from math import radians
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def rec2points(x: float, y: float, width: float, height: float, angle_deg: float):
    center = np.array([[x], [y]])
    angle = radians(angle_deg)

    R_lt = np.array([[np.cos(angle), -np.sin(angle)], [-np.sin(angle), -np.cos(angle)]])
    A = np.dot(R_lt, np.array([[width / 2], [height / 2]])) + center

    R_rt = np.array([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]])
    B = np.dot(R_rt, np.array([[width / 2], [height / 2]])) + center

    R_rb = np.array([[-np.cos(angle), np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    C = np.dot(R_rb, np.array([[width / 2], [height / 2]])) + center

    R_lb = np.array([[-np.cos(angle), -np.sin(angle)], [np.sin(angle), -np.cos(angle)]])
    D = np.dot(R_lb, np.array([[width / 2], [height / 2]])) + center

    corners = [A, B, C, D]

    for i in range(len(corners)):
        corn = corners[i]
        corners[i] = (corn[0], corn[1])

    return Polygon(corners)


def OBB(rec: Polygon, point: Point):
    return rec.contains(point)
