import cadquery as cq

width = 52.0
depth = 34.0
height = 12.0
wall = 0.8
hole_width = 47.0
hole_depth = 30.0

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
    .center(0, 0)
    .workplane(offset=-(3.0 + wall))
    .rect(width - 2 * wall, depth - 2 * wall)
    .rect(hole_width, hole_depth)
    .extrude(wall)
)

cq.exporters.export(box, "solar.stl")
