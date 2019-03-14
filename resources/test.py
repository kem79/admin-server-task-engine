from sqlalchemy import create_engine, insert, select
from sqlalchemy import Table, Column, String, Integer, MetaData

if __name__ == '__main__':
    engine = create_engine('postgres://guest:guest@192.168.99.100:5432/guest')

    metadata = MetaData()

    applications = Table('applications', metadata,
                         Column('id', Integer(), autoincrement="auto", primary_key=True, index=True),
                         Column('name', String(), unique=True))
    metadata.create_all(engine)
    print(engine.table_names())

    stmt = insert(applications).values(name='marc')
    result_proxy = engine.execute(stmt)
    stmt = insert(applications).values(name='lydie')
    result_proxy = engine.execute(stmt)

    print(result_proxy.rowcount)

    stmt = select([applications])
    results = engine.execute(stmt).fetchall()

    for res in results:
        print(res)



