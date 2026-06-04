import cadquery as cq

battery_diameter = 18.4
extra_diameter = 2.7
shell_radius = (battery_diameter + extra_diameter) / 2
battery_height = 65.3
extra_length = 23.7
shell_thickness = 0.8
filament_hole_diameter = 3
EPS = 0.01

candle = (
    cq.Workplane("XY")
    .circle(shell_radius)
    .extrude(battery_height + extra_length)
    .faces(">Z")
    .shell(-shell_thickness)
)

candle = candle.cut(
    cq.Workplane("XY")
    .circle(filament_hole_diameter / 2)
    .extrude(shell_thickness + EPS)
)

cq.exporters.export(candle, "shell.stl")
