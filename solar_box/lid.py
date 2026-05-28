import cadquery as cq
from solar import width, depth, wall

knob_radius = 1.8
knob_height = 2.5
clearance = 0.05
thickness = 1.0
calc = lambda dim, wall, clearance: dim - 2 * wall - clearance
lid_width = calc(width, wall, clearance)
lid_depth = calc(depth, wall, clearance)

lid = (
    cq.Workplane("XY")
    .box(lid_width, lid_depth, thickness)
    .faces(">Z")
    .workplane()
    .circle(knob_radius)
    .extrude(knob_height)
)

cq.exporters.export(lid, "lid.stl")
