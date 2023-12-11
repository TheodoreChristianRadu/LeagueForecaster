import pandas

data = pandas.read_csv('historicList.csv')

n = len(data.index)

data.iloc[:(n // 3), :].to_csv('historicList1.csv', index=False)
data.iloc[(n // 3):(2 * n // 3), :].to_csv('historicList2.csv', index=False)
data.iloc[(2 * n // 3):, :].to_csv('historicList3.csv', index=False)
