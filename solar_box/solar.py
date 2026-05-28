import cadquery as cq

width = 52.0
depth = 34.0
height = 16.0
wall = 0.8
ledge_drop = 3.1
ledge_length = 2.4
z = (height / 2) - ledge_drop

box = (
    cq.Workplane("XY")
    .box(width, depth, height)
    .faces(">Z")
    .shell(-wall)
)

left_support = (
    cq.Workplane("XZ")
    .polyline([
        (-width / 2 + wall, z),
        (-width / 2 + wall + ledge_length, z),
        (-width / 2 + wall, z - ledge_length),
    ])
    .close()
    .extrude(depth - 2 * wall)
    .translate((0, depth / 2 - wall, 0))
)

right_support = (
    cq.Workplane("XZ")
    .polyline([
        (width / 2 - wall, z),
        (width / 2 - wall - ledge_length, z),
        (width / 2 - wall, z - ledge_length),
    ])
    .close()
    .extrude(depth - 2 * wall)
    .translate((0, depth / 2 - wall, 0))
)

box = box.union(left_support).union(right_support)

box = (
    box
    .faces(">Y")
    .workplane(centerOption="CenterOfMass")
    .circle(4.7 / 2)
    .cutBlind(-wall)
)

box = (
    box
    .faces("<Y")
    .workplane(centerOption="CenterOfMass")
    .rect(8.6, 4.0)
    .cutBlind(-wall)
)

cq.exporters.export(box, "solar.stl")
