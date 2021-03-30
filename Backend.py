from typing import List
import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.sql.functions import count
from starlette.responses import JSONResponse

DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()
job_table = sqlalchemy.Table(
    'job_table', metadata,
    sqlalchemy.Column('job_id', sqlalchemy.String, primary_key=True),
    sqlalchemy.Column('job_name', sqlalchemy.String),
    sqlalchemy.Column('location', sqlalchemy.String),
    sqlalchemy.Column('discription', sqlalchemy.String),
    sqlalchemy.Column('skills', sqlalchemy.String),
)
engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

app = FastAPI()


class all(BaseModel):
    job_id: str
    job_name: str
    location: str
    discription: str
    skills: str


class Insert(BaseModel):
    job_id: str
    job_name: str
    location: str
    discription: str
    skills: str


class Update(BaseModel):
    job_id: str
    job_name: str
    location: str
    discription: str
    skills: str


class Delete(BaseModel):
    job_id: str

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
@app.get("/")
async def home():
    return JSONResponse(content={"message": "Hello"})


@app.get("/select/", response_model=List[all])
async def read_records():
    query = job_table.select()
    return await database.fetch_all(query)


@app.post("/insert/", response_model=all)
async def insert_record(insert: Insert):
    #Check the record is already exist or not
    query1 = select([count(1)]).where((job_table.c.job_id == insert.job_id))
    val = await database.fetch_one(query1)

    if val == (0,):
        query = job_table.insert().values(job_id=insert.job_id, job_name=insert.job_name, location=insert.job_name,
                                          discription=insert.discription, skills=insert.skills)
        last_record_id = await database.execute(query)
        result = JSONResponse(content={"message": "Record inserted"})
    else:
        result = JSONResponse(content={"message": "record already exists"})
    return result


@app.put("/update", response_model=all)
async def update_record(update: Update):
    query1 = select([count(1)]).where((job_table.c.job_id == update.job_id))
    val = await database.fetch_one(query1)

    if val == (0,):
        result = JSONResponse(status_code=200, content={"message": "jod id not found"})
    elif val == (1,):
        #update if the record is present
        query = job_table.update().where(job_table.c.job_id == update.job_id).values(job_name=update.job_name,location=update.job_name,discription=update.discription,skills=update.skills)
        record = await database.execute(query)

        result = JSONResponse(content={"message": "updated"})
    else:
        result = JSONResponse(content={"message": "error"})
    return result


@app.delete("/delete", response_model=Delete)
async def delete_record(delete: Delete):
    #check the job_id is exist or not
    query1 = select([count(1)]).where((job_table.c.job_id == delete.job_id))
    val = await database.fetch_one(query1)

    if val == (0,):
        result = JSONResponse(status_code=200, content={"message": "jod id not found"})
    elif val == (1,):
        #Deleting records
        query = job_table.delete().where(job_table.c.job_id == delete.job_id)
        record = await database.execute(query)
        result = JSONResponse(content={"message": "Record deleted"})
    else:
        result = JSONResponse(content={"message": "error"})
    return result
