import cadquery as cq

base_x = 46.0
base_y = 9.0
base_z = 3.8
pin_radius = 2.3 #For 5mm shelf
pin_length = 12.0 + base_z
tip_radius = 1.0
clearance = 0.5
hole_radius = pin_radius + clearance
arm_spacing = base_x - (hole_radius * 2) - ((base_y - hole_radius) / 2)

base = (
    cq.Workplane("XY")
    .box(base_x, base_y, base_z)
    .edges("|Z")
    .fillet(3)
)

base = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-arm_spacing / 2, 0),
        (arm_spacing / 2, 0)
    ])
    .circle(hole_radius)
    .cutThruAll()
)

base = (
    base
    .faces(">Z")
    .workplane()
    .circle(hole_radius)
    .cutThruAll()
)

pin = (
    cq.Workplane("XY")
    .circle(pin_radius)
    .extrude(pin_length + base_z)
    .faces(">Z")
    .fillet(tip_radius)
)

cq.exporters.export(base, "base.stl")
cq.exporters.export(pin, "pin.stl")
