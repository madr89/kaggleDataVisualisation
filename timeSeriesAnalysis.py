# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 10:48:50 2022

@author: igig
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
import plotly.graph_objects as go

df = pd.read_csv('C:\\Users\igig\Documents\Kaggle\Measurement_summary.csv')
df.head()
df.info()

list_scode = list(set(df['Station code']))
list_scode

list_add = list(df['Address'])
District = [i.split(',')[2] for i in list_add]
df['District'] = District
list_district = list(set(District))

list_district = list(set(District))

list_YM = [i.split(" ")[0][:-3] for i in list(df['Measurement date'])]
list_Year = [i.split(" ")[0][0:4] for i in list(df['Measurement date'])]
list_Month = [i.split(" ")[0][5:7] for i in list(df['Measurement date'])]

df['YM'] = list_YM
df['Year'] = list_Year
df['Month'] = list_Month

#create a monthly dataframe
df_monthly = df.groupby(['Station code', 'District', 'YM', 'Year', 'Month']).mean()
df_monthly = df_monthly[['SO2', 'NO2', 'O3', 'CO','PM10', 'PM2.5']].reset_index()

df_monthly.head()

# PLOTOWANIE DANYCH towardsdatascience.com/8-visualizations-with-python-to-handle
#-multiple-time-series-data-19b5b2e66dd0

sns.set_style('darkgrid')
sns.set(rc={'figure.figsize':(14,8)})

ax = sns.lineplot(data=df_monthly, x='YM', y = 'PM2.5',
                  hue='District', palette='viridis',
                  legend='full', lw=3)
ax.tick_params(axis='x', rotation=60)

#extract color palette, the palette can be changed 
pal = list(sns.color_palette(palette='viridis', n_colors=len(list_scode)).as_hex())


fig = go.Figure()
for d,p in zip(list_district, pal):
    fig.add_trace(go.Scatter(x = df_monthly[df_monthly['District']==d]['YM'],
                             y = df_monthly[df_monthly['District']==d]['PM2.5'],
                             name = d,
                             line_color = p, 
                             fill=None))   #tozeroy 
   
fig.show()

fig = go.Figure()
for d,p in zip(list_district, pal):
    fig.add_trace(go.Scatter(x = df_monthly[df_monthly['District']==d]['YM'],
                             y = df_monthly[df_monthly['District']==d]['PM2.5'],
                             name = d,
                             line_color = p, 
                             fill=None))   #tozeroy 

fig.show()
fig = go.Figure()
for d,p in zip(list_district, pal):
    fig.add_trace(go.Scatter(x = df_monthly[df_monthly['District']==d]['YM'],
                             y = df_monthly[df_monthly['District']==d]['PM2.5'],
                             name = d,
                             line_color = p, 
                             fill='tozeroy'))   #tozeroy 

fig.show()
#------------------------------------------------------------------------------
g = sns.relplot(data = df_monthly, x = "YM", y = "PM2.5",
                col = "District", hue = "District",
                kind = "line", palette = "Spectral",   
                linewidth = 4, zorder = 5,
                col_wrap = 5, height = 3, aspect = 1.5, legend = False
               )

#add text and silhouettes
for time, ax in g.axes_dict.items():
    ax.text(.1, .85, time,
            transform = ax.transAxes, fontweight="bold"
           )
    sns.lineplot(data = df_monthly, x = "YM", y = "PM2.5", units="District",
                 estimator = None, color= ".7", linewidth=1, ax=ax
                )

ax.set_xticks('')
g.set_titles("")
g.set_axis_labels("", "PM2.5")
g.tight_layout()


g = sns.FacetGrid(df_monthly, col="Year", row="Month", height=4.2, aspect=1.9)
g = g.map(sns.barplot, 'District', 'PM2.5', palette='viridis', ci=None, order = list_district)

g.set_xticklabels(rotation = 90)
plt.show()


#%
df_pivot = pd.pivot_table(df_monthly,
                          values='PM2.5',
                          index='District',
                          columns='YM')

df_pivot

plt.figure(figsize = (40,19))
plt.title('Average Monthly PM2.5 (mircrogram/m3)',fontsize=22)

#
sns.heatmap(df_pivot, annot=True, cmap='RdYlBu_r', fmt= '.4g')
plt.xticks(rotation=45)
plt.xlabel('Year-Month', fontsize=22)
plt.ylabel('District', fontsize=22)
plt.tick_params(axis='both', which='major', labelsize=18)
plt.show()

