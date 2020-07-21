import pandas as pd

def breakdown_cat_distribution(df:pd.DataFrame, cat_columns:list):
    print(f'DatFrame columns breakdown\n' + 20 * '=')
    for col in cat_columns:
        print(f'\nColumn `{col}` distribution')
        tmp = pd.concat([
                df[col].value_counts(normalize=False, dropna=False).apply('{:,}'.format).rename('count'),
                df[col].value_counts(normalize=True, dropna=False).apply('{:.1%}'.format).rename('percentage')
            ], axis=1)
        display(tmp)
