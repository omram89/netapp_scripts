import os
import sys
import glob
import numpy  as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

#sys.path.insert(0, '/home/om/Downloads/netapp_scripts/commons')
#import dataloader
#from dataloader import load_joined_ems_events

COLNAMES_EMS_EVENTS = 'timestamp,seqID,eventType,severity,nodeName,stack,shelf,bay,dev,componentName'.split(',')
COLNAMES_RAID_GROUP = 'raidGroup,stack,shelf,bay,dev,type'.split(',')
def load_ems_events(path=None, low_memory=True, delim=None):

    ems_glob = os.path.join(path, 'ems-events-split*.csv')

    ret_df = None
    
    for filename in sorted(glob.iglob(ems_glob)):
        df = pd.read_csv(filename, delimiter=delim, header=None, names=COLNAMES_EMS_EVENTS, low_memory=low_memory)

        df['stack'].replace('NULL', np.nan, inplace=True)
        df['stack'].replace('', np.nan, inplace=True)
        df['shelf'].replace('', np.nan, inplace=True)
        df.dropna(subset=['stack'], inplace=True)
        #df = df[df.shelf != '?']


        raid_filename = filename.replace('ems-events','raid-groups')
        raid_df = pd.read_csv(raid_filename, delimiter=',', header=None, names=COLNAMES_RAID_GROUP, low_memory=low_memory)
        raid_df = raid_df.drop_duplicates(subset=COLNAMES_RAID_GROUP)

        merged = df.merge(raid_df, how='left', left_on=['stack','shelf','bay','dev'], right_on=['stack','shelf','bay','dev'], sort=False, suffixes=('',''))
        if ret_df is None:
            ret_df = merged
        else:
            ret_df = pd.concat([merged, ret_df])

    #ret_df = ret_df[np.isfinite(ret_df['stack'])]
    #ret_df['stack'].replace('NULL', np.nan, inplace=True)
    #ret_df['stack'].replace('', np.nan, inplace=True)
    #ret_df['shelf'].replace('', np.nan, inplace=True)

    #ret_df.dropna(subset=['stack'], inplace=True)
    ret_df.sort_values(['timestamp','seqID'], inplace=True)
    return ret_df
    #ret_df = ret_df.join(ret_df)


final_df = load_ems_events('/home/om/Downloads/NetApp_dataset/20170522-SystemA/systemA', True,',')

#final_df['shelf'] = pd.Series([], dtype=object)
#final_df = final_df[final_df.shelf != '?']
final_df['shelf'] = final_df['shelf'].astype(np.uint64)
final_df['timestamp'] = pd.to_datetime(final_df['timestamp'], format='%Y-%m-%dT%H:%M:%S:%f')

gb1 = final_df.groupby(['nodeName', 'stack','shelf']).count().to_csv('/home/om/Downloads/data_figures/fig115_new.csv',sep=',')

#gb1 = final_df.groupby(['nodeName', 'stack']).count().to_csv('/home/om/Downloads/data_figures/fig116.csv',sep=',')

#gb1 = final_df.groupby(['nodeName', 'stack']).count().to_csv('/home/om/Downloads/data_figures/fig121.csv',sep=',')

#gb1 = final_df.groupby(['shelf','bay']).count().to_csv('/home/om/Downloads/data_figures/fig111.csv',sep=',')

#gb1 = final_df.groupby(['nodeName','stack','shelf']).to_csv('/home/om/Downloads/data_figures/fig114.csv',sep=',')

#final_df.to_csv('/home/om/Downloads/data_figures/final_df_all.csv',sep=',')

#print(final_df['timestamp'])
#print(final_df.index)
#gb1 = final_df.groupby(final_df['timestamp'].dt.date,final_df['nodeName']).count()
#final_df.sort_values(['nodeName','timestamp'],inplace=True)
#final_df.set_index('timestamp').groupby([pd.TimeGrouper(freq='D'), 'nodeName']).count().to_csv('/home/om/Downloads/data_figures/gb_ts_node_cnt.csv',sep=',')

#gb1 = final_df.set_index('timestamp').groupby([pd.TimeGrouper(freq='D'), 'nodeName']).count()

#gb2 = final_df.set_index('timestamp').groupby([pd.Grouper(freq='D'),'nodeName','stack','shelf','bay','dev']).count().to_csv('/home/om/Downloads/data_figures/gb_ts_node_all_cnt.csv',sep=',')

#gb3 = final_df.set_index('timestamp').groupby([pd.Grouper(freq='H'),'eventType','nodeName','stack','shelf','bay','dev']).count().to_csv('/home/om/Downloads/data_figures/gb_tsH_err_all_cnt.csv',sep=',')

#test = pd.pivot_table(gb1, index='timestamp', columns='nodeName', values='seqID')
#test = test.fillna(method='pad')
#test = test.fillna(method='bfill')

#test.plot(style='.')
#plt.show()

#final_df.groupby()
#print(gb1)
#print(final_df.dtypes)
#final_df.to_csv('/home/om/Downloads/data_figures/final_df_raid.csv',sep=',')
#final_df.sort_values(['eventType','nodeName','stack','shelf','bay'],inplace=True)
#gb1.last().sort_values('nodeName').to_csv('/home/om/Downloads/data_figures/gb_evnt_node.csv',sep=',')
#final_df.to_csv('/home/om/Downloads/data_figures/final_df_all.csv',sep=',')
#print(len(final_df.index))
#err_cnt = len(final_df.index)
#n_err_cnt = 8 * err_cnt // 10
#print(n_err_cnt)

#cnt_plt = final_df.groupby("bay").ids.agg(lambda x:len(x.unique()))

#pd.value_counts(final_df['bay']).plot(kind="bar")
#sr = pd.value_counts(final_df['bay'])
#sr = pd.value_counts(final_df['shelf'])
#sr = pd.value_counts(final_df['raidGroup'])
#sr.plot(kind="bar")
#print(sr)
#sr.to_csv('/home/om/Downloads/data_figures/raid_plot.csv',',')

#print(final_df.head(1000))
#final_df.hist(column='bay', bins=24)
#final_df.hist(column='bay', bins=division)
#plt.axis('auto')
#bay_fig = bay_hist.get_figure()
#bay_fig.savefig('./bay_hist.pdf')
#bay_hist.plot()
#plt.show()

## Heat Map code - Begins

#htmap_list = [[0,4,0,95],[198,0,268,0],[122,0,0,0],[0,77,335,0],[0,186,0,0],[202,0,0,260]]
#htmap_df = pd.DataFrame(htmap_list)
#sns.heatmap(htmap_df, cmap='Reds', fmt="g", annot=True)
#sns.heatmap(htmap_df, cmap='Reds')
#plt.show()

## Heat Map code - Ends

