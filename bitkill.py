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
            break_down_block(input_image, tmp_image, x_chunk, y_chunk, chunk_size, all_colors)

    palette = make_palette(all_colors)

    palette_image = Image.new("RGB", (450, 50), "black")
    for i in xrange(len(palette)):
        fill_chunk(palette_image, i * 50, 0, 50, palette[i])

    palette_image.save("palette.png", "PNG")

    for x in xrange(0, input_image.size[0] - chunk_size, chunk_size / 2):
        for y in xrange(0, input_image.size[1] - chunk_size, chunk_size / 2):
            original_color = tmp_image.getpixel((x, y))
            color_from_palette = closest_color(original_color, palette)
            fill_chunk(output_image, x, y, chunk_size / 2, color_from_palette)

    tmp_image.save("tmp.png", "PNG")
    output_image.save(output_file, "PNG")

def break_down_block(in_image, out_image, x, y, chunk_size, all_colors, minimum_chunk_size = -1):
    if minimum_chunk_size == -1:
        minimum_chunk_size = ((in_image.size[0] + in_image.size[1]) / 2) / 70
    variance = chunk_diff(in_image, x, y, chunk_size)
    if variance < 2000 or chunk_size <= minimum_chunk_size:
        avg_color = chunk_average(in_image, x, y, chunk_size)
        all_colors.append(avg_color)
        fill_chunk(out_image, x, y, chunk_size, avg_color)
    else:
        small_chunk_size = chunk_size / 2
        adjusted_chunk_size = small_chunk_size
        if chunk_size % 2 != 0:
            adjusted_chunk_size += 1
        break_down_block(in_image, out_image, x, y, small_chunk_size, all_colors, minimum_chunk_size)
        break_down_block(in_image, out_image, x + small_chunk_size, y, adjusted_chunk_size, all_colors, minimum_chunk_size)
        break_down_block(in_image, out_image, x, y + small_chunk_size, adjusted_chunk_size, all_colors, minimum_chunk_size)
        break_down_block(in_image, out_image, x + small_chunk_size, y + small_chunk_size, adjusted_chunk_size, all_colors, minimum_chunk_size)

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

def chunk_diff(image, start_x, start_y, chunk_size):
    diff = 0
    for x in xrange(start_x, start_x + chunk_size - 1):
        for y in xrange(start_y, start_y + chunk_size - 1):
            this_r, this_g, this_b = image.getpixel((x, y))
            next_r, next_g, next_b = image.getpixel((x + 1, y + 1))
            diff += math.fabs(next_r - this_r) * math.fabs(next_g - this_g) * math.fabs(next_b - this_b)
    return diff / (chunk_size * chunk_size)

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
