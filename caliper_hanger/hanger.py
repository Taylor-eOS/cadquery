import cadquery as cq

base_width = 54.0
base_height = 9.0
base_thickness = 4.0
pin_radius = 4.0
pin_length = 11.0
arm_spacing = 45.0
arm_radius = 3.0
arm_length = 20.0
tip_radius = 1.0

hanger = (
    cq.Workplane("XY")
    .box(base_width, base_height, base_thickness)
    .edges("|Z")
    .fillet(3)
)

hanger = (
    hanger
    .faces("<Z")
    .workplane()
    .circle(pin_radius)
    .extrude(pin_length)
    .faces("<Z")
    .fillet(tip_radius)
)

hanger = (
    hanger
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-arm_spacing / 2, 0),
        (arm_spacing / 2, 0)
    ])
    .circle(arm_radius)
    .extrude(arm_length)
    .faces(">Z")
    .fillet(tip_radius)
)

cq.exporters.export(hanger, "hanger.stl")
