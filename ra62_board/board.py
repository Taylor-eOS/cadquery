import cadquery as cq
import math

board_x = 21.5
board_y = 19.5
board_z = 2.5
hole_size = 0.8
clearance = 0.1
EPS = 0.01
col_separation = 2.0
row_separation = 16.0
hole_number = 8
first_layer = 0.2 + EPS
square = hole_size + clearance
circle_diameter = square * math.sqrt(2)
fillet_radius = 1.0
wall_inner_y = 17.0
wall_height = 1.0
wall_thickness = ((board_y - wall_inner_y) / 2) - clearance
wall_length = row_separation

board = (
    cq.Workplane("XY")
    .box(board_x, board_y, board_z)
    .edges("|Z")
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .rarray(row_separation, col_separation, 2, hole_number)
    .circle(circle_diameter / 2)
    .cutBlind(-(board_z - first_layer))
)
wall_center_y = (board_y / 2) - (wall_thickness / 2)
board = (
    board.faces(">Z")
    .workplane()
    .pushPoints([(0, wall_center_y), (0, -wall_center_y)])
    .box(wall_length, wall_thickness, wall_height, combine=True)
)
cq.exporters.export(board, "board.stl")
