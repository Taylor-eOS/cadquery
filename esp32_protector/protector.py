import cadquery as cq

m = 0.1
pcb_x = 23.0 + (2 * m)
pcb_y = 18.0 + (2 * m)
bottom_z = 5.3
top_z = 2.7
tot_plate_z = bottom_z + top_z
wall_thickness = 1.0
case_x = pcb_x + (2 * wall_thickness)
case_y = pcb_y + (2 * wall_thickness)
side_wall_x = (pcb_x / 2) + (wall_thickness / 2)
front_y = (pcb_y / 2) + (wall_thickness / 2)
back_y = -(pcb_y / 2) - (wall_thickness / 2)
gap_width = 8.0
c = (True, True, False)
pin_hole_x = 20.0 + (2 * m)
pin_hole_y = 2.4 + (2 * m)
pin_hole_x_offset = -0.7
pin_y_offset = (pcb_y / 2) - (pin_hole_y / 2)
usb_z = 3.0 + (2 * m)
usb_y = 8.8 + (2 * m)
usb_r = (usb_z / 2) - m
usb_x = tot_plate_z + 0.7
rib_x = 10.0
rib_y = 0.2
rib_z = top_z
rib_inner_front_y = (pcb_y / 2) - (rib_y / 2)
rib_inner_back_y = -(pcb_y / 2) + (rib_y / 2)

def make_short_wall(tx):
    return (
        cq.Workplane("XY")
        .box(wall_thickness, case_y, top_z, centered=c)
        .translate((tx, 0, tot_plate_z))
    )

def make_long_wall(ty):
    return (
        cq.Workplane("XY")
        .box(pcb_x, wall_thickness, top_z, centered=c)
        .translate((0, ty, tot_plate_z))
    )

def make_gap(ty):
    return (
        cq.Workplane("XY")
        .box(gap_width, wall_thickness * 3, top_z * 2, centered=c)
        .translate((0, ty, bottom_z))
    )

def make_crush_rib(ty):
    return (
        cq.Workplane("XY")
        .box(rib_x, rib_y, rib_z, centered=c)
        .translate((0, ty, tot_plate_z))
    )

def make_usb_hole():
    return (
        cq.Workplane("YZ")
        .rect(usb_y, usb_z)
        .extrude(wall_thickness * 3, both=True)
        .edges("|X")
        .fillet(usb_r)
        .translate((-side_wall_x, 0, usb_x + (usb_z / 2)))
    )

def make_pin_holes():
    full_height = bottom_z + top_z + m
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

bottom_plate = cq.Workplane("XY").box(case_x, case_y, bottom_z, centered=c)
top_plate = cq.Workplane("XY").box(case_x, case_y, top_z, centered=c).translate((0, 0, bottom_z))
left_wall = make_short_wall(-side_wall_x)
right_wall = make_short_wall(side_wall_x)
front_wall = make_long_wall(front_y)
back_wall = make_long_wall(back_y)
front_gap = make_gap(front_y)
back_gap = make_gap(back_y)
front_rib = make_crush_rib(rib_inner_front_y)
back_rib = make_crush_rib(rib_inner_back_y)
usb_yole = make_usb_hole()
pin_hole_tool = make_pin_holes()

case = (
    bottom_plate
    .union(top_plate)
    .union(left_wall)
    .union(right_wall)
    .union(front_wall)
    .union(back_wall)
    .union(front_rib)
    .union(back_rib)
    .cut(usb_yole)
    .cut(pin_hole_tool)
)

cq.exporters.export(case, "protector.stl")
