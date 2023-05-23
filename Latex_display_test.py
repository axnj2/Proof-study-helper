import matplotlib.pyplot as plt


def display_math(latex_code):
    plt.figure(figsize=(12, 2))
    ax = plt.subplot()
    plt.subplots_adjust(left=0)
    ax.axis('off')
    ax.text(0,0, latex_code,fontsize=12,color="Black", )
    plt.show()