#! /usr/bin/python3

import pandas as pd
import argparse
import os.path

parser = argparse.ArgumentParser(description='A simple greeting program')
parser.add_argument('-i', '--input', type=str, default='input.csv', help='input file')
parser.add_argument('-k', '--tmkw', type=str, default='TMKW.csv', help='TMKW.csv file')
parser.add_argument('-s', '--spkw', type=str, default='SPKW.csv', help='SPKW.csv file')
parser.add_argument('-r', '--dryrun', type=bool, default=0, help='dryrun')
args = parser.parse_args()
input = args.input
tmkw = args.tmkw
spkw = args.spkw
dryrun = args.dryrun
path = os.path.dirname(input) 
name = os.path.basename(input) 
extension = os.path.splitext(input)[1]

##debug
print(f'{input}')

# Load the CSV files
pd.set_option ("display.max_rows", None)
pd.set_option('display.max_colwidth', None)
tmkw_df = pd.read_csv(tmkw)  # File with short and long keywords
spkw_df = pd.read_csv(spkw)  # File with SPORT's short and long keywords
# input_df = pd.read_csv(input, encoding='windows-1252')  # File with the Title column
# input_df = pd.read_csv(input, encoding='cp1252')  # File with the Title column
input_df = pd.read_csv(input)  # File with the Title column
# print(input_df["Title"])
# s_dropped = input_df[['Title']].dropna().sort_values(by="Title")
# print(s_dropped)

# print(input_df["Title"][0])
# print(input_df["Title"][14])
# print(input_df["Title"][15])
# print(input_df["Title"][16])

# Sort the keywords by length in descending order
tmkw_df = tmkw_df.sort_values(by='short keyword', key=lambda x: x.str.len(), ascending=False)

# Iterate over each row in the SPKW dataframe to remove sport products
spkw_df = spkw_df.dropna(how='all')
sp_pattern = '|'.join([rf'\b{row["short keyword"]}\b' for i, row in spkw_df.iterrows()])
##debug
loc = input_df[input_df[['Handle', 'Title', 'Tags']].apply(lambda x: x.str.contains(sp_pattern, na=False, case=False)).any(axis=1)]
loc_dropped = loc[['Handle', 'Title', 'Tags']].dropna().sort_values(by="Title")
print('REMOVED')
print(f'{loc_dropped}')
# print(sp_pattern)
##debug
input_df = input_df[~input_df[['Handle', 'Title', 'Tags']].apply(lambda x: x.str.contains(sp_pattern, na=False, case=False)).any(axis=1)]

# Iterate over each row in the TMKW dataframe to replace short keywords with long keywords
tmkw_df = tmkw_df.dropna()
for index, row in tmkw_df.iterrows():
    short_keyword = row['short keyword']
    pattern = rf'\b{short_keyword}\b'
    long_keyword = row['long keyword']    
    input_df['Title'] = input_df['Title'].str.replace(pattern, long_keyword, regex=True, case=False)

# Capitalize the first letter of each word in the 'Title' column
input_df['Title'] = input_df['Title'].str.title()


#iterate input and add first part of a handle as a tag
input_df.loc[input_df['Product Id'].notna(), 'Tags'] = input_df['Tags'].astype(str)+ (input_df['Handle'].astype(str).str.split('-').str[0].apply(lambda x: ","+x if x != "" else ""))
input_df['Tags'] = input_df['Tags'].str.lower()


# unique = set (mstr.splitlines ())
##debug
# s_dropped = input_df[['Handle', 'Title', 'Tags']].dropna().sort_values(by="Title")
res = input_df[['Handle', 'Title']].dropna().sort_values(by="Title")
print('RESULT:')
print(res)
print(res.shape[0])
# tag_dropped = input_df['Tags'].dropna().drop_duplicates().sort_values()
tags = 'crs|pln|planner|pjs|sps|hdjk|hdj|cld|calendar|slws|ear|2d|3d|osbh|hsw|tumb|tumb2|mug|dns|swt|cdg|crcs|scr|flcr|pjm|spjm|jrs|slcs|bjk|caror|car|crm|crmt|awb|pcs|psk|tb|wpz|hoodie|pjk|spj|spv|hpv|sjk|sas|short|knst|sjlg|canvas|drm|hdlj|hdlg|cplg|ttlg|bfj|hw|zaw|jns|jean|dpb|tsbb|ohzs|hzs|flag|tst|wtc|clkk|swk|llap|msb|ltc|cdl|bblk|ljk|ltv|splk|premium|sun|yard|blkt|cts|hlts|fm|hdrs|jumpsuit|mrb|totebag|tote|lpb|bed|jrb|cms|csc|gls|pl|kmn|ff'
new_tags = input_df[~input_df['Tags'].str.contains(tags, case=False, na=False)]
# print('debug:')
# print(input_df[~input_df['Tags'].str.contains('crs|pln|planner|pjs|hdjk|hdj|cld|slws', case=False, na=False)]
print('NEW TAGS:')
print(new_tags[['Handle', 'Tags', 'Title']].dropna().sort_values(by='Handle'))
##debug

# Save the modified DataFrame back to a new CSV file\
if (dryrun != 1):
    input_df.to_csv('modified_'+name, index=False)



###
    

# Iterate over the list
# str_list=("Calendar DC.csv" "clogs DC.csv" "HDJK DC.csv" "pjs_10441163_2024_January_13_11_21_17.csv" "planner DC.csv")
# for s in "${str_list[@]}"
# do 
#   python3 main.py -i /home/chuongnh/Downloads/ideattonghop/DC/old/0115/$s -k /home/chuongnh/Downloads/ideattonghop/DC/TMKW.csv -s /home/chuongnh/Downloads/ideattonghop/DC/SPKW.csv -r 1
# done
