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
clearance = 0.1

base = (
    cq.Workplane("XY")
    .box(base_width, base_height, base_thickness)
    .edges("|Z")
    .fillet(3)
)

base = (
    base
    .faces("<Z")
    .workplane()
    .circle(pin_radius)
    .extrude(pin_length)
    .faces("<Z")
    .fillet(tip_radius)
)

base = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-arm_spacing / 2, 0),
        (arm_spacing / 2, 0)
    ])
    .circle(arm_radius + clearance)
    .cutBlind(-(base_thickness - 1.0))
)

arm = (
    cq.Workplane("XY")
    .circle(arm_radius)
    .extrude(arm_length + base_thickness - 1.0)
    .faces(">Z")
    .fillet(tip_radius)
)

cq.exporters.export(base, "base.stl")
cq.exporters.export(arm, "arm.stl")
