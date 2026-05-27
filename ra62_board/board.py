import cadquery as cq

board_x = 20.0
board_y = 20.0
board_z = 2.0
hole_size = 0.8
col_separation = 2.0
row_separation = 16.0
cols = 8
clearance = 0.1

board = (
    cq.Workplane("XY")
    .box(board_x, board_y, board_z)
    .faces(">Z")
    .workplane()
    .rarray(row_separation, col_separation, 2, cols)
    .rect(hole_size + clearance, hole_size + clearance)
    .cutThruAll()
)

cq.exporters.export(board, "board.stl")
