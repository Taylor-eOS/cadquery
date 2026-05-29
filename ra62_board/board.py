import cadquery as cq
import math

board_x = 21.5
board_y = 19.5
board_z = 2.8
hole_size = 0.8
clearance = 0.1
col_separation = 2.0
row_separation = 16.0
holes = 8
first_layer = 0.2 + 0.01
square = hole_size + clearance
circle_diameter = square * math.sqrt(2)
fillet_radius = 1.0
guardrail_inner_y = 17.0
guardrail_height = 1.0
guardrail_thickness = (board_y - guardrail_inner_y) / 2
guardrail_length = row_separation
guardrail_center_y = (board_y / 2) - (guardrail_thickness / 2)

board = (
    cq.Workplane("XY")
    .box(board_x, board_y, board_z)
    .edges("|Z")
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .rarray(row_separation, col_separation, 2, holes)
    .circle(circle_diameter / 2)
    .cutBlind(-(board_z - first_layer))
)

board = (
    board.faces(">Z")
    .workplane()
    .pushPoints([(0, guardrail_center_y), (0, -guardrail_center_y)])
    .box(guardrail_length, guardrail_thickness, guardrail_height, combine=True)
)

cq.exporters.export(board, "board.stl")
