import numpy as np
import pandas as pd

df_memeber = pd.read_excel('./memberstatus.xlsx')
arr = {'user_id': 123265, 'user_name': 'mjmj', 'chat_id':'lklk', 'forbiden':'doggy'}
new_row = pd.Series(arr, name=len(df_memeber))
new_data = df_memeber.iloc[:]["user_id"]
# df_memeber.insert(1,value=arr)
# print(len(df_memeber.index))
# print(df_memeber.head())
# print(df_memeber.info())
# print(df_memeber.shape)
# print(df_memeber.describe())
df_memeber.insert(1,["user_id", "user_name", "chat_id", "forbiden"], arr)
print(new_data)