from ares import Board
import pyautogui
import numpy as np
import easyocr

# Where on screen the puzzle is
puzzle_x_osset = 180
puzzle_y_osset = 273

# Read dimensions from screen
dim_x_osset = 184
dim_y_osset = 153

# Get screenshot
myScreenshot = pyautogui.screenshot()

# crop the image from screen
puzzle = np.array(myScreenshot)[puzzle_y_osset:600+puzzle_y_osset, puzzle_x_osset:600+puzzle_x_osset, :]
# crop dimention from screen
number = np.array(myScreenshot)[dim_y_osset:102+dim_y_osset, dim_x_osset:598+dim_x_osset, :]

# Start an OCR
reader = easyocr.Reader(['en'])
result = reader.readtext(number)
dim = result[0][1].split("x")[0].strip()

# Detect Dimension
if "4" in dim:
    dim = 4
elif "6" in dim:
    dim = 6
elif "8" in dim:
    dim = 8
elif "0" in dim:
    dim = 10
else:
    raise IOError("Can't find puzzle.")


# Create a puzzle with the image
the_board = Board.read_from_image(dim, puzzle)
# Solve the puzzle
the_board.solve()
# Click on screen
Board.click(the_board, puzzle.shape[0], puzzle_y_osset, puzzle_x_osset)
