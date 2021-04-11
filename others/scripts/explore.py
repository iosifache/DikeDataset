#!/usr/bin/env python3
"""Python 3 script for analyzing the dataset labels and for creating
tables and images.

Before running the script, install the Python 3 dependencies by
executing the command `pip3 install requirements.txt`.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas
import seaborn as sns
from tabulate import tabulate

# Constants
LABELS_FOLDER = "../../labels/"
TABLES_FOLDER = "../tables/"
IMAGES_FOLDER = "../images/"
BENIGN_LABELS = LABELS_FOLDER + "benign.csv"
MALWARE_LABELS = LABELS_FOLDER + "malware.csv"
LABELS_TABLE = TABLES_FOLDER + "labels.md"
UNIVARIATE_ANALYSIS_TABLE = TABLES_FOLDER + "univariate_analysis.md"
DISTRIBUTION_IMAGE = IMAGES_FOLDER + "distribution.png"
HISTOGRAMS_IMAGE = IMAGES_FOLDER + "histograms.png"

# Import the datasets
benign_df = pandas.read_csv(BENIGN_LABELS)
malware_df = pandas.read_csv(MALWARE_LABELS)

# Generate the samples distribution plot
all_df = pandas.merge(benign_df, malware_df, how="outer")
all_df["is_malware"] = all_df.malice > 0
all_df = all_df.groupby(["is_malware", "type"]).size().unstack(level=0)
sns.heatmap(data=all_df,
            xticklabels=["Benign", "Malicious"],
            yticklabels=["PE", "OLE"],
            annot=True,
            fmt="d")
plt.xlabel("Malice")
plt.ylabel("Filetype")
print("[+] The plot with the samples distribution was saved.")
plt.savefig(DISTRIBUTION_IMAGE)

# Generate the characteristics table
column_types = [(column_type[0], str(column_type[1]))
                for column_type in malware_df.dtypes.items()]
labels_table = tabulate(column_types, ["Name", "Type"], tablefmt="github")
with open(LABELS_TABLE, "w") as labels_file:
    labels_file.write(labels_table)
print(
    "[+] The table containing the characteristics of the dataset was dumped.")

# Generate the univariate analysis table
analysis_malware_df = malware_df.loc[:, malware_df.columns != "type"]
analysis_df = analysis_malware_df.describe(percentiles=[])
analysis_df = analysis_df.drop(["count", "50%"])
uni_analysis_table = tabulate(analysis_df, headers="keys", tablefmt="github")
with open(UNIVARIATE_ANALYSIS_TABLE, "w") as uni_analysis_file:
    uni_analysis_file.write(uni_analysis_table)
print("[+] The table containing the univariate analysis was dumped.")

# Generate a histogram for each numeric label
numeric_columns = analysis_malware_df.select_dtypes(
    include=np.number).columns.tolist()
plots_count = len(numeric_columns)
total_cols = 2
total_rows = plots_count // total_cols
fig, axs = plt.subplots(nrows=total_rows,
                        ncols=total_cols,
                        figsize=(7 * total_cols, 7 * total_rows),
                        constrained_layout=True)
for i, column_name in enumerate(numeric_columns):
    row = i // total_cols
    column = i % total_cols

    plot = sns.histplot(data=analysis_malware_df,
                        x=column_name,
                        ax=axs[row][column])

    if (i == 0):
        new_label = column_name.capitalize()
    else:
        new_label = column_name.capitalize() + " Family Membership"
    plt.setp(axs[row, column], xlabel=new_label)
plt.setp(axs[:, :], ylabel="Count")
plt.savefig(HISTOGRAMS_IMAGE)
print("[+] The plot containing a histogram for each numeric label was saved.")
