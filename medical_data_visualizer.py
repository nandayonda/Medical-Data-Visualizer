import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['overweight'] = ((df['weight'])/(df['height']/100)**2).round(2)
df['overweight'] = df['overweight'].apply(lambda x: 0 if x<=25 else 1)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x==1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x==1 else 1)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df,id_vars='cardio', value_vars=['cholesterol','gluc','smoke','alco','active','overweight'])
    df_cat = df_cat.sort_values(by='cardio').reset_index().drop(['index'],axis=1)


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.pivot_table(columns=['cardio','variable','value'], aggfunc='size').reset_index()
    df_cat.rename(columns = {0 : 'total'}, inplace=True)

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(x='variable',y='total',hue='value',col='cardio',data=df_cat,kind='bar')
    



    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo']<=df['ap_hi'])&(df['height']>=df['height'].quantile(0.025))&(df['height']<=df['height'].quantile(0.975))&(df['weight']>=df['weight'].quantile(0.025))&(df['weight']<=df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr,dtype=bool))



    # Set up the matplotlib figure
    fig, ax = plt.subplots()

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr,vmin=-0.16, vmax=0.32, center=0, mask=mask, annot=True, cbar_kws={'shrink': 0.5, 'ticks': [-0.08, 0.00, 0.08, 0.16, 0.24]}, fmt='.1f')



    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
