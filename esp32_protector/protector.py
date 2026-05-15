import cadquery as cq

pcb_x = 23.0 + 0.1
pcb_y = 18.0 + 0.1
top_height = 2.7
bottom_z = 5.3
wall_thickness = 1.0
side_wall_x = (pcb_x / 2) - (wall_thickness / 2)
front_y = (pcb_y / 2) - (wall_thickness / 2)
back_y = -(pcb_y / 2) + (wall_thickness / 2)
gap_width = 6.0
full_wall_length = pcb_x - (2 * wall_thickness)
wall_z = bottom_z + top_height
c = (True, True, False)

def make_short_wall(tx):
    return (
        cq.Workplane("XY")
        .box(wall_thickness, pcb_y, top_height, centered=c)
        .translate((tx, 0, wall_z))
    )

def make_long_wall(ty):
    return (
        cq.Workplane("XY")
        .box(full_wall_length, wall_thickness, top_height, centered=c)
        .translate((0, ty, wall_z))
    )

def make_gap(ty):
    return (
        cq.Workplane("XY")
        .box(gap_width, wall_thickness, top_height * 2, centered=c)
        .translate((0, ty, bottom_z))
    )

bottom_plate = (
    cq.Workplane("XY")
    .box(pcb_x, pcb_y, bottom_z, centered=c)
)

top_plate = (
    cq.Workplane("XY")
    .box(pcb_x, pcb_y, top_height, centered=c)
    .translate((0, 0, bottom_z))
)

left_wall = make_short_wall(-side_wall_x)
right_wall = make_short_wall(side_wall_x)
front_wall = make_long_wall(front_y)
back_wall = make_long_wall(back_y)
front_gap = make_gap(front_y)
back_gap = make_gap(back_y)

case = (
    bottom_plate
    .union(top_plate)
    .union(left_wall)
    .union(right_wall)
    .union(front_wall)
    .union(back_wall)
    .cut(front_gap)
    .cut(back_gap)
)

cq.exporters.export(case, "protector.stl")
