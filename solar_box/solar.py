import cadquery as cq

width = 52.0
depth = 34.0
height = 12.0
wall = 0.8
ledge_height = 3.0
ledge_width = 47.0
ledge_depth = 30.0

box = (
    cq.Workplane("XY")
    .box(width, depth, height)
    .faces(">Z")
    .shell(-wall)
)

box = (
    box
    .faces(">Z")
    .workplane()
    .workplane(offset=-((height / 2) - ledge_height))
    .rect(width - 2 * wall, depth - 2 * wall)
    .rect(ledge_width, ledge_depth)
    .extrude(wall)
)

cq.exporters.export(box, "solar.stl")
