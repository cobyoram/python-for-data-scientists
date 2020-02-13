import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

# ----- FUNCTION FOR DISTRIBUTIONS ---------------|
def auto_subplots(df, **kwargs):
    '''
    This function creates a series of sublots to display the distribution for all continuous variables in a DataFrame
    It operates like a FacetGrid, but it's a little more customized.

    The dimensions of the subplot (no_subplots X no_subplots) are calculated automatically by how many continuous variables are found.
    You can use a number of kwargs to customize the output of the function. Those include:
    kwargs:
        limitx  -   Limits the number of subplots along the x-axis, and calculates the no_subplots on y axis from given limit
        kind    -   Allows you to specify which type of distribution grid you'd like to use. Values include
            -   hist: creates a matplotlib.pyplot histogram
            -   boxplot: creates a seaborn boxplot
                -   whis: adjust the boxplot whisker bounds
            -   swarm: create a one-dimensional seaborn swarmplot

    Enjoy!

    '''
    EACH_SIZE = 3
    WSPACE = .3
    HSPACE = .7
    DEFAULT_BOXPLOT_WHIS = 1.5

    columns = df.select_dtypes(include='number').columns
    len_cols = len(columns)

    if kwargs.get('limitx'):
        limitx = kwargs.get('limitx')
        count_dimensions = tuple([limitx, int(count_dimensions/limitx + 1)])

    else:
        try_num = len_cols
        while True:
            sq = math.sqrt(try_num)
            if sq == int(sq):
                break
            try_num += 1
        count_dimensions = tuple([sq, sq])

    dimensions = tuple([count_dimensions[0] * EACH_SIZE, count_dimensions[1] * EACH_SIZE])
    plt.figure(figsize=dimensions)

    for i, col in enumerate(columns):
        plt.subplot(count_dimensions[0], count_dimensions[1], i+1)
        if kwargs.get('kind'):
            kind = kwargs.get('kind')
            selection = ['hist', 'boxplot', 'swarm']
            if kind == 'hist':
                plt.hist(df[col])
            elif kind == 'boxplot':
                whis = DEFAULT_BOXPLOT_WHIS
                if kwargs.get('whis'):
                    whis = kwargs.get('whis')
                sns.boxplot(df[col], whis=whis)
            elif kind == 'swarm':
                sns.swarmplot(y=col, data=df)
            else:
                print('Kind: {} is currently unavailable. For now enjoy our limited selection of: {}'.format(kind, selection))
        else:
            plt.hist(df[col])
        plt.title(col)

    plt.subplots_adjust(wspace=WSPACE, hspace=HSPACE)
    plt.show()
# ------- END OF DISTRIBUTION SELF_MADE FUNCS ----------------------|

# ----- FUNCTION FOR GENERAL MISSING VALUES ---------------|
def missingness_summary(df, print_log, sort):
    s = df.isna().sum()*100/len(df)
    if sort == 'asc':
        s.sort_values(ascending=True, inplace=True)
    elif sort == 'desc':
        s.sort_values(ascending=False, inplace=True)
    if print_log == True:
        print(s)
    return s
# ------- END OF MISSING SELF_MADE FUNCS ----------------------|

# ----- FUNCTIONS FOR GENERAL OUTLIER HANDLING --------------|
def get_minmax_with_threshold(s, threshold):
    q75, q25 = np.percentile(s, [75,25])
    iqr = q75 - q25
    min_val = q25 - (iqr*threshold)
    max_val = q75 + (iqr*threshold)
    
    return min_val, max_val
    
def get_outliers(s, threshold):
    min_val, max_val = get_minmax_with_threshold(s, threshold)
    return s.loc[(s > max_val) | (s < min_val)]

def outliers_summary(df, threshold, print_log, sort):    
    s = pd.Series([get_outliers(df[col], threshold).count() *100 / len(df[col])
                   for col in df.select_dtypes(include='number').columns],
                 index=df.select_dtypes(include='number').columns)
    
    if sort == 'asc':
        s.sort_values(ascending=True, inplace=True)
    elif sort == 'desc':
        s.sort_values(ascending=False, inplace=True)
    if print_log == True:
        print(s)
        
    return s

def get_percentiles(df, column_name, threshold):
    min_val, max_val = get_minmax_with_threshold(df[column_name], threshold)
    
    max_percentile = df.loc[df[column_name] >= max_val, column_name].count() / len(df[column_name])
    min_percentile = df.loc[df[column_name] <= min_val, column_name].count() / len(df[column_name])
    
    return min_percentile, max_percentile
# ------- END OF OUTLIER SELF_MADE FUNCS ----------------------|