from fastapi import APIRouter
from pydantic import BaseModel
from database.mission_db import mission

class Base_Mission(BaseModel):
    title : str
    description : str
    location : str
    difficulty : int
    importance : int




router = APIRouter()

@router.post('',status_code=201)
def create_mission(data:Base_Mission):
    return mission.create_mission(data)

@router.get("")
def get_all_missions():
    return mission.get_all_missions()

@router.get("/{id}")
def get_mission_by_id(id:int):
    return mission.get_mission_by_id(id)


@router.put("/{id}/assign/{agent_id}")
def assign_mission(id:int,agent_id:int):
    return mission.assign_mission(m_id=id,a_id=agent_id)


@router.put("/{id}/start")
def start_mission(id:int):
    return mission.update_mission_status(id,"IN_PROGRESS")


@router.put("/{id}/complete")
def complete_mission(id:int):
    return mission.update_mission_status(id,"COMPLETED")

@router.put("/{id}/fail")
def fail_mission(id:int):
    return mission.update_mission_status(id,"FAILED")



@router.put("/{id}/cancel")
def cancel_mission(id:int):
    return mission.update_mission_status(id,"CANCELLED")

