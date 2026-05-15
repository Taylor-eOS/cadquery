import cadquery as cq

m = 0.1
pcb_x = 23.0 + (2 * m)
pcb_y = 18.0 + (2 * m)
plate_z = 8.0
wall_thickness = 1.0
case_x = pcb_x + (2 * wall_thickness)
case_y = pcb_y + (2 * wall_thickness)
side_wall_x = (pcb_x / 2) + (wall_thickness / 2)
front_y = (pcb_y / 2) + (wall_thickness / 2)
back_y = -(pcb_y / 2) - (wall_thickness / 2)
c = (True, True, False)
pin_hole_x = 20.0 + (2 * m)
pin_hole_y = 2.4 + (2 * m)
pin_hole_x_offset = -0.7
pin_y_offset = (pcb_y / 2) - (pin_hole_y / 2)
usb_z = 3.0 + (2 * m)
usb_y = 8.8 + (2 * m)
usb_r = (usb_z / 2) - m
usb_x = plate_z + 0.7
rib_x = 10.0
rib_y = 0.2
rib_z = 2.7
rib_inner_front_y = (pcb_y / 2) - (rib_y / 2)
rib_inner_back_y = -(pcb_y / 2) + (rib_y / 2)

def make_short_wall(tx):
    return (
        cq.Workplane("XY")
        .box(wall_thickness, case_y, rib_z, centered=c)
        .translate((tx, 0, plate_z))
    )

def make_long_wall(ty):
    return (
        cq.Workplane("XY")
        .box(pcb_x, wall_thickness, rib_z, centered=c)
        .translate((0, ty, plate_z))
    )

def make_pin_holes():
    full_height = plate_z + rib_z + m
    return (
        cq.Workplane("XY")
        .box(pin_hole_x, pin_hole_y, full_height, centered=c)
        .translate((pin_hole_x_offset, pin_y_offset, 0))
        .union(
            cq.Workplane("XY")
            .box(pin_hole_x, pin_hole_y, full_height, centered=c)
            .translate((pin_hole_x_offset, -pin_y_offset, 0))
        )
    )

def make_usb():
    return (
        cq.Workplane("YZ")
        .rect(usb_y, usb_z)
        .extrude(wall_thickness * 3, both=True)
        .edges("|X")
        .fillet(usb_r)
        .translate((-side_wall_x, 0, usb_x + (usb_z / 2)))
    )

def make_supported_rib(ty, wall_y, direction):
    pts = [
        (wall_y, plate_z + rib_z),
        (ty + (rib_y / 2) * direction, plate_z + rib_z),
        (ty + (rib_y / 2) * direction, plate_z),
        (wall_y, plate_z - rib_z),
        (wall_y, plate_z)
    ]
    return (
        cq.Workplane("YZ")
        .polyline(pts)
        .close()
        .extrude(rib_x / 2, both=True)
    )

base_plate = cq.Workplane("XY").box(case_x, case_y, plate_z, centered=c)
left_wall = make_short_wall(-side_wall_x)
right_wall = make_short_wall(side_wall_x)
front_wall = make_long_wall(front_y)
back_wall = make_long_wall(back_y)
front_rib_assembly = make_supported_rib(rib_inner_front_y, front_y - (wall_thickness / 2), -1.0)
back_rib_assembly = make_supported_rib(rib_inner_back_y, back_y + (wall_thickness / 2), 1.0)
usb_hole = make_usb()
pin_hole_tool = make_pin_holes()

case = (
    base_plate
    .union(left_wall)
    .union(right_wall)
    .union(front_wall)
    .union(back_wall)
    .cut(pin_hole_tool)
    .union(front_rib_assembly)
    .union(back_rib_assembly)
    .cut(usb_hole)
)

cq.exporters.export(case, "protector.stl")
