import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# Setting global variables

dpi = 300
figsize = (7.5, 6)
fontscale = 2
fontsize = 18
sns.set(font_scale = fontscale, style = 'whitegrid')
markersize = 75


labels_dict = {'PESEX_x': 'Sex',
               'PREMPNOT_y': 'Employment Status',
               'PRTAGE_x': 'Age',
               'target': 'Employment Status',
               'PEHRACTT': 'Hours Worked in a Week',
               'Features': 'Features',
               'LogRegCoeff': 'Logistic Regression\n Coefficients'
               
              }

ticks_dict = {'PESEX_x': ['Male', 'Female'],
              'PREMPNOT_y': ['Employed', 'Unemployed', 'NILF\nDiscouraged', 'NILF\nOther'],
              'target': ['Employed', 'Not Employed'],
              'LogRegCoeff': ['Age', 
                              'Born on U.S. Islands', 
                              'Have More than 1 Job', 
                              'Born on Mainland U.S.', 
                              'Population of State', 
                              'Usual Hours Worked in a Week',
                              'Doctorate Degree',
                              'Family Income',
                              'Fin. Services Ind.',
                              'Actual Hours Worked in a Week'
                             ]
             }







def PlotCatCoeff(df, xvar,targetdir, yvar=None, orient=None, kind='count',palette="coolwarm_r"):
    """Plot a categorical plot with automatic labels provided in a global dict in CustomModule. 
        Pass a dataframe through `df`, a string through `xvar`, and where to save the image through
        `targetdir`. 
    """
    m_label = month_label(xvar)
    
    title = f'Scale of {labels_dict[xvar]}'
    

    fig = sns.catplot(data=df,
                x=xvar,
                y=yvar,
                kind = kind,
                orient = orient,
                height = figsize[1],
                aspect = figsize[0]/figsize[1],
                palette=palette
               )
    plt.ylabel(yvar)
    plt.xlabel('Scale')
    plt.title(title)
    labels = ticks_dict[xvar]
    plt.yticks(list(range(len(labels))), labels)

    fig.savefig(f'{targetdir}{title}.png', bbox_inches='tight')

    return plt.show()

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
    plt.xlabel(labels_dict[xvar], size = fontsize)
    plt.ylabel(y_label, size = fontsize)
    plt.title(title, size=fontsize)
    labels = ticks_dict[xvar]
    plt.xticks(list(range(len(labels))), labels, size=fontsize)
    if 'PREMPNOT' in xvar:
        plt.xticks(rotation=-30)
    
    
    if yvar and 'PEHRACTT' in yvar:
        plt.ylim((0, 140))
#     matplotlib.rcParams.update({'font.size': 18})

    fig.savefig(f'{targetdir}{title}.png', bbox_inches='tight')
    
    
    return plt.show()

def month_label(var):
    if ('_y' in var) or ('target' in var):
        var = ' in July 2020'
    else:
        var= ''
    return var
        
