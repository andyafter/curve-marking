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
            data[i][1] = round(new_marked_value, 2)
        else:
            data[i][1] = str(round(float(data[i][1]) + modify_diff, 2))

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
        data.append([t, round(value,2)])
    return data


def mark_singo(ipe, bap):
    # Sing Gas Oil = (IPE(G) + Go East/West(BAP)) / 7.45
    with open(ipe, 'r') as f:
        reader = csv.reader(f)
        ipe_data = list(reader)
    with open(bap, 'r') as f:
        reader = csv.reader(f)
        bap_data = list(reader)

    result = []
    for i in range(min(len(ipe_data), len(bap_data))):
        t = ipe_data[i][0]
        value = (float(ipe_data[i][1])+ float(bap_data[i][1]))/7.45
        result.append([t, round(value,2)])
    return result

def mark_visco(file_180, marked_380):
    # Visco = 180 - 380
    with open(file_180, 'r') as f:
        reader = csv.reader(f)
        data_180 = list(reader)
    l = min(len(data_180), len(marked_380))
    result = []
    for i in range(l):
        t = data_180[i][0]
        value = float(data_180[i][1]) - float(marked_380[i][1])
        result.append([t, round(value,2)])
    return result


def mark_mopj(brent, mopj_crack):
    # Mopj = (Brent + Mopj Crack) * 8.9
    with open(brent, 'r') as f:
        reader = csv.reader(f)
        brent_data = list(reader)
    with open(mopj_crack, 'r') as f:
        reader = csv.reader(f)
        mopj_crack_data = list(reader)
    result = []
    for i in range(min(len(brent_data), len(mopj_crack_data))):
        t = brent_data[i][0]
        value = (float(brent_data[i][1])+ float(mopj_crack_data[i][1]))*8.9
        result.append([t, round(value,2)])
    return result

def mark_gasoline():

    pass

def generate_table(data_dict):
    latex_table = "\\begin{tabular}{|c|c|c|c|c|}\n"
    latex_table += "\\hline\n"
    latex_table += "Month & " + " & ".join([f"{k}" for k in data_dict.keys()]) + " \\\\\n"
    latex_table += "\\hline\n"
    for i in range(len(data_dict[list(data_dict.keys())[0]])):  # assuming all lists are of same length
        month = data_dict[list(data_dict.keys())[0]][i][0]
        values = []
        for k in data_dict.keys():
            values.append(str(data_dict[k][i][1]))
        latex_table += month + " & " + " & ".join(values) + " \\\\\n"
        if i < len(data_dict[list(data_dict.keys())[0]]) - 1:
            spread_month = f"{month}/{data_dict[list(data_dict.keys())[0]][i+1][0]}"
            spreads = []
            for k in data_dict.keys():
                spread = data_dict[k][i][1] - data_dict[k][i+1][1]
                spreads.append(str(round(spread, 2)))
            latex_table += "\\small{" + spread_month + "} & \\small{" + "} & \\small{".join(spreads) + "} \\\\\n"
    latex_table += "\\hline\n"
    latex_table += "\\end{tabular}\n\n"
    return latex_table

if __name__ == '__main__':
    product = "data/0.5.csv"
    # mark(product, "Aug23/Sep23", "8.5")
    marked_380 = mark_380("data/brent.csv", "data/barge.csv", "data/sjs.csv")
    marked_singo = mark_singo("data/ipe.csv", "data/bap.csv")
    marked_visco = mark_visco("data/szs.csv", marked_380)
    marked_mopj = mark_mopj("data/brent.csv", "data/nbg.csv")

    data_dict = {"380": marked_380, "Sing GO": marked_singo, "Visco": marked_visco, "Mopj": marked_mopj}
    latex_table = generate_table(data_dict)

    with open("combined_table.tex", "w") as file:
        file.write("\\documentclass{article}\n")
        file.write("\\usepackage{graphicx}\n")
        file.write("\\usepackage{fancyhdr}\n")  # Add this line to use the fancyhdr package
        file.write("\\pagestyle{fancy}\n")  # Set the page style to fancy
        file.write("\\fancyhf{}\n")  # Clear all header and footer fields
        file.write("\\renewcommand{\\headrulewidth}{0pt}\n")  # Remove the header line
        file.write("\\fancyhead[L]{\\includegraphics[width=3.5cm]{logo.png}}\n")  # Add the logo to the left header
        file.write("\\begin{document}\n")
        file.write(latex_table)
        file.write("\\end{document}")

    print("LaTeX file has been written to combined_table.tex")
