from typing import List
import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import select, ForeignKey
from sqlalchemy.sql.functions import count
from starlette.responses import JSONResponse

DATABASE_URL = "sqlite:///./jobdatabases.db"
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()
Job_Table = sqlalchemy.Table(
    'Job_Table', metadata,
    sqlalchemy.Column('job_id', sqlalchemy.String, primary_key=True),
    sqlalchemy.Column('job_name', sqlalchemy.String),
    sqlalchemy.Column('location', sqlalchemy.String),
    sqlalchemy.Column('discription', sqlalchemy.String),
    sqlalchemy.Column('skills', sqlalchemy.String),
)
Job_Application = sqlalchemy.Table(
    'Job_Application', metadata,
    sqlalchemy.Column('first_name', sqlalchemy.String),
    sqlalchemy.Column('last_name', sqlalchemy.String),
    sqlalchemy.Column('job_id', sqlalchemy.String, ForeignKey('Job_Table.job_id')),
    sqlalchemy.Column('email_id', sqlalchemy.String),
    sqlalchemy.Column('it_skills', sqlalchemy.String),
    sqlalchemy.Column('qualification', sqlalchemy.String),
    sqlalchemy.Column('yearofexp', sqlalchemy.String)
)
Candidate_Table = sqlalchemy.Table(
    'Candidate_Table', metadata,
    sqlalchemy.Column('job_id', sqlalchemy.String, ForeignKey('Job_Application.job_id')),
    sqlalchemy.Column('first_name', sqlalchemy.String),
    sqlalchemy.Column('email_id', sqlalchemy.String),
    sqlalchemy.Column('it_skills', sqlalchemy.String),
    sqlalchemy.Column('qualification', sqlalchemy.String),
    sqlalchemy.Column('yearofexp', sqlalchemy.String),
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


class Delete(BaseModel):
    job_id: str


class ApplicantAll(BaseModel):
    job_id: str
    first_name: str
    last_name: str
    email_id: str
    it_skills: str
    qualification: str
    yearofexp: str


class DeleteApplicant(BaseModel):
    first_name: str
    last_name: str


class CandidateAll(BaseModel):
    job_id: str
    first_name: str
    email_id: str
    it_skills: str
    qualification: str
    yearofexp: str


class CandidateSelect(BaseModel):
    id: str


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
    query = Job_Table.select()
    return await database.fetch_all(query)


@app.post("/insert/", response_model=all)
async def insert_record(insert: all):
    # Check the record is already exist or not
    query1 = select([count(1)]).where((Job_Table.c.job_id == insert.job_id))
    val = await database.fetch_one(query1)

    if val == (0,):
        query = Job_Table.insert().values(job_id=insert.job_id, job_name=insert.job_name, location=insert.job_name,
                                          discription=insert.discription, skills=insert.skills)
        last_record_id = await database.execute(query)
        result = JSONResponse(content={"message": "Record inserted"})
    else:
        result = JSONResponse(content={"message": "record already exists"})
    return result


@app.put("/update/", response_model=all)
async def update_record(update: all):
    query1 = select([count(1)]).where((Job_Table.c.job_id == update.job_id))
    val = await database.fetch_one(query1)

    if val == (0,):
        result = JSONResponse(status_code=200, content={"message": "jod id not found"})
    elif val == (1,):
        # update if the record is present
        query = Job_Table.update().where(Job_Table.c.job_id == update.job_id).values(job_name=update.job_name,
                                                                                     location=update.job_name,
                                                                                     discription=update.discription,
                                                                                     skills=update.skills)
        record = await database.execute(query)
        result = JSONResponse(content={"message": "updated"})
    else:
        result = JSONResponse(content={"message": "error"})
    return result

@app.delete("/delete/", response_model=Delete)
async def delete_record(delete: Delete):
    # check the job_id is exist or not
    query1 = select([count(1)]).where((Job_Table.c.job_id == delete.job_id))
    val = await database.fetch_one(query1)

    if val == (0,):
        result = JSONResponse(status_code=200, content={"message": "jod id not found"})
    elif val == (1,):
        # Deleting records
        query = Job_Table.delete().where(Job_Table.c.job_id == delete.job_id)
        record = await database.execute(query)
        result = JSONResponse(content={"message": "Record deleted"})
    else:
        result = JSONResponse(content={"message": "error"})
    return result


@app.get("/select applicant records", response_model=List[ApplicantAll])
async def read_candiate_records():
    query = Job_Application.select()
    return await database.fetch_all(query)


async def add(candidate: ApplicantAll):
    try:
        query1 = Candidate_Table.insert().values(job_id=candidate.job_id, first_name=candidate.first_name,
                                             email_id=candidate.email_id,
                                             it_skills=candidate.it_skills,
                                             qualification=candidate.qualification,
                                             yearofexp=candidate.yearofexp)
        record = await database.execute(query1)
        print("record inserted in candidate's")
    except Exception:
        print(Exception)

@app.post("/insert applicant records", response_model=ApplicantAll)
async def insert_applicant_records(candidate: ApplicantAll):
    global result
    query1 = select([count(1)]).where((Job_Table.c.job_id == candidate.job_id))
    val = await database.fetch_one(query1)
    if val == (0,):
        result = JSONResponse(content={"message": "Invalid Job Id"})
    elif val == (1,):

        query = Job_Application.insert().values(job_id=candidate.job_id, first_name=candidate.first_name,
                                                 last_name=candidate.last_name, email_id=candidate.email_id,
                                                 it_skills=candidate.it_skills, qualification=candidate.qualification,
                                                 yearofexp=candidate.yearofexp)
        record = await database.execute(query)
        try:
            query2= (Candidate_Table.insert().values(job_id=candidate.job_id, first_name=candidate.first_name,
                                            email_id=candidate.email_id,
                                            it_skills=candidate.it_skills,
                                            qualification=candidate.qualification,
                                            yearofexp=candidate.yearofexp))

            record1=await database.execute(query2)
        except Exception as e:
            print(e)
        finally:
            result = JSONResponse(content={"message": "Record inserted"})
        result=JSONResponse(content={"message": "Record inserted"})
    else:
        result = JSONResponse(content={"message": "Error"})

    return result


@app.delete("/delete applicant records", response_model=DeleteApplicant)
async def delete_applicant_record(deletec: DeleteApplicant):
    query1 = select([count(1)]).where(
        (Job_Application.c.first_name == deletec.first_name and Job_Application.c.last_name == deletec.last_name))
    val = await database.fetch_one(query1)

    if val == (0,):
        result = JSONResponse(status_code=200, content={"message": "Record not found"})
    elif val == (1,):
        # Deleting records
        query = Job_Application.delete().where(
            Job_Application.c.first_name == deletec.first_name and Job_Application.c.last_name == deletec.last_name)
        record = await database.execute(query)
        result = JSONResponse(content={"message": "Record deleted"})
    else:
        result = JSONResponse(content={"message": "error"})
    return result

