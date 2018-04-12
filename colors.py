MAP_COLORS = [
    [117, 150, 46, 1],
    [141, 178, 63, 1],
    [204, 214, 94, 1],
    [236, 206, 134, 1],
    [248, 231, 192, 1]
]
MAP_COLORS[:] = [[ele / 255 for ele in sub] for sub in MAP_COLORS]
