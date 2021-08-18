import pandas as pd

data = []

columns = ('COUNTRY', 'POP', 'AREA', 'GDP', 'CONT', 'IND_DAY')

df = pd.DataFrame(data=data, index=columns).T

df.to_csv('data3.csv')

data2 = [
    {'COUNTRY': 'Zeelandia', 'POP': 0.00, 'AREA': 0.00, 'GDP':0.00,
        'CONT': 'Zeeland', 'IND_DAY': 'today'}
]

df2 = pd.DataFrame(data=data2,index=columns).T
df2.to_csv('data3.csv', mode = 'a', header = False)