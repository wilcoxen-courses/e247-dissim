#! /bin/python3
#  Spring 2021 (PJW)
#
#  Demonstrate appending, joining, and selecting data
#

import pandas as pd
import matplotlib.pyplot as plt

#%%
#
#  Read two files of data on generators and then append them. Create
#  a county variable to track source.
#

gen_oswego   = pd.read_csv('generators-oswego.csv')
gen_oswego['county'] ='Oswego'

gen_onondaga = pd.read_csv('generators-onondaga.csv')
gen_onondaga['county'] ='Onondaga'

gen_all = pd.concat( [gen_oswego, gen_onondaga] )

#%%
#
#  Read a file of plant information for several counties
#

plants = pd.read_csv('plants.csv')

#
#  Use a left m:1 join to add the plant information to the generators
#

both = gen_all.merge(plants,
                     on='Plant Code',
                     how='left',
                     validate='m:1',
                     indicator=True)

#%%
#
#  Check the outcome
#

print( both['_merge'].value_counts() )
both = both.drop(columns='_merge')

#
#  Set the index for good measure. Do it after the merge because merging
#  discards the index.
#

both = both.set_index(['Plant Code','Generator ID'])

#%%
#
#  Select records for one plant using the index
#

plant_2589 = both.xs(2589,level='Plant Code')
print( plant_2589 )

#
#  Select records for a technology using .query()
#

ngcc = both.query("Technology == 'Natural Gas Fired Combined Cycle'")
print( ngcc )

#
#  Select records based on a boolean series
#

is_newish = both['Operating Year'] >= 1990

newish = both[ is_newish ]
print( newish )

#%%
#
#  Group data and construct selected aggregates
#

tech_by_kv = both.groupby(['Grid kV','Technology'])

summary = pd.DataFrame()
summary['units'] = tech_by_kv.size()
summary['mw'] = tech_by_kv['Capacity MW'].sum()

print( summary )

#%%
#
#  Draw a bar graph. Flip the sort order so that the smallest voltages are
#  at the top and the largest are at the bottom. Looks best because the
#  bottom bars are much longer than the top ones.
#

summary = summary.sort_index(ascending=False)

fig1, ax1 = plt.subplots(dpi=300)
fig1.suptitle('Electric Power Plants in Onondaga and Oswego')
summary.plot.barh(y='mw',ax=ax1,legend=None)
ax1.set_xlabel('MW')
