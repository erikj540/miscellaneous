# IMPORTS
import os, sys, glob
import os
import glob
import numpy as np
import pandas as pd


def standardize_table_dominicks(df):
    # Function that creates standardized table with item, store, week, price, and demand
    # Args: processed data (e.g., output of dataProcessing)
    # Returns: standardized table, i.e., data frame with rows ITEM/UPC, STORE, WEEK, PRICE, DEMAND

    # Remove OK=0 data
    df = df[df['ok'] == 1]

    # # Set price to be NaN for data for which price=0 and move!=0
    # # self.data.set_value((self.data['price']==0) & (self.data['move']!=0), 'price', np.nan)
    # df.set_value(df['price'] == 0, 'price', np.nan)

    # Treat all price=0 data as bad data
    df = df[df['price'] != 0.0]

    # Check qty!=0
    if df[(df['qty'] == 0)].empty is False:
        raise ZeroDivisionError('There are qty=0 items')

    # Convert stuff to right type
    df['move'] = df['move'].apply(lambda move: float(move))
    df['qty'] = df['qty'].apply(lambda qty: float(qty))

    # Demand is given by MOVE/QTY
    demand = pd.DataFrame({'demand': df['move']/df['qty']})

    # Create standardized dataframe discussed abouve with index {0,1,2,...}
    new_df = pd.DataFrame()
    new_df['item'] = df['upc'].apply(lambda item_id: str(item_id))
    new_df['store'] = df['store'].apply(lambda location: str(location))
    new_df['week'] = df['week'].apply(lambda week: int(week))
    new_df['price'] = df['price'].apply(lambda price: float(price))
    new_df['profit'] = df['profit'].apply(lambda profit: float(profit))
    new_df['demand'] = demand

    return new_df


def cost_calc(df):
    # Demand is given by MOVE/QTY
    # demand = pd.DataFrame({'demand': df['move']/df['qty']})

    sales = df['demand'].multiply(df['price'], fill_value=0.0)

    cost = sales*(1 - df['profit']/100.)

    final_df_row = pd.Series()

    final_df_row['item'] = df.iloc[0]['item']

    statistics = cost.describe()

    for index in statistics.index.values:
        # upper_index = index.upper()
        final_df_row[index] = statistics[index]
        # final_df_row[upper_index] = statistics[index]

    return final_df_row

walk_dir = '/Users/erikjohnson/Documents/Category_Files/'
walk_dir = os.path.abspath(walk_dir)

output_dir = r'/Users/erikjohnson/Google Drive/Dominicks_Stats/Cost_Stats/'
print "Removing files in {}".format(output_dir)
files = glob.glob(output_dir+'*')
for f in files:
    os.remove(f)
# df = pd.DataFrame(columns=('W*.csv File', '# of UPCs having QTY=1',
#                            '# of UPCs having QTY>1','UPCs with QTY>1'))

# list_file_path = os.path.join('/Users/erikjohnson/Documents/recursiveFileTest/','list.txt')
i = 1
for root, subdirs, files in os.walk(walk_dir):
    # if i >= 2:
    #     i += 1
    #     break
    for filename in files:
        if filename[-3:] == 'csv' and filename[0] == 'W':
            print i, filename, "\n"
            i += 1

            print "Reading data\n"
            wfile_df = pd.read_csv(os.path.join(root, filename))
            wfile_df.columns = [str(x).lower() for x in list(wfile_df)]

            print "Standardizing\n"
            wfile_df = standardize_table_dominicks(wfile_df)

            # Group by UPC/item
            print "Grouping\n"
            groups = wfile_df.groupby('item')

            print "Applying on groups\n"
            final_df = groups.apply(cost_calc)

            print "Saving\n"
            final_df = final_df.reset_index(drop=True)

            final_df[['item', 'count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']].to_csv(output_dir+'stats_'+filename, index=False)










