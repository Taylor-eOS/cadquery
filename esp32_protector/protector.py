import cadquery as cq

pcb_x = 23.0
pcb_y = 18.0
wall_thickness = 1.0
base_thickness = 1.0
wall_height = 2.7
margin = 0.1
inside_x = pcb_x + margin * 2
inside_y = pcb_y + margin * 2
case_x = inside_x + wall_thickness * 2
case_y = inside_y + wall_thickness * 2

base = (
    cq.Workplane("XY")
    .box(
        case_x,
        case_y,
        base_thickness,
        centered=(True, True, False)
    )
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
