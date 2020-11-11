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


labels_dict = {
               'Features': 'Features',
               'LogRegCoeff': 'Logistic Regression\n Coefficients'
               
              }

ticks_dict = {'LogRegCoeff': [0, 1, 2, 4, 5, 6, 7, 8, 9],
             }



def PlotCat(df, xvar,targetdir, yvar=None, orient=None, kind='count',palette="coolwarm"):
    """Plot a categorical plot with automatic labels provided in a global dict in CustomModule. 
        Pass a dataframe through `df`, a string through `xvar`, and where to save the image through
        `targetdir`. 
    """
    m_label = month_label(xvar)
    
    title = f'Frequency of {labels_dict[xvar]} Categories{m_label}'
    

    
    
    fig = sns.catplot(data=df,
                x=xvar,
                y=yvar,
                kind = kind,
                orient = orient,
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
        
    fig.savefig(f'{targetdir}{title}.png', bbox_inches='tight')

    return plt.show()

def month_label(var):
    if '_y' in var:
        var = ' in July 2020'
    else:
        var= ''
    return var