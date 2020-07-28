import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, DateTime, Float


# connecting to DB
engine = create_engine('mysql+pymysql://gamza:12344321@crsa.izmiran.ru/rsf_mag', echo=True)

meta = MetaData()

BEY = Table('BEY', meta,
            Column('dt', DateTime, primary_key=True),
            Column('H', Float),
            Column('e', Float),
            Column('Z', Float),
            Column('temp', Float)
            )
meta.create_all(engine)
