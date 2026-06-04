import cadquery as cq

battery_diameter = 18.4
battery_height = 65.3
shell_radius = (battery_diameter + 2.8) / 2
shell_z = battery_height + 8.0
shell_thickness = 0.8
filament_hole_diameter = 3
EPS = 0.01

candle = (
    cq.Workplane("XY")
    .circle(shell_radius)
    .extrude(shell_z)
    .faces(">Z")
    .shell(-shell_thickness)
)

candle = candle.cut(
    cq.Workplane("XY")
    .circle(filament_hole_diameter / 2)
    .extrude(shell_thickness + EPS)
)

cq.exporters.export(candle, "shell.stl")
