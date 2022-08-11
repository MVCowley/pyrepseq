from functools import reduce

import numpy as np
import pandas as pd

aminoacids = 'ACDEFGHIKLMNPQRSTVWY'
_aminoacids_set = set(aminoacids)

def isvalidaa(string):
    "returns true if string is composed only of characters from the standard amino acid alphabet"
    return all(c in _aminoacids_set for c in string)

def multimerge(dfs, on, suffixes=None, **kwargs):
    """Merge multiple dataframes on a common column.

    Provides support for custom suffixes.

    Parameters
    ----------
    on: 'index' or column name
    suffixes: [list-like | None]
        list of suffixes to append to the data
    **kwargs:  keyword arguments passed along to `pd.merge`

    Returns
    -------
    merged dataframe
    """

    merge_kwargs = dict(how='outer')
    merge_kwargs.update(kwargs)
    if suffixes:
        dfs_new = []
        for df, suffix in zip(dfs, suffixes):
            if not on == 'index':
                df = df.set_index(on)
            dfs_new.append(df.add_suffix('_'+suffix))
        return reduce(lambda left, right: pd.merge(left, right,
                                                   right_index=True, left_index=True,
                                                   **merge_kwargs),
                      dfs_new)
    if on == 'index':
        return reduce(lambda left, right: pd.merge(left, right,
                                                   right_index=True, left_index=True,
                                                   **merge_kwargs),
                      dfs)
    return reduce(lambda left, right: pd.merge(left, right, on,
                                               **merge_kwargs), dfs)
