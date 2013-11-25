import Image
import math
import random

from optparse import OptionParser

def average_file(input_file, output_file, chunk_size = -1):
    print "doing an average thing with input: " + input_file + " and output " + output_file

    input_image = Image.open(input_file)
    tmp_image = Image.new("RGB", input_image.size, "black")
    output_image = Image.new("RGB", input_image.size, "black")

    if chunk_size == -1:
        chunk_size = ((input_image.size[0] + input_image.size[1]) / 2) / 35

    print "input image size is " + str(input_image.size[0]) + "x" + str(input_image.size[1]) \
            + " and chunk size is " + str(chunk_size)

    all_colors = []

    for x_chunk in xrange(0, input_image.size[0] - chunk_size, chunk_size):
        for y_chunk in xrange(0, input_image.size[1] - chunk_size, chunk_size):
            avg_color = chunk_average(input_image, x_chunk, y_chunk, chunk_size)
            all_colors.append(avg_color)
            fill_chunk(tmp_image, x_chunk, y_chunk, chunk_size, avg_color)

    palette = make_palette(all_colors)

    palette_image = Image.new("RGB", (450, 50), "black")
    for i in xrange(len(palette)):
        fill_chunk(palette_image, i * 50, 0, 50, palette[i])

    palette_image.save("palette.png", "PNG")

    for x_chunk in xrange(0, input_image.size[0] - chunk_size, chunk_size):
        for y_chunk in xrange(0, input_image.size[1] - chunk_size, chunk_size):
            original_color = tmp_image.getpixel((x_chunk, y_chunk))
#            blurred_original_color = average_from_surrounding(tmp_image, x_chunk, y_chunk, chunk_size)
            color_from_palette = closest_color(original_color, palette)
            fill_chunk(output_image, x_chunk, y_chunk, chunk_size, color_from_palette)

    tmp_image.save("tmp.png", "PNG")
    output_image.save(output_file, "PNG")

def average_from_surrounding(scan, x, y, chunk_size):
    surrounding_points = [scan.getpixel((x, y - chunk_size)), scan.getpixel((x + chunk_size, y)), \
            scan.getpixel((x, y + chunk_size)), scan.getpixel((x - chunk_size, y)), \
            scan.getpixel((x - chunk_size, y - chunk_size)), scan.getpixel((x + chunk_size, y - chunk_size)), \
            scan.getpixel((x + chunk_size, y + chunk_size)), scan.getpixel((x - chunk_size, y + chunk_size)), \
            scan.getpixel((x, y)), scan.getpixel((x, y)), scan.getpixel((x, y))]

    r_total, g_total, b_total = 0, 0, 0
    for r, g, b in surrounding_points:
        r_total += r
        g_total += g
        b_total += b

    return (1, 1, 1)

def make_palette(all_colors):
    palette = []
    for i in xrange(9):
        palette.append(all_colors[random.randint(0, len(all_colors))])
    return palette

def closest_color(color, palette):
    diffs = []
    for other_color in palette:
        r, g, b = color
        o_r, o_g, o_b = other_color
        diffs.append(math.fabs(o_r - r) * math.fabs(o_g - g) * math.fabs(o_b - b))

    lowest = 0
    for i in xrange(1, len(palette)):
        if diffs[i] < diffs[lowest]:
            lowest = i

    return palette[lowest]

def fill_chunk(image, start_x, start_y, chunk_size, color):
    for x in xrange(start_x, start_x + chunk_size):
        for y in xrange(start_y, start_y + chunk_size):
            image.putpixel((x, y), color)

def chunk_average(image, start_x, start_y, chunk_size):
    r_sum, g_sum, b_sum = 0, 0, 0

    for x in xrange(start_x, start_x + chunk_size):
        for y in xrange(start_y, start_y + chunk_size):
            r_pix, g_pix, b_pix = image.getpixel((x, y))
            r_sum += r_pix
            g_sum += g_pix
            b_sum += b_pix

    pix_count = chunk_size * chunk_size

    r = r_sum / pix_count
    g = g_sum / pix_count
    b = b_sum / pix_count

    return (r, g, b)

def main():
    parser = OptionParser()
    parser.add_option("-i", "--input-file", dest="input_file")
    parser.add_option("-o", "--output-file", dest="output_file")
    parser.add_option("-a", action="store_true", dest="average")

    (options, args) = parser.parse_args()

    if options.average:
        if options.input_file:
            if options.output_file:
                average_file(options.input_file, options.output_file)
            else:
                average_file(options.input_file, "output.png")
        else:
            print "you need to specify an input file for the 'average' option"
    else:
        print "you need to specify an option"

if __name__ == "__main__":
	main()
