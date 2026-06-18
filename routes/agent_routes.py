from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from database.agent_db import agent
import mysql.connector.errors

class Base_Agent(BaseModel):
    name : str
    specialty : str
    agent_rank : str

class Update_Agent(BaseModel):
    name : str | None = None
    specialty : str | None = None
    is_active: bool | None = None
    completed_missions : int | None = None
    failed_missions : int | None = None
    agent_rank : str | None = None



router = APIRouter()


def check_exists_agent(id):
    data = agent.get_agent_by_id(id)
    if data is None:
        raise HTTPException(404,"Agent does not exist.")



@router.post('',status_code=201)
def create_agent(data:Base_Agent):
    try:
        return agent.create_agent(data.model_dump())
    except mysql.connector.errors.DatabaseError:
        raise HTTPException(400)
       
    


@router.get('')
def get_all_agents():
    return agent.get_all_agents()


@router.get("/{id}")
def get_agent_by_id(id:int):
    check_exists_agent(id)
    return agent.get_agent_by_id(id)
    
    

@router.put("/{id}")
def update_agent(id:int,data_for_update:Update_Agent):
    check_exists_agent(id)
    return agent.update_agent(id,data_for_update)


@router.put('/{id}/deactivate')
def deactivate_agent(id:int):
    check_exists_agent(id)
    return agent.deactivate_agent(id)

@router.get('/{id}/performance')
def get_agent_performance(id:int):
    check_exists_agent(id)
    return agent.get_agent_performance(id)

