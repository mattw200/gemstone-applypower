#!/usr/bin/env python

# Matthew J. Walker
# Created: 21 Sep 2017

working_dir = 'cross_freq_plot_wrapper_working_directory'

model_A7 = 'models/gs-A7-4-pmcs.params'                    
model_A15 = 'models/gs-A15.params'

map_combined_A7 = 'maps/gs-profiler-A7-vlookup.map'
map_combined_A15 = 'maps/gs-profiler-A15-vlookup.map'

map_gem5_A7 = 'maps/gem5-A7-vlookup.map'
map_gem5_A15 = 'maps/gem5-A15-vlookup.map'

def plot_cluster_data_to_series(plot_df,xlabel):
    result_s = pd.Series()
    cols_to_include = [
        'hw stat duration (s)',
        'gem5 stat sim_seconds',
        'hw power model total power',
        'gem5 power model total power',
        'hw energy',
        'gem5 energy',
        'execution time MAPE',
        'execution time MPE',
        'power MAPE',
        'power MPE',
        'energy MAPE',
        'energy MPE'
    ]
    result_s['xlabel'] = xlabel
    clusters = plot_df['scenario'].tolist()
    # duration (s), hw and gem5
    for cluster in clusters:
         temp_row = plot_df[plot_df['scenario'] == cluster].iloc[0]
         for col in [x for x in plot_df.columns.values if x in cols_to_include]:
             result_s[cluster+'-'+col] = temp_row[col]
    print result_s
    #raw_input('waiting')
    return result_s

