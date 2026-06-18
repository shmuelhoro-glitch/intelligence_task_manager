from fastapi import APIRouter
from database.agent_db import agent
from database.mission_db import mission


router = APIRouter()


@router.get('/summary')
def get_summary_report():
    dict_summary = {
        "active_agents_count" : agent.count_active_agents()[0],
        "total_missions" : mission.count_all_missions()[0],
        "open_missions" : mission.count_open_missions()[0],
        "completed_missions" : mission.count_by_status("COMPLETED")[0],
        "failed_missions" : mission.count_by_status("FAILED")[0],
        "critical_missions" : mission.count_critical_missions()[0],
    }
    return dict_summary


@router.get('/missions-by-status')
def get_missions_by_status():
    dict_status = {
        "open": mission.count_open_missions()[0],
        "in_progress": mission.count_by_status("IN_PROGRESS")[0],
        "completed" : mission.count_by_status("COMPLETED")[0],
        "failed": mission.count_by_status("FAILED")[0],
        "cancelled" : mission.count_by_status("CANCELLED")[0]
    }
    return dict_status


@router.get('/top-agent')
def get_top_agent():
    return mission.get_top_agent()











