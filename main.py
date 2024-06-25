from PIL import Image, ImageDraw

# Open the image file
img = Image.open("im04.png").convert("L")  # Convert to grayscale

# Initialize a list to hold the coordinates of pixels with values more than 0
pixels_more_than_zero = []

# Iterate over each pixel
for x in range(img.width):
    for y in range(img.height):
        # Get the pixel value
        pixel_value = img.getpixel((x, y))
        # Check if the pixel's value is more than 0
        if pixel_value > 0:
            # Add the pixel's coordinates to the list
            pixels_more_than_zero.append((x, y))

# Separate the list into left and right side
left_side = []
right_side = []
midline = 230
for i, (x, y) in enumerate(pixels_more_than_zero):
    if x < midline:
        left_side.append((x, y))
    else:
        right_side.append((x, y))

# print(f"Left Side: {left_side}")
# print(f"Right Side: {right_side}")

left_side = sorted(left_side, key=lambda x: x[1])
right_side = sorted(right_side, key=lambda x: x[1])

# Calculate slope for each side
left_side_slope = []
top_bottom_padding = 10
high_slope = 1000
for i in range(len(left_side) - 1):
    x, y = left_side[i]
    if i <top_bottom_padding or i > len(left_side) - top_bottom_padding:
        slope = high_slope
    else:
        x1, y1 = left_side[i - 5]
        x2, y2 = left_side[i + 5]

        try:
            # Calculate the slope
            slope = (y2 - y1) / (x2 - x1)
            if abs(slope) > 6:
                slope = high_slope
        except ZeroDivisionError:
            # Handle division by zero
            slope = high_slope
    left_side_slope.append((x, y, slope))

right_side_slope = []
for i in range(len(right_side) - 1):
    x, y = right_side[i]
    if i <top_bottom_padding or i > len(right_side) - top_bottom_padding:
        slope = high_slope
    else:
        x1, y1 = right_side[i - 5]
        x2, y2 = right_side[i + 1 + 5]

        try:
            # Calculate the slope
            slope = (y2 - y1) / (x2 - x1)
            if abs(slope) > 6:
                slope = high_slope
        except ZeroDivisionError:
            # Handle division by zero
            slope = high_slope
    right_side_slope.append((x, y, slope))

# calculate the element wise distance between the two sides
distance = []
end_index_skip = 3
for i in range(len(left_side_slope) - end_index_skip):
    dist = abs(left_side_slope[i][0] - right_side[i][0])
    distance.append(dist)

# print(f"Distance: {distance}")

distance2 = []
# if one of the lines is vertical or they have
# equal slope with opposite sign, then the distance is calculated
# with just a horizontal distance
# Other wise search for the closest point
# on the other line and calculate the distance
search_range = 20
slope_similarity = 0.5
for i in range(int(search_range/2), len(left_side_slope) - int(search_range/2)):
    if left_side_slope[i][2] ==high_slope or right_side_slope[i][2] ==high_slope or \
    abs(left_side_slope[i][2] + right_side_slope[i][2]) < slope_similarity:
        dist = abs(left_side_slope[i + 1][0] - right_side_slope[i + 1][0])
        distance2.append((left_side_slope[i][0], left_side_slope[i][1],
                          right_side_slope[i][0], right_side_slope[i][1], dist))
    else:
        dist0 = 100000
        k0 = 0
        for j in range(search_range):
            dist = abs(left_side_slope[i][0] - right_side[int(i - search_range/2 + j)][0])
            k = int(i - search_range/2 + j)
            if dist > dist0:
                dist = dist0
                k = k0
            dist0 = dist
            k0 = k

        distance2.append((left_side_slope[i][0], left_side_slope[i][1],
                          right_side[k][0], right_side[k][1], dist))

# print(f"Distance: {distance2}")

draw = ImageDraw.Draw(img)

skipping_factor = 10 # to avoid drawing all the lines
for i in range(0, len(distance2), skipping_factor):
    x1, y1, x2, y2, _ = distance2[i]
    draw.line((x1, y1, x2, y2), fill=128, width=4)

img.show()
