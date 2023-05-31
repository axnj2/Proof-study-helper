from matplotlib import pyplot as plt

# constants for matplotlib LATEX display
FONT_SIZE = 14
FONT_COLOR = "black"
DISPLAY_SHAPE = (12, 2) # a rectangle, width, height in inches

def display_math(latex_code):
    plt.figure(figsize=DISPLAY_SHAPE)
    ax = plt.subplot()
    plt.subplots_adjust(left=0)
    ax.axis('off')
    ax.text(0, 0, latex_code, fontsize=FONT_SIZE, color=FONT_COLOR)
    plt.show()