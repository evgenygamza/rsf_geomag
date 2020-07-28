import pandas as pd
from sqlalchemy import create_engine

# taking csv & create df
df = pd.read_csv('ALK_20180900_60pp.csv', skiprows=1, names=['dt', 'H', 'E', 'Z', 'temp'])
print(df.head(10))

# connecting to DB
engine = create_engine('mysql+pymysql://gamza:12344321@crsa.izmiran.ru/rsf_mag', echo=True)

# inserting df into database
df.to_sql('ALK', index=False, con=engine, if_exists='append')
