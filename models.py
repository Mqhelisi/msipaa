from sqlalchemy import create_engine, MetaData, Column, Integer, String, Date, Text, Boolean, Float,JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import date, datetime
import numpy as np
from dateutil import relativedelta
import json
engine = create_engine("postgresql+psycopg2://postgres:Mqhe23@localhost/msipa")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
class Worker(Base):

    __tablename__ = 'workers'
    
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    workDate = Column(Date, nullable=False)
    leaveDays = Column(Float, nullable=False)
    leaveHist = Column(JSON, nullable=True)

    

    def __init__(self,name,position,leaveDays,workDate):
        self.name = name
        self.position = position
        self.leaveDays = (relativedelta.relativedelta(date.today(),workDate).months + relativedelta.relativedelta(date.today(),workDate).years*12)*2.5
        self.workDate = workDate
     
        
    def json(self):
        return {
            'id':self.id,
            'name': self.name,
            'position': self.position,
            'leaveDays': self.leaveDays,
            'leaveHist': self.leaveHist,
            'workDate': self.workDate.strftime("%d/%m/%Y"),                 
        }
    
class Work(Base):

    __tablename__ = 'works'
    
    id = Column(Integer, nullable=False, primary_key=True)
    descr = Column(String, nullable=False)
    startDate = Column(Date, nullable=False)
    capacity = Column(Float, nullable=False)
    endDate = Column(Date, nullable=True)
    status = Column(String, nullable=False)
    workers = Column(JSON, nullable=False)

    
    def __init__(self,descr,startDate,capacity,status,workers):
        self.descr = descr
        self.startDate = startDate
        self.capacity = capacity
        self.status = status
        self.workers = workers

    def workSum(self):
        ast3=list()
        for ast in self.workers:
            ast3.append(str(ast['id']) + ' ' + ast['name'] + ': ' +  ast['position'] )
        ast3
        my_list = ast3
        string_list = [str(element) for element in my_list]
        delimiter = ", "
        result_string = delimiter.join(string_list)
        return {
            'id':self.id,
            'descr': self.descr,
            'capacity': self.capacity,
            'status': self.status,
            'workers': result_string,
            'startDate': self.startDate.strftime("%d/%m/%Y"), 
            # 'endDate': self.endDate.strftime("%d/%m/%Y")
        }   
    
    def json(self):
        
        return {
            'id':self.id,
            'descr': self.descr,
            'capacity': self.capacity,
            'status': self.status,
            'workers': json.dumps(self.workers),
            'startDate': self.startDate.strftime("%d/%m/%Y"), 
            # 'endDate': self.endDate.strftime("%d/%m/%Y")
        } 
    
class Leave(Base):

    __tablename__ = 'leaves'
    
    id = Column(Integer, nullable=False, primary_key=True)
    worker = Column(Integer, nullable=False)
    setDate = Column(Date, nullable=False)
    startDate = Column(Date, nullable=False)
    endDate = Column(Date, nullable=False)
    leaveType = Column(String, nullable=False)

    
    def __init__(self,worker,startDate,endDate,setDate,leaveType):
        self.worker = worker
        self.startDate = startDate
        self.endDate = endDate
        self.setDate = setDate
        self.leaveType = leaveType
             
        
    def json(self):
        return {
            'id':self.id,
            'worker': self.worker,
            'leaveType': self.leaveType,
            'setDate': self.setDate.strftime("%d/%m/%Y"), 
            'startDate': self.startDate.strftime("%d/%m/%Y"), 
            'endDate': self.endDate.strftime("%d/%m/%Y")
        } 
        
def add_work(descr,startDate,capacity,status,workers):
#     (self,descr,startDate,capacity,status,workers)
    row = Work(descr,startDate,capacity,status,workers)
#     ("dscrption",date.today(),20,"open",[{"w1":125},{"w2":25},{"w3":125},{"w4":25}])
    session.add(row)
    session.commit()
    session.close()
    return "Work added successfully!"

def check_worker_leave(worker_id, leave_days_taken):
    user = session.get(Worker, worker_id)
    if user:
        if user.leaveDays < leave_days_taken:
            rtt = user.leaveDays

            return False, rtt
        user.leaveDays = user.leaveDays-leave_days_taken
        rtt = user.leaveDays
        session.commit()
        session.close()
        return True, rtt
    else:
        return None, None

def update_worker_leave(workerid,leaveid):
    # update the worker leave history JSON
    user = session.get(Worker, workerid)
    if session.get(Worker, workerid) != None:
        print("found worker")
        user.leaveHist[datetime.now()] = leaveid
        session.commit()
        
        return True    
    print("nots")
    return False

def add_leave(newDt,workerid,startDate,endDate,setDate,leaveType):
    
    row = Leave(workerid,startDate,endDate,setDate,leaveType)
    session.add(row)
    session.commit()
    session.close()
    return "Leave added successfully! Worker ID: " + str(workerid) + " left with " +str(newDt) + " leave days"

    
def add_worker(descr,startDate,capacity,status,workers,leaveHist):
    row = Worker(descr,startDate,capacity,status,workers,leaveHist)
    session.add(row)
    session.commit()
    print("Worker added successfully!")
    session.close()
    
def read_workers():
    asdd = list()
    for i in session.query(Worker).all():
        asdd.append(i.json())
        session.close()

    return asdd

def read_leaves():
    asdd = list()
    for i in session.query(Leave).all():
        asdd.append(i.json())
        session.close()

    return asdd

def read_works():
    asdd = list()
    for i in session.query(Work).all():
        asdd.append(i.workSum())
        session.close()

    return asdd

