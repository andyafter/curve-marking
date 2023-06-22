import csv
import os
from tabulate import tabulate

def mark(product, mark_month, new_marked_value):
    # Read the CSV file into a list of lists
    with open(product, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    modify_diff = 0
    # Find the row with the specified month and update its value
    for i in range(1,len(data)):
        if data[i][0] == mark_month:
            modify_diff = float(new_marked_value) - float(data[i][1])
            data[i][1] = new_marked_value
        else:
            data[i][1] = str(float(data[i][1]) + modify_diff)

    # Convert the data into a LaTeX table
    latex_table = tabulate(data, tablefmt="latex")

    # Create a complete LaTeX document
    latex_document = r"""
    \documentclass{article}
    \usepackage{helvet}  % Load the Helvetica font package
    \begin{document}
    {\fontfamily{phv}\selectfont  % Start a group with the Helvetica font
    """ + latex_table + r"""
    }  % End the group
    \end{document}
    """

    # Write the LaTeX document to a .tex file
    with open('table.tex', 'w') as f:
        f.write(latex_document)

    # Use pdflatex to generate a PDF from the .tex file
    os.system('pdflatex table.tex')


def mark_380(brent, barge, sjs):
    with open(brent, 'r') as f:
        reader = csv.reader(f)
        brent_data = list(reader)
    with open(barge, 'r') as f:
        reader = csv.reader(f)
        barge_data = list(reader)
    with open(sjs, 'r') as f:
        reader = csv.reader(f)
        sjs_data = list(reader)

    data = []
    for i in range(min(len(brent_data), len(barge_data), len(sjs))):
        t = brent_data[i][0]
        value = (float(brent_data[i][1])+ float(barge_data[i][1]))*6.35 + float(sjs_data[i][1])
        data.append([t, round(value,3)])
    return data


def mark_gasoline():

    pass

if __name__ == '__main__':
    product = "data/0.5.csv"
    # mark(product, "Aug23/Sep23", "8.5")
    print(mark_380("data/brent.csv", "data/barge.csv", "data/sjs.csv"))
