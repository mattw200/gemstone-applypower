#!/usr/bin/env python

# Matthew J. Walker
# Created: 20 December 2017

if __name__=='__main__':
    import argparse
    import os
    import pandas as pd
    import gemstone_apply_power as gsp
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--params',  dest='model_params', required=True, \
               help="The parameters file for the model to use")
    parser.add_argument('-m', '--var-map',  dest='var_map', required=True, \
               help="Maps the names of the variables in the data to the model parameters")
    #parser.add_argument('-v', '--vf-lookup', dest='vf_lookup', required=False, \
               #help="Path to voltage-frequency lookup file")
    parser.add_argument('-s', '--separator', dest='separator', required=False, \
               default='" + \\\n "', help="How to separate each component")
    parser.add_argument('-b', '--before', dest='before', required=False, \
               default='"', help="Prefix  the equation")
    parser.add_argument('-a', '--after', dest='after', required=False, \
               default='"', help="Postfix of the equation")
    parser.add_argument('-o', '--output-file', dest='output_file', required=False, \
               help="The output file")
    args=parser.parse_args()
    params_df = pd.read_csv(args.model_params,sep='\t')
    map_dict, map_order = gsp.map_dict_from_file(args.var_map)  
    #if args.vf_lookup:
        #vf_lookup_df = pd.read_csv(args.vf_lookup,sep='\t')
    if not args.output_file:
        args.output_file='equation.txt'
    # 1. map file can refer to variables in itself - first, check for this
    # go through each variable in the map file and check that 'x' (df['x']) is not defined in the map file
    previous_items = []
    for map_item in map_order:
        # make substitutions
        for pitem in previous_items:
              pitem_string = 'df["'+pitem+'"]'
              map_dict[map_item] = map_dict[map_item].replace(pitem_string,map_dict[pitem])
              pitem_string = "df['"+pitem+"']"
              map_dict[map_item] = map_dict[map_item].replace(pitem_string,map_dict[pitem])
        previous_items.append(map_item)
    # Finished transforming map
    # 2. Make substitutions for model params
    equation_components = []
    for i in range(0, len(params_df.index)):
        param_name = params_df['Name'].iloc[i]
        param_value = float(params_df['Value'].iloc[i])
        param_vars = param_name.split(':')
        formula_string = " * ".join(["("+str(map_dict[x])+")" for x in param_vars])+" * "+str(param_value)
        equation_components.append(formula_string)
    # remove 'gem5 stat '
    equation_components = [x.replace('gem5 stat ','') for x in equation_components] # remove 'gem5 stat '
    equation_components = ['('+x+')' for x in equation_components] # remove 'gem5 stat '
    final_eqn = (args.separator).join(equation_components)
    final_eqn = args.before + final_eqn + args.after
    import re
    final_eqn = re.sub(r"df\['(.+?)'\]", "\g<1>", final_eqn,flags=re.MULTILINE)
    print("FINAL EQUATION: ")
    print(final_eqn)
    with open(args.output_file,'w') as f:
        f.write(final_eqn)
    f.closed
    print("Written equation to: "+args.output_file)
