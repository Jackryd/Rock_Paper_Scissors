import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rc

# Assuming 'file.csv' is your CSV file with 'tag' and 'val' columns
with open('text.csv', 'r') as file:
    df = pd.read_csv(file)

    # Grouping the data by 'tag' and summing up 'val'
    df_sum = df.groupby('tag', as_index=False)[['wins', 'games']].sum()

    df_sum['val'] = df_sum['wins'] / df_sum['games']

    # Setting the aesthetic style of the plots
    sns.set_style("whitegrid")

    # Enable LaTeX and set the Computer Modern font
    rc('text', usetex=True)
    rc('text.latex', preamble=r'\usepackage{lmodern}')
    rc('font', family='serif', serif='cmr10')  # Computer Modern Roman

    # Creating a bar plot with narrow bars, pastel colors, and a thin border
    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(x="tag", y="val", data=df_sum, palette="pastel", width=0.5,
                          edgecolor='gray', linewidth=0.5)  # Adding border with edgecolor and linewidth

    # Adding labels and title for clarity
    plt.xlabel("Tag", fontsize=18)
    plt.ylabel("Sum of Values", fontsize=18)
    plt.title("Sum of Values by Tag", fontsize=18)

    # Increase the size of the x-tick labels
    plt.xticks(rotation=45, fontsize=16)  # Increase fontsize here
    plt.yticks(fontsize=16)

    # Looping over the bars in the plot to add text
    for bar in barplot.patches:
        # Formatting the label to display the value ('val') within each bar
        barplot.text(bar.get_x() + bar.get_width() / 2, bar.get_height() / 2, 
                     f'{round(bar.get_height(), 2)}', 
                     ha='center', va='center', fontsize=16, color='black')

    plt.ylim(0, 100)
    # Save the plot as an SVG file with LaTeX fonts and high resolution
    plt.savefig('plot2.svg', format='svg', bbox_inches='tight', dpi=300)  # Increase DPI for higher resolution

    print(df_sum)
