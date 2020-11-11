import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# Setting global variables

dpi = 300
figsize = (7.5, 6)
fontscale = 1.4
sns.set(font_scale = fontscale, style = 'whitegrid')
markersize = 75


labels_dict = {'PESEX_x': 'Sex',
               'PREMPNOT_y': 'Employment Status',
               'PRTAGE_x': 'Age'
               
              }

ticks_dict = {'PESEX_x': ['Male', 'Female'],
              'PREMPNOT_y': ['Employed', 'Unemployed', 'NILF\nDiscouraged', 'NILF\nOther']
             }



def PlotCat(df, xvar, targetdir, kind='count', palette="coolwarm"):
    """Plot a categorical plot with automatic labels provided in a global dict in CustomModule. 
        Pass a dataframe through `df`, a string through `xvar`, and where to save the image through
        `targetdir`. 
    """
    m_label = month_label(xvar)
    
    title = f'Frequency of {labels_dict[xvar]} Categories{m_label}'
    

    fig = plt.figure()
    
    sns.catplot(data=df,
                x=xvar,
                kind = kind,
                height = figsize[0],
                aspect = figsize[1]/figsize[0],
                palette=palette
               )
    plt.xlabel(labels_dict[xvar])
    plt.ylabel('Frequency')
    plt.title(title)
    labels = ticks_dict[xvar]
    plt.xticks(list(range(len(labels))), labels)
    if 'PREMPNOT' in xvar:
        plt.xticks(rotation=-25)

    return plt.show()

def month_label(var):
    if '_y' in var:
        var = ' in July 2020'
    else:
        var= ''
    return var
        
