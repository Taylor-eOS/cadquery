import cadquery as cq

PCB_CLEARANCE = 0.2
pcb_x = 23.0 + (2 * PCB_CLEARANCE)
pcb_y = 18.0 + (2 * PCB_CLEARANCE)
plate_z = 8.0
wall_z = 2.8
wall_thickness = 1.0
case_x = pcb_x + (wall_thickness * 2)
case_y = pcb_y + (wall_thickness * 2)
side_wall_x = (pcb_x / 2) + (wall_thickness / 2)
front_y = (pcb_y / 2) + (wall_thickness / 2)
back_y = -(pcb_y / 2) - (wall_thickness / 2)
EPS = 0.01
c = (True, True, False)
PIN_CLEARANCE = 0.3
pin_hole_y = 2.6 + (2 * PIN_CLEARANCE)
pin_dist_left = 0.6
pin_dist_right = 1.2
pin_hole_x = pcb_x - pin_dist_left - pin_dist_right
pin_hole_x_offset = (pin_dist_left - pin_dist_right) / 2
pin_y_offset = (pcb_y / 2) - (pin_hole_y / 2)
USB_CLEARANCE = 0.2
usb_z = 3.0 + (2 * USB_CLEARANCE)
usb_y = 8.8 + (2 * USB_CLEARANCE)
usb_rad = (usb_z / 2) - 0.2 - EPS
usb_x = plate_z + 0.7
rib_x = 10.0
rib_y = PCB_CLEARANCE
rib_z = wall_z
rib_front_y = (pcb_y / 2) - rib_y
rib_back_y = -(pcb_y / 2) + rib_y

def make_short_wall(tx):
    return (
        cq.Workplane("XY")
        .box(wall_thickness, case_y, wall_z, centered=c)
        .translate((tx, 0, plate_z))
    )

def make_long_wall(y_center):
    return (
        cq.Workplane("XY")
        .box(pcb_x, wall_thickness, wall_z, centered=c)
        .translate((0, y_center, plate_z))
    )

def make_pin_hole(y_offset):
    tool_height = plate_z + (2 * EPS)
    return (
        cq.Workplane("XY")
        .box(pin_hole_x, pin_hole_y, tool_height, centered=c)
        .translate((pin_hole_x_offset, y_offset, plate_z - tool_height + EPS))
    )

def make_usb_hole():
    return (
        cq.Workplane("YZ")
        .rect(usb_y, usb_z)
        .extrude(wall_thickness * 3, both=True)
        .edges("|X")
        .fillet(usb_rad)
        .translate((-side_wall_x, 0, usb_x + (usb_z / 2)))
    )

def make_supported_rib(rib_center_y, wall_y, direction):
    pts = [
        (wall_y, plate_z + rib_z),
        (rib_center_y + rib_y * direction, plate_z),
        (wall_y, plate_z - rib_z),
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
front_rib = make_supported_rib(rib_front_y, front_y - (wall_thickness / 2), -1)
back_rib = make_supported_rib(rib_back_y, back_y + (wall_thickness / 2), 1)
usb_hole = make_usb_hole()
pin_hole_front = make_pin_hole(pin_y_offset)
pin_hole_back = make_pin_hole(-pin_y_offset)

bottom_panel = (
    base_plate
    .cut(pin_hole_front)
    .cut(pin_hole_back)
)

usb_wall = (
    left_wall
    .cut(usb_hole)
)

long_walls = (
    front_wall
    .union(back_wall)
    .union(front_rib)
    .union(back_rib)
)

walls = (
    long_walls
    .union(usb_wall)
    .union(right_wall)
)

case = (
    bottom_panel
    .union(walls)
)

cq.exporters.export(case, "protector.stl")
