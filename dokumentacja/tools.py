import webcolors


def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name


requested_colour = (255, 0, 23)
actual_name, closest_name = get_colour_name(requested_colour)

print("Actual colour name:", actual_name, ", closest colour name:", closest_name)

# second method for approx_color
# closest_color_2 = "black"
#     points = [[p1[0], p1[1]], [p2[0], p1[1]], [p2[0], p2[1]], [p1[0], p2[1]]]
#
#     mask = np.zeros(img.shape[:2], dtype=np.uint8)
#     cv2.fillConvexPoly(mask, np.array(points, dtype=np.int32), 1)
#     roi = cv2.bitwise_and(img, img, mask=mask)
#     mean_color = cv2.mean(roi, mask=mask)
#     mean_color_rgb = tuple(reversed(mean_color[:3]))
#     r2 = mean_color_rgb[0]
#     g2 = mean_color_rgb[1]
#     b2 = mean_color_rgb[2]
#
#     min_distance2 = float("inf")
#     for color, value in colors.items():
#         dist = sum([(i - j) ** 2 for i, j in zip((r2, g2, b2), value)])
#         if dist < min_distance2:
#             min_distance2 = dist
#             closest_color_2 = color
