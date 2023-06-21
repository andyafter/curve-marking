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
    \begin{document}
    """ + latex_table + r"""
    \end{document}
    """

    # Write the LaTeX document to a .tex file
    with open('table.tex', 'w') as f:
        f.write(latex_document)

    # Use pdflatex to generate a PDF from the .tex file
    os.system('pdflatex table.tex')

if __name__ == '__main__':
    product = "0.5.csv"
    mark(product, "Aug23/Sep23", "8.5")
