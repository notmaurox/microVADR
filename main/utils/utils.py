from random import randint
from sqlalchemy.orm import sessionmaker

def random_id():
   min_ = 100
   max_ = 1000000000
   rand = randint(min_, max_)
   # make sure id doesnt exist in db. 
   # my_engine = create_engine('mysql://root:root@db/main')
   # db_session_maker = sessionmaker(bind=my_engine)
   # db_session = db_session_maker()
   # while db_session.query(VadrRun).filter(run_id == rand).limit(1).first() is not None:
   #    rand = randint(min_, max_)
   db_session_maker = sessionmaker(bind=your_db_engine)
   db_session = db_session_maker()
   while db_session.query(Table).filter(uuid == rand).limit(1).first() is not None:
      rand = randint(min_, max_)

   return rand