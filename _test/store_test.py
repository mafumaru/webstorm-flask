from sqlalchemy import create_engine

engine = create_engine('mysql+mysqldb://root@localhost:3306/test')