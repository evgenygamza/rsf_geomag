import pandas as pd
from sqlalchemy import create_engine


# connecting to DB
engine = create_engine('mysql+pymysql://gamza:12344321@crsa.izmiran.ru/rsf_mag', echo=True)


# taking table & create df
df = pd.read_sql('ALK', con=engine, index_col='dt')
print(df.head(10))


