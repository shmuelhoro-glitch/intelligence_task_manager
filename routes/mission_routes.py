from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from database.mission_db import mission
from database.agent_db import agent
import mysql.connector.errors
from logs.config_log import logger


class Base_Mission(BaseModel):
    title : str
    description : str
    location : str
    difficulty : int
    importance : int

def check_mission_exists(id):
    if mission.get_mission_by_id(id) is None:
        raise HTTPException(404,"Mission not available")



router = APIRouter()

@router.post('',status_code=201)
def create_mission(data:Base_Mission):
    logger.info("post/missions called")
    try:
        return mission.create_mission(data.model_dump())
    except mysql.connector.errors.DatabaseError:
        raise HTTPException(400)

@router.get("")
def get_all_missions():
    logger.info("get/missions called")
    return mission.get_all_missions()

@router.get("/{id}")
def get_mission_by_id(id:int):
    logger.info("get/missions/id called")
    check_mission_exists(id)
    return mission.get_mission_by_id(id)


@router.put("/{id}/assign/{agent_id}")
def assign_mission(id:int,agent_id:int):
    logger.info("put/missions/id/assign/agent_id called")
    agent_data = agent.get_agent_by_id(agent_id)
    if agent_data is None:
        raise HTTPException(404,"Agent not found")
    mission_data = mission.get_mission_by_id(id)
    if mission_data is None:
        raise HTTPException(404,"Mission not available")
    if not agent_data.get("is_active"):
        raise HTTPException(400,"Agent is not active") 
    if mission_data.get("status") != "NEW":
        raise HTTPException(400,"Mission not available")
    if len(mission.get_open_missions_by_agent(agent_id)) >=3:
        raise HTTPException(400,"Agent has reached maximum missions")
    if mission_data.get("risk_level") == "CRITICAL":
        if agent_data.get("agent_rank") != "Commander":
            raise HTTPException(400,"Only Commander can handle critical missions")
    return mission.assign_mission(id,agent_id)


@router.put("/{id}/start")
def start_mission(id:int):
    logger.info("put/missions/id/start called")
    mission_data = mission.get_mission_by_id(id)
    if mission_data is None:
        raise HTTPException(404,"Mission not available")
    if mission_data.get("status") != "ASSIGNED":
        raise HTTPException(400,"cant change")
    return mission.update_mission_status(id,"IN_PROGRESS")


@router.put("/{id}/complete")
def complete_mission(id:int):
    logger.info("put/missions/id/complete called")
    mission_data = mission.get_mission_by_id(id)
    if mission_data is None:
        raise HTTPException(404,"Mission not available")
    if mission_data.get("status") != "IN_PROGRESS":
        raise HTTPException(400)
    agent.increment_completed(mission_data.get("assigned_agent_id"))
    return mission.update_mission_status(id,"COMPLETED")

@router.put("/{id}/fail")
def fail_mission(id:int):
    logger.info("put/missions/id/fail called")
    data_mission = get_mission_by_id(id)
    if data_mission.get("status") != "IN_PROGRESS":
        raise HTTPException(400,{"message":"Just a task that was in_progress"})
    agent.increment_failed(data_mission.get("assigned_agent_id"))
    return mission.update_mission_status(id,"FAILED")



@router.put("/{id}/cancel")
def cancel_mission(id:int):
    logger.info("put/missions/id/cancel called")
    data_mission = get_mission_by_id(id)
    if data_mission.get("status") not in ["NEW","ASSIGNED"]:
        raise HTTPException(400)
    return mission.update_mission_status(id,"CANCELLED")
    

