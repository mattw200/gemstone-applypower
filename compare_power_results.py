
def mape(actual, predicted):
    #df['c'] = df.apply(lambda x: max(len(x['a']), len(x['b'])), axis=1)
    return ((actual - predicted)/actual).abs()*100.0

def signed_err(actual,predicted):
    return ((actual - predicted)/actual)*100.0

def mase():
    pass

if __name__=='__main__':
    import argparse
    import os
    import pandas as pd
    parser = argparse.ArgumentParser()
    parser.add_argument('--gem5-results',  dest='gem5_results', required=True, \
               help="The gem5 power model results")
    parser.add_argument('--xu3-results', dest='xu3_results', required=True, \
               help="The ODROID XU3 power model results")
    parser.add_argument('--core-mask', dest='core_mask', required=True, \
               help="The core mask, e.g. '4,5,6,7'")
    args=parser.parse_args()
    gem5_df = pd.read_csv(args.gem5_results,sep='\t')
    xu3_df = pd.read_csv(args.xu3_results,sep='\t')
    print "Len of gem5_df = "+str(len(gem5_df.index))
    print "Len of xu3_df = "+str(len(xu3_df.index))
    # filter on core mask
    gem5_df = gem5_df[gem5_df['gem5 stat core mask'] == args.core_mask]
    xu3_df = xu3_df[xu3_df['xu3 stat core mask'] == args.core_mask]
    print("Note: the results must come from applying the same model to the same input data!")
    print("(assumes the rows of both model results represent the same samples!)")
    pmc_cols = [x for x in gem5_df.columns.values.tolist() if x.find('EPH_0x') > -1 and x.find('power model') == -1 and x.find(':') == -1]
    print("Found the following PMC cols in the gem5 results: "+str(pmc_cols))
    for pmc in pmc_cols:
        if pmc not in xu3_df.columns.values.tolist():
            raise ValueError("The pmc column ("+pmc+") was in the gem5 results but not in the xu3 results")
    # split into all events only, model events only, and the power contribution
    # make sure length is the same
    if len(gem5_df.index) != len(xu3_df.index):
        raise ValueError("Length of DFs do not match!")
    '''
    pmc_mape_df = gem5_df[pmc_cols]
    pmc_mape_df.columns = ['gem5 '+x for x in pmc_mape_df.columns.values]
    for pmc in pmc_cols:
        pmc_mape_df['xu3 '+pmc] = xu3_df[pmc]
    print pmc_mape_df
    pmc_mape_df.to_csv('pmc-mape-df.csv',sep='\t')
    '''
    mape_df = gem5_df[['xu3 stat workload name', 'xu3 stat core mask', 'xu3 stat Freq (MHz) C0', 'xu3 stat Freq (MHz) C4']]
    signed_df = gem5_df[['xu3 stat workload name', 'xu3 stat core mask', 'xu3 stat Freq (MHz) C0', 'xu3 stat Freq (MHz) C4']]
    mape_diff_df = gem5_df[['xu3 stat workload name', 'xu3 stat core mask', 'xu3 stat Freq (MHz) C0', 'xu3 stat Freq (MHz) C4']]
    signed_diff_df = gem5_df[['xu3 stat workload name', 'xu3 stat core mask', 'xu3 stat Freq (MHz) C0', 'xu3 stat Freq (MHz) C4']]
    for pmc in pmc_cols:
        mape_df[pmc+' mape'] = mape(xu3_df[pmc], gem5_df[pmc])
        mape_diff_df[pmc+' mape'] = mape(xu3_df[pmc]*xu3_df['xu3 stat duration (s)'], gem5_df[pmc]*gem5_df['gem5 stat sim_seconds'])
        signed_df[pmc+' signed'] = signed_err(xu3_df[pmc], gem5_df[pmc])
        signed_diff_df[pmc+' signed'] = signed_err(xu3_df[pmc]*xu3_df['xu3 stat duration (s)'], gem5_df[pmc]*gem5_df['gem5 stat sim_seconds'])
    print mape_df.mean()
    print signed_df.mean()
    print("Diffs:")
    print mape_diff_df.mean()
    print signed_diff_df.mean()

    # TODO: calculate diff from rates as well 
    # Add other PMCs
    # Find new PMC for A15
    # Make A7 model
