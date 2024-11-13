from PIL import Image
import argparse
import os
import sys


def load_custom_style(style_name):
    style_folder = 'Styles'
    file_path = os.path.join(style_folder, f'{style_name}.txt')
    if not os.path.exists(file_path):
        print(f"Error: Style file '{style_name}.txt' not found in '{style_folder}' folder.")
        exit(1)
    with open(file_path, 'r') as f:
        content = f.read()
    ascii_chars = [char.strip() for char in content.split(',') if char.strip()]
    if not ascii_chars:
        print(f"Error: No valid ASCII characters found in '{style_name}.txt'.")
        exit(1)
    return ascii_chars

def zoom_ascii(ascii_art, zoom_factor):
    if zoom_factor == 1:
        return ascii_art

    lines = ascii_art.splitlines()

    if zoom_factor > 1:
        zoomed_lines = []
        for line in lines:
            zoomed_line = ""
            for char in line:
                zoomed_line += char * zoom_factor
            zoomed_lines.extend([zoomed_line] * zoom_factor)
        zoomed_ascii = "\n".join(zoomed_lines)
        return zoomed_ascii

    elif zoom_factor < -1:
        reduction_factor = abs(zoom_factor)

        ascii_chars = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']
        char_brightness_map = {char: idx for idx, char in enumerate(ascii_chars)}
        brightness_char_map = {idx: char for idx, char in enumerate(ascii_chars)}

        max_line_length = max(len(line) for line in lines)
        lines = [line.ljust(max_line_length) for line in lines]

        brightness_matrix = []
        for line in lines:
            brightness_row = [char_brightness_map.get(char, 0) for char in line]
            brightness_matrix.append(brightness_row)

        reduced_height = len(brightness_matrix) // reduction_factor
        reduced_width = len(brightness_matrix[0]) // reduction_factor
        reduced_brightness_matrix = []

        for i in range(reduced_height):
            row = []
            for j in range(reduced_width):
                block_brightness = []
                for di in range(reduction_factor):
                    for dj in range(reduction_factor):
                        y = i * reduction_factor + di
                        x = j * reduction_factor + dj
                        if y < len(brightness_matrix) and x < len(brightness_matrix[0]):
                            block_brightness.append(brightness_matrix[y][x])
                avg_brightness = sum(block_brightness) / len(block_brightness)
                avg_brightness_idx = int(round(avg_brightness))
                avg_char = brightness_char_map.get(avg_brightness_idx, ' ')
                row.append(avg_char)
            reduced_brightness_matrix.append(row)

        reduced_ascii_lines = [''.join(row) for row in reduced_brightness_matrix]
        reduced_ascii = '\n'.join(reduced_ascii_lines)
        return reduced_ascii
    else:
        return ascii_art


def view_ascii_files():
    ascii_folder = 'ASCII'
    ascii_files = os.listdir(ascii_folder)
    if not ascii_files:
        print("No ASCII files found.")
        return

    print("ASCII Files:")
    for i, file in enumerate(ascii_files):
        print(f"{i + 1}. {file}")

    while True:
        choice = input("Enter the number of the file to view (or 'q' to quit): ")
        if choice == 'q':
            break

        try:
            file_index = int(choice) - 1
            if 0 <= file_index < len(ascii_files):
                file_path = os.path.join(ascii_folder, ascii_files[file_index])
                with open(file_path, 'r') as f:
                    ascii_art = f.read()

                zoom_factor = int(input("Enter the zoom factor (e.g., 2 for 2x zoom): "))
                zoomed_art = zoom_ascii(ascii_art, zoom_factor)
                print(zoomed_art)
            else:
                print("Invalid file number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'.")


def ascii_converter():
    try:
        image = Image.open(f'Pics/{args.img_name}.jpg')
    except FileNotFoundError:
        print("Error: Image file not found.")
        exit(1)

    width, height = image.size
    new_height = args.height or height // 13
    new_width = args.width or width // 5

    try:
        resized_image = image.resize((new_width, new_height))
    except Exception as e:
        print("An error occurred while resizing the image:", str(e))
        exit(1)

    if args.style:
        ascii_chars = load_custom_style(args.style)
    else:
        ascii_chars = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']

    char_step = 255 // (len(ascii_chars) - 1)
    ascii_art = ''

    for y in range(resized_image.size[1]):
        for x in range(resized_image.size[0]):
            try:
                r, g, b = resized_image.getpixel((x, y))
            except Exception as e:
                print("An error occurred while retrieving pixel data:", str(e))
                exit(1)
            grayscale = int(0.21 * r + 0.72 * g + 0.07 * b)
            char_index = min(grayscale // char_step, len(ascii_chars) - 1)
            ascii_art += ascii_chars[char_index]
        ascii_art += '\n'

    if args.write:
        with open(f'ASCII/{args.img_name}_ascii_art.txt', 'w') as f:
            f.write(ascii_art)

    print(ascii_art)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('img_name', nargs='?', type=str, help='Choose Image from <<Pics>> folder for converting into ASCII-art')
    parser.add_argument('--height', type=int, help='Choose ASCII-art height')
    parser.add_argument('--width', type=int, help='Choose ASCII-art width')
    parser.add_argument('--write', action='store_true', help='Write your ASCII-art into .txt file')
    parser.add_argument('--view', action='store_true', help='Show ASCII-art files from ASCII folder')
    parser.add_argument('--style', type=str, help='Choose a style from Styles folder to use custom ASCII characters')
    args = parser.parse_args()

    if args.view:
        view_ascii_files()
    else:
        if not args.img_name:
            print("Error: Image name is required unless using --view.")
            exit(1)
        ascii_converter()
