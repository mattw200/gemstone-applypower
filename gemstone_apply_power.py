#!/usr/bin/env python

# Matthew J. Walker
# Created: 19 August 2017

vf_lookup_df = None

def vlookup(freq_mhz):
    if vf_lookup_df is None:
        raise ValueError("Using vlookup but not vf_looup file specified (-v)")
    import numpy as np
    # NOTE: rounds the frequencies to the nearest 10 (as it is sometimes out by > 0.5)
    freq_mhz = freq_mhz.apply(lambda x : np.around(x,-1).astype(np.uint64))
    print ('Frequencies in input data: '+str(freq_mhz.unique()))
    for f in freq_mhz.unique(): # just checking - otherwise error message is not clear
        if f not in vf_lookup_df['frequency (MHz)'].tolist():
            raise ValueError('input data contains frequency: '+str(f)+ \
                ' MHz which is not in the vf lookup')
    return freq_mhz.apply(lambda x : vf_lookup_df[vf_lookup_df['frequency (MHz)'] == int(x)]['voltage (V)'].iloc[0])
    

def run_model(data_df, params_df, map_dict, map_order, individual_components=True, compare_with=None, prefix='power model '):
    import math
    print(params_df['Name'])
    print(params_df['Value'])
    df = data_df
    # Pre-calculate values in map (not efficient, but allows re-use of results)
    for map_item in map_order:
        df[map_item] = pd.eval(map_dict[map_item],engine='python')
    power = 0
    if individual_components:
        df[prefix+' non-dyn power'] = 0
    for i in range(0, len(params_df.index)):
        param_name = params_df['Name'].iloc[i]
        param_value = float(params_df['Value'].iloc[i])
        param_vars = param_name.split(':')
        formula_string = " * ".join(["("+str(map_dict[x])+")" for x in param_vars])+" * "+str(param_value)
        this_val_power =  pd.eval(formula_string,engine='python')
        if individual_components:
            if param_name.find('EPH_') > -1: # it is a dynamic component
                df[prefix+param_name+' power'] = this_val_power
            else: # it is a non-dynamic component
                df[prefix+' non-dyn power'] += this_val_power
        power += this_val_power
    df[prefix+'total power'] = power
    if compare_with:
        df[prefix+'vs '+compare_with+' signed err'] = ((df[compare_with] - power)/power)*100.0
        df[prefix+'vs '+compare_with+' MAPE'] = ((df[compare_with] - power).abs()/power)*100.0
        print("mean signed error: "+str(df[prefix+'vs '+compare_with+' signed err'].mean()))
        print("mean MAPE: "+str(df[prefix+'vs '+compare_with+' MAPE'].mean()))

def map_dict_from_file(path):
    lines = []
    with open(path,'r') as f:
        lines = f.read().split('\n')
    f.closed
    map_dict = {}
    map_order = []
    for l in lines:
        fields = l.split('\t')
        if len(fields) != 2:
            continue
        map_dict[fields[0].strip()] = fields[1].strip()
        map_order.append(fields[0].strip())
    return (map_dict,map_order)
        
if __name__=='__main__':
    import argparse
    import os
    import pandas as pd
    used_vf = False
    prefix = 'power model '
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--params',  dest='model_params', required=True, \
               help="The parameters file for the model to use")
    parser.add_argument('-i', '--input-data',  dest='input_data', required=True, \
               help="The data")
    parser.add_argument('-m', '--var-map',  dest='var_map', required=True, \
               help="Maps the names of the variables in the data to the model parameters")
    parser.add_argument('-v', '--vf-lookup', dest='vf_lookup', required=False, \
               help="Path to voltage-frequency lookup file")
    parser.add_argument('--compare-with',  dest='compare_with', required=False, \
               help="The name of a column to compare the final power with (optional)")
    parser.add_argument('--prefix', dest='prefix', required=False, \
               help="Optional string to prefix to results columns")
    parser.add_argument('-o', '--output-file', dest='output_file', required=False, \
               help="The output file")
    args=parser.parse_args()
    data_df = pd.read_csv(args.input_data,sep='\t')
    params_df = pd.read_csv(args.model_params,sep='\t')
    map_dict, map_order = map_dict_from_file(args.var_map)  
    if args.prefix:
        prefix = args.prefix
    if args.vf_lookup:
        vf_lookup_df = pd.read_csv(args.vf_lookup,sep='\t')
    run_model(data_df, params_df, map_dict, map_order, compare_with=args.compare_with, prefix=prefix)
    if not args.output_file:
        args.output_file='model-result.csv'
    data_df.to_csv(args.output_file,sep='\t')
    
