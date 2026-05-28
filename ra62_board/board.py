import cadquery as cq
import math

board_x = 21.5
board_y = 19.5
board_z = 2.5
hole_size = 0.8
clearance = 0.0
col_separation = 2.0
row_separation = 16.0
holes = 8
first_layer = 0.2 + 0.01
square = hole_size + clearance
circle_diameter = square * math.sqrt(2)

board = (
    cq.Workplane("XY")
    .box(board_x, board_y, board_z)
    .faces(">Z")
    .workplane()
    .rarray(row_separation, col_separation, 2, holes)
    .circle(circle_diameter / 2)
    .cutBlind(-(board_z - first_layer))
)

cq.exporters.export(board, "board.stl")
