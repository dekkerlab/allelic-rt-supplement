#########
# just a couple of little helper functions
# mostly visualization related
import numpy as np
import pandas as pd

to_uscs = lambda treg: f"{treg[0]}:{treg[1]}-{treg[2]}"

def fillcolor_compartment_style(ycmp, ax, bin_range=None, lw=0.5, level=.0, color_less="blue", color_more="red"):
    """
    fill colors between - compartment style ...
    like, yo like, listen, like, you know, like uhmmmmm,
    color like A-like into like red-like, and B-like in
    bluish like you know
    you got the jigitist you know like right yo ?!
    """
    if bin_range is None:
        y = ycmp
        y_size = len(y)
        x = np.arange(y_size)
        y0 = np.zeros_like(x) + level
    else:
        y = ycmp[slice(*bin_range)]
        y_size = len(y)
        x = np.arange(*bin_range)
        y0 = np.zeros_like(x) + level
        
    ax.plot(x,y,color="black",linewidth=lw, alpha=0.5,linestyle="solid",markersize=0)
    ax.fill_between(x,y0,y,where=(y<=level),color = color_less)
    ax.fill_between(x,y0,y,where=(y>level),color = color_more)
    
    return 0


def bar_signal(oe,signal,thresh=0.1):
    oe1 = np.nanmean(oe[signal >= thresh])
    oe2 = np.nanmean(oe[(signal >= -thresh)&(signal < thresh)])
    oe3 = np.nanmean(oe[signal < -thresh])
    # return [oe1,oe2,oe3]
    return pd.DataFrame(
        { "set": ["A","AB","B"],
          "OE" : [oe1,oe2,oe3] }
    )


def random_test(oe,comps,iters=100,thresh=0.1,cyclic=False):
    """
    a function that would generate a distribution of OE-averages
    for a number of randomized compartment tracks
    """
    # copy compartments, just in case:
    # although neither permuations not roll are "invasive"- 
    # they do not change input ...
    # they also work with NaNs just fine
    comps_loc = comps.copy()
    n_bins = len(comps_loc)
    
    oes_list = []
    
    if cyclic:
        # just shift compartments instead of permuting
        # and recalculate average Obs/Exp for different compartments
        for i in range(n_bins):
            comps_rnd = np.roll( comps_loc, shift=i )
            oes = bar_signal(oe,comps_rnd,thresh=thresh)
            oes_list.append(oes)
    else:
        # permute compartments with all the maskings etc
        # and recalculate average Obs/Exp for different compartments
        for i in range(iters):
            comps_rnd = np.random.permutation( comps_loc )
            oes = bar_signal(oe,comps_rnd,thresh=thresh)
            oes_list.append(oes)
    
    return pd.concat(oes_list)
