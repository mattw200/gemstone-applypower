#!/usr/bin/env python

# Matthew J. Walker
# Created: 6 Sep 2017

import pandas as pd

def mape(actual, predicted):
    return ((actual - predicted)/actual).abs()*100.0

def mpe(actual,predicted):
    return ((actual - predicted)/actual)*100.0

if __name__=='__main__':
    import argparse
    import os
    import pandas as pd
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-data',  dest='input_data', required=True, \
               help="The data")
    args=parser.parse_args()
    df = pd.read_csv(args.input_data,sep='\t')
    gem5_pwr_cols = [x for x in df.columns.values if x.find('gem5 power') > -1]
    xu3_pwr_cols = [x for x in df.columns.values if x.find('xu3 power') > -1]
    print("gem5 power cols: "+str(gem5_pwr_cols))
    print("xu3 power cols: "+str(xu3_pwr_cols))
    print("Power APE: "+str(mape(df['xu3 power model total power'], df['gem5 power model total power'])))
    print("Power MAPE: "+str(mape(df['xu3 power model total power'], df['gem5 power model total power']).mean()))
    print("Power PE: "+str(mpe(df['xu3 power model total power'], df['gem5 power model total power'])))
    print("Power MPE: "+str(mpe(df['xu3 power model total power'], df['gem5 power model total power']).mean()))

    df['xu3 energy'] = df['xu3 power model total power'] * df['xu3 stat duration (s)']
    df['gem5 energy'] = df['gem5 power model total power'] * df['gem5 stat sim_seconds']

    df['execution time MAPE'] = mape(df['xu3 stat duration (s)'],df['gem5 stat sim_seconds'])
    df['execution time MPE'] = mpe(df['xu3 stat duration (s)'],df['gem5 stat sim_seconds'])
    df['power MAPE'] = mape(df['xu3 power model total power'],df['gem5 power model total power'])
    df['power MPE'] = mpe(df['xu3 power model total power'],df['gem5 power model total power'])
    df['energy MAPE'] = mape(df['xu3 energy'],df['gem5 energy'])
    df['energy MPE'] = mpe(df['xu3 energy'],df['gem5 energy'])

    # now create the df to print!
    # cols: workload name, workload cluster, freq C0, freq C4, xu3 duration, gem5 duration, power model stuffs
    cols = [ 'xu3 stat Freq (MHz) C0', 'xu3 stat Freq (MHz) C4', 'xu3 stat duration (s)', 'gem5 stat sim_seconds']
    cols = cols + xu3_pwr_cols + gem5_pwr_cols + ['xu3 energy', 'gem5 energy', 'execution time MAPE', 'execution time MPE', 'power MAPE', 'power MPE', 'energy MAPE', 'energy MPE']
    out_df = pd.DataFrame(columns=cols)
    out_df = out_df.append(df[cols].mean(),ignore_index=True)
    scenario_list = ['mean']
    # get unique clusters
    for cluster_id in list(set(df['workload A15 clusters'].unique())):
        scenario_list.append('cluster: '+str(cluster_id))
        out_df = out_df.append(df[df['workload A15 clusters'] == cluster_id][cols].mean(), ignore_index=True)
    out_df['scenario'] = scenario_list
    print out_df
    out_df.to_csv(args.input_data+'-per-cluster.csv',sep='\t')
    
