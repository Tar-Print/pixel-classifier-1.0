import pandas as pd

data = [
    {'COUNTRY': 'China', 'POP': 1_398.72, 'AREA': 9_596.96,
        'GDP': 12_234.78, 'CONT': 'Asia'},
    {'COUNTRY': 'India', 'POP': 1_351.16, 'AREA': 3_287.26,
        'GDP': 2_575.67, 'CONT': 'Asia', 'IND_DAY': '1947-08-15'},
    {'COUNTRY': 'US', 'POP': 329.74, 'AREA': 9_833.52,
        'GDP': 19_485.39, 'CONT': 'N.America', 'IND_DAY': '1776-07-04'},
    {'COUNTRY': 'Indonesia', 'POP': 268.07, 'AREA': 1_910.93,
        'GDP': 1_015.54, 'CONT': 'Asia', 'IND_DAY': '1945-08-17'},
    {'COUNTRY': 'Brazil', 'POP': 210.32, 'AREA': 8_515.77,
        'GDP': 2_055.51, 'CONT': 'S.America', 'IND_DAY': '1822-09-07'},
    {'COUNTRY': 'Pakistan', 'POP': 205.71, 'AREA': 881.91,
        'GDP': 302.14, 'CONT': 'Asia', 'IND_DAY': '1947-08-14'},
    {'COUNTRY': 'Nigeria', 'POP': 200.96, 'AREA': 923.77,
        'GDP': 375.77, 'CONT': 'Africa', 'IND_DAY': '1960-10-01'},
    {'COUNTRY': 'Bangladesh', 'POP': 167.09, 'AREA': 147.57,
        'GDP': 245.63, 'CONT': 'Asia', 'IND_DAY': '1971-03-26'},
    {'COUNTRY': 'Russia', 'POP': 146.79, 'AREA': 17_098.25,
        'GDP': 1_530.75, 'IND_DAY': '1992-06-12'},
    {'COUNTRY': 'Mexico', 'POP': 126.58, 'AREA': 1_964.38,
        'GDP': 1_158.23, 'CONT': 'N.America', 'IND_DAY': '1810-09-16'},
    {'COUNTRY': 'Japan', 'POP': 126.22, 'AREA': 377.97,
        'GDP': 4_872.42, 'CONT': 'Asia'},
    {'COUNTRY': 'Germany', 'POP': 83.02, 'AREA': 357.11,
        'GDP': 3_693.20, 'CONT': 'Europe'},
    {'COUNTRY': 'France', 'POP': 67.02, 'AREA': 640.68,
        'GDP': 2_582.49, 'CONT': 'Europe', 'IND_DAY': '1789-07-14'},
    {'COUNTRY': 'UK', 'POP': 66.44, 'AREA': 242.50,
        'GDP': 2_631.23, 'CONT': 'Europe'},
    {'COUNTRY': 'Italy', 'POP': 60.36, 'AREA': 301.34,
        'GDP': 1_943.84, 'CONT': 'Europe'},
    {'COUNTRY': 'Argentina', 'POP': 44.94, 'AREA': 2_780.40,
        'GDP': 637.49, 'CONT': 'S.America', 'IND_DAY': '1816-07-09'},
    {'COUNTRY': 'Algeria', 'POP': 43.38, 'AREA': 2_381.74,
        'GDP': 167.56, 'CONT': 'Africa', 'IND_DAY': '1962-07-05'},
    {'COUNTRY': 'Canada', 'POP': 37.59, 'AREA': 9_984.67,
        'GDP': 1_647.12, 'CONT': 'N.America', 'IND_DAY': '1867-07-01'},
    {'COUNTRY': 'Australia', 'POP': 25.47, 'AREA': 7_692.02,
        'GDP': 1_408.68, 'CONT': 'Oceania'},
    {'COUNTRY': 'Kazakhstan', 'POP': 18.53, 'AREA': 2_724.90,
        'GDP': 159.41, 'CONT': 'Asia', 'IND_DAY': '1991-12-16'}
]

columns = ('COUNTRY', 'POP', 'AREA', 'GDP', 'CONT', 'IND_DAY')

df = pd.DataFrame(data=data, index=columns).T

df.to_csv('data2.csv')

data2 = [
    {'COUNTRY': 'Zeelandia', 'POP': 0.00, 'AREA': 0.00, 'GDP':0.00,
        'CONT': 'Zeeland', 'IND_DAY': 'today'}
]

df2 = pd.DataFrame(data=data2,index=columns).T
df2.to_csv('data2.csv', mode = 'a', header = False)