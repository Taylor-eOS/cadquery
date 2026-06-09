import cadquery as cq

stick_width = 10.0
stick_depth = 35.0
left_height = 40.0
horizontal_length = 40.0
right_drop = 10.0

profile = [
    (0, 0),
    (0, left_height),
    (stick_width, left_height),
    (stick_width, stick_width),
    (horizontal_length, stick_width),
    (horizontal_length, -right_drop),
    (horizontal_length - stick_width, -right_drop),
    (horizontal_length - stick_width, 0),
]

result = (
    cq.Workplane("XZ")
    .polyline(profile)
    .close()
    .extrude(stick_depth)
)

cq.exporters.export(result, "holder.stl")
