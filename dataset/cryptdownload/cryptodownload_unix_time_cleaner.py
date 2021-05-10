import pandas as pd
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('path')
args = parser.parse_args()


df = pd.read_csv(args.path)
df['unix'] = df['unix'].astype(int)

millisec_unix_df = df[df['unix'] >= 10**12]
millisec_unix_df['time'] = pd.to_datetime(millisec_unix_df['unix'], unit='ms')

sec_unix_df = df[df['unix'] < 10**12]
sec_unix_df['time'] = pd.to_datetime(sec_unix_df['unix'], unit='s')

df = pd.concat([millisec_unix_df, sec_unix_df])
df = df.drop_duplicates(subset='time', keep='first')
df.sort_values('time', ascending=False, inplace=True)
df.drop(columns=['date', 'unix'], inplace=True)
df = df[['time'] + list(df.columns.difference(['time']))]
df.to_csv(args.path, index=False)
