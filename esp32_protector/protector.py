import cadquery as cq

pcb_x = 23.0
pcb_y = 18.0
wall_thickness = 1.0
base_thickness = 1.0
wall_height = 2.7
clearance = 1.0
inside_x = pcb_x + (clearance * 2)
inside_y = pcb_y + (clearance * 2)
case_x = inside_x + (wall_thickness * 2)
case_y = inside_y + (wall_thickness * 2)
slot_width = 2.4 + 0.1
slot_length = 20.0 + 0.1
pin_y_center_dist = 15.0 / 2
pin_x_offset = -0.6

base = (
    cq.Workplane("XY")
    .box(case_x, case_y, base_thickness, centered=(True, True, False))
)

base = (
    base.faces(">Z")
    .workplane()
    .pushPoints([(pin_x_offset, -pin_y_center_dist), (pin_x_offset, pin_y_center_dist)])
    .rect(slot_length, slot_width)
    .cutThruAll()
)

walls = (
    base
    .faces(">Z")
    .workplane()
    .rect(case_x, case_y)
    .rect(inside_x, inside_y)
    .extrude(wall_height)
)

case = base.union(walls)

cq.exporters.export(case, "protector.stl")