if __name__=='__main__':
    import argparse
    import os
    import pandas as pd
    parser = argparse.ArgumentParser()
    parser.add_argument('--a7-freqs', dest='a7_freqs', required=False, \
               help="List of A7 frequencies")
    parser.add_argument('--a15-freqs', dest='a15_freqs', required=True, \
               help="List of A15 frequencies")
    parser.add_argument('--a7-in', dest='a7_in', required=True, \
               help="A7 input data")
    parser.add_argument('--a15-in', dest='a15_in', required=True, \
               help="A15 input data")
    parser.add_argument('--a15-vf', dest='a15_vf', required=True, \
               help="A15 v lookup")
    parser.add_argument('--a7-vf', dest='a7_vf', required=True, \
               help="A7 v lookup")
    parser.add_argument('-w','--working-directory', dest='working_directory', required=False)
    args=parser.parse_args()

    if args.working_directory:
        working_dir = args.working_directory
    
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    a7_data_df = pd.read_csv(args.a7_in, sep='\t')
    a15_data_df = pd.read_csv(args.a15_in, sep='\t')
    a7_data_df = a7_data_df[a7_data_df['hw stat core mask'] == '0,1,2,3']
    a15_data_df = a15_data_df[a15_data_df['hw stat core mask'] == '4,5,6,7']
    #debug_cols = [x for x in a15_data_df if x.find('0x14') > -1 or x.find('0x73') > -1 or x.find('0x1b') > -1]
    #a7_data_df.to_csv('DEBUG-A7.csv',sep='\t')
    #a15_data_df[['hw stat workload name', 'hw stat core mask', 'hw stat duration (s)', 'hw stat Freq (MHz) C0', 'hw stat Freq (MHz) C4']+debug_cols].to_csv('DEBUG-A15.csv',sep='\t')
    new_df = pd.DataFrame()
    if args.a7_freqs:
        for a7_freq in [int(x.strip()) for x in args.a7_freqs.split(',')]:
            input_data_filename = os.path.join(working_dir,'working-data-a7-'+str(a7_freq)+'.csv')
            model_out_filename = input_data_filename + '-model-out.csv'
            a7_data_df[a7_data_df['hw stat Freq (MHz) C0'] == a7_freq].to_csv(input_data_filename,sep='\t')
            # run combined model
            if not args.a7_vf:
                os.system('python gemstone_apply_power -p '+model_A7+' -m '+map_combined_A7+' -i '+input_data_filename+' -o '+model_out_filename+' --prefix "hw power model "')
            else:
                os.system('python gemstone_apply_power.py -p '+model_A7+' -m '+map_combined_A7+' -i '+input_data_filename+' -o '+model_out_filename+' --prefix "hw power model " -v '+args.a7_vf+'')
            # add gem5 model 
            if not args.a7_vf:
                os.system('python gemstone_apply_power.py -p '+model_A7+' -m '+map_gem5_A7    +' -i '+model_out_filename+' -o '+model_out_filename+' --prefix "gem5 power model "')
            else:
                os.system('python gemstone_apply_power.py -p '+model_A7+' -m '+map_gem5_A7    +' -i '+model_out_filename+' -o '+model_out_filename+' --prefix "gem5 power model " -v '+args.a7_vf+'')
            # create data for cluster plot
            os.system('python create_plot_data_cluster_bars.py -i '+model_out_filename)
            new_df = new_df.append(plot_cluster_data_to_series(pd.read_csv(model_out_filename+'-power-analysis-per-cluster.csv',sep='\t'),'A7-'+str(a7_freq)+'MHz'),ignore_index=True)

    for a15_freq in [int(x.strip()) for x in args.a15_freqs.split(',')]:
        input_data_filename = os.path.join(working_dir,'working-data-a15-'+str(a15_freq)+'.csv')
        model_out_filename = input_data_filename + '-model-out.csv'
        a15_data_df[a15_data_df['hw stat Freq (MHz) C4'] == a15_freq].to_csv(input_data_filename,sep='\t')
        # run combined model
        if not args.a15_vf:
            os.system('python gemstone_apply_power.py -p '+model_A15+' -m '+map_combined_A15+' -i '+input_data_filename+' -o '+model_out_filename+' --prefix "hw power model "')
        else:
            os.system('python gemstone_apply_power.py -p '+model_A15+' -m '+map_combined_A15+' -i '+input_data_filename+' -o '+model_out_filename+' --prefix "hw power model " -v '+args.a15_vf+'')
        # add gem5 model 
        if not args.a15_vf:
            os.system('python gemstone_apply_power.py -p '+model_A15+' -m '+map_gem5_A15    +' -i '+model_out_filename+' -o '+model_out_filename+' --prefix "gem5 power model "')
        else:
            os.system('python gemstone_apply_power.py -p '+model_A15+' -m '+map_gem5_A15    +' -i '+model_out_filename+' -o '+model_out_filename+' --prefix "gem5 power model " -v '+args.a15_vf+'')
        # create data for cluster plot
        os.system('python create_plot_data_cluster_bars.py -i '+model_out_filename)
        new_df = new_df.append(plot_cluster_data_to_series(pd.read_csv(model_out_filename+'-power-analysis-per-cluster.csv',sep='\t'),'A15-'+str(a15_freq)+'MHz'),ignore_index=True)
    # add normalised cols
    # make performance 1/time
    cols_to_inv = [x for x in new_df.columns.values if x.find('hw stat duration (s)') > -1 or x.find('gem5 stat sim_seconds') > -1]
    for col in cols_to_inv:
        new_df[col+' inv'] = 1.0 / new_df[col]
    vars_to_normalise = [
        'hw stat duration (s) inv',
        'gem5 stat sim_seconds inv',
        'hw power model total power',
        'gem5 power model total power',
        'hw energy',
        'gem5 energy',
    ]
    #init_cols = {}
    cols_to_normalise = [x for x in new_df.columns.values if any(substring in x for substring in vars_to_normalise)]
    # hack - normalise to lowest A15 rather than lowest A7 to get A15 speedup only. - need iloc of first A15 col
    #a15_600_index = new_df[new_df['xlabel'] == 'A15-600MHz'].iloc[0].index
    #print new_df
    #print "Index: "+str(a15_600_index)
    for col in cols_to_normalise:
        new_df[col+' Normalised'] = new_df[col].apply(lambda x: x / new_df[col].iloc[0])
    print("NEWDEBUG: "+str(cols_to_normalise))
    new_df.to_csv(os.path.join(working_dir,'cross-freq-result.csv'),sep='\t')
    simple_cols_perf_hw = [x for x in new_df.columns.values if x.find('hw stat duration (s) inv Normalised') > -1]
    simple_cols_perf_gem5 = [x for x in new_df.columns.values if x.find('gem5 stat sim_seconds inv Normalised') > -1]
    simple_cols_power_hw = [x for x in new_df.columns.values if x.find('hw power model total power Normalised') > -1]
    simple_cols_power_gem5 = [x for x in new_df.columns.values if x.find('gem5 power model total power Normalised') > -1]
    simple_cols_energy_hw = [x for x in new_df.columns.values if x.find('hw energy Normalised') > -1]
    simple_cols_energy_gem5 = [x for x in new_df.columns.values if x.find('gem5 energy Normalised') > -1]
    new_df[['xlabel']+simple_cols_perf_hw].to_csv(os.path.join(working_dir,'cross-freq-result-perf-hw.csv'),sep='\t')
    new_df[['xlabel']+simple_cols_perf_gem5].to_csv(os.path.join(working_dir,'cross-freq-result-perf-gem5.csv'),sep='\t')
    new_df[['xlabel']+simple_cols_power_hw].to_csv(os.path.join(working_dir,'cross-freq-result-power-hw.csv'),sep='\t')
    new_df[['xlabel']+simple_cols_power_gem5].to_csv(os.path.join(working_dir,'cross-freq-result-power-gem5.csv'),sep='\t')
    new_df[['xlabel']+simple_cols_energy_hw].to_csv(os.path.join(working_dir,'cross-freq-result-energy-hw.csv'),sep='\t')
    new_df[['xlabel']+simple_cols_energy_gem5].to_csv(os.path.join(working_dir,'cross-freq-result-energy-gem5.csv'),sep='\t')
    print new_df

