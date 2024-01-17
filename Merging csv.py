
import pandas as pd 
import glob 
import os 

# combine all files in directory, names begins with "data"
joined_files = os.path.join("D:/Python/...", "data*.csv") 

# a list of all joined files
joined_list = glob.glob(joined_files) 

# convert joined files to dataframe and save as csv
df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True) 
df.to_csv('D:/Python/merged.csv', index = False, encoding = 'utf-8')


