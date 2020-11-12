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
               'PRTAGE_x': 'Age',
               'target': 'Employment Status',
               'PEHRACTT': 'Hours Worked in a Week'
               
              }

ticks_dict = {'PESEX_x': ['Male', 'Female'],
              'PREMPNOT_y': ['Employed', 'Unemployed', 'NILF\nDiscouraged', 'NILF\nOther'],
              'target': ['Employed', 'Not Employed']
             }



def PlotCat(df, xvar, targetdir, yvar=None, kind='count', hue=None, palette="coolwarm"):
    """Plot a categorical plot with automatic labels provided in a global dict in CustomModule. 
        Pass a dataframe through `df`, a string through `xvar`, and where to save the image through
        `targetdir`. 
    """
    m_label = month_label(xvar)
    
    if yvar:
        y_label = labels_dict[yvar] + ' in April 2020'
    else:
        y_label = 'Frequency'
        
    
    title = f'{y_label} vs. \n{labels_dict[xvar]} Categories{m_label}'
    

    
    
    fig = sns.catplot(data=df,
                x=xvar,
                y=yvar,
                kind = kind,
                hue = hue,
                height = figsize[0],
                aspect = figsize[1]/figsize[0],
                palette=palette
               )
    plt.xlabel(labels_dict[xvar])
    plt.ylabel(y_label)
    plt.title(title)
    labels = ticks_dict[xvar]
    plt.xticks(list(range(len(labels))), labels)
    if 'PREMPNOT' in xvar:
        plt.xticks(rotation=-25)
    
    
    if yvar and 'PEHRACTT' in yvar:
        plt.ylim((0, 140))
    fig.savefig(f'{targetdir}{title}.png', bbox_inches='tight')

    return plt.show()

def month_label(var):
    if ('_y' in var) or ('target' in var):
        var = ' in July 2020'
    else:
        var= ''
    return var
        
