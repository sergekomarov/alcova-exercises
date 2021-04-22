import numpy as np
from collections import OrderedDict
import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns


def convert_orderbook(ex,
        n_prices=50, n_orders=40, mid_price=5032):

    """
    Convert price points from the exchange to an orderbook table.

    Args
    ----
    ex: Exchange
        exchange instance
    n_prices: int
        number of price points to show
    n_orders: int
        number of orders to show
    mid_price: int
        center prices around this value

    Returns
    -------
    pandas DataFrame containing orders per price
    """

    min_price = mid_price - n_prices//2
    max_price = mid_price + n_prices//2
    min_ind = min_price - ex.min_price
    max_ind = max_price - ex.min_price

    ob = pd.DataFrame(
            np.zeros((max_price-min_price+1, n_orders)),
            index=np.arange(min_price,max_price+1)
            )

    for ppoint in ex.price_points[min_ind:max_ind+1]:
        if ppoint.orders:
            orders_num = min(n_orders, len(ppoint.orders))
            buy_sell = 2 * (ppoint.price <= (ex.buy_max_ind
                                           + ex.min_price)) - 1
            ob.loc[ppoint.price,:orders_num-1] = buy_sell * pd.DataFrame(
                            list(ppoint.orders.values())
                            )['qty'][:orders_num]
    ob.index = ob.index/100
    return ob[::-1]

def plot_orderbooks(orderbooks, sx=1,sy=1, figscale=1.,
                   titles=None, hm_kwargs={}):

    figscale *= 4.
    _hm_kwargs = hm_kwargs.copy()
    fig,axes = plt.subplots(sy,sx, figsize=(sx*figscale,sy*figscale),
                            sharex=True, sharey=True, squeeze=False)

    for n in range(len(orderbooks)):
        mask = orderbooks[n]==0
        if 'annot' in hm_kwargs:
            if hm_kwargs['annot']:
                _hm_kwargs['annot'] = orderbooks[n].abs()
        ax = sns.heatmap(orderbooks[n], mask=mask, ax=axes[n//sx, n%sx],
                         cmap='coolwarm',
                         center=0, **_hm_kwargs
                         )
        if titles is not None:
            ax.set_title(titles[n], fontsize=12)
        ax.tick_params('y', labelrotation=0)
    return #fig,axes
