from database.db_connection import DB_connection
# from pydantic import BaseModel
# from database.agent_db import agent



def calculating_urgency_level(num):
    if num < 10:
        return "LOW"
    elif 10 <=num<18:
        return "MEDIUM"
    elif 18 <= num< 25:
        return "HIGH"
    elif num >= 25 :
        return "CRITICAL"
    else:
        raise ValueError



class MissionDB:
    def __init__(self):
        self.db = DB_connection()
    def create_mission(self,data:dict):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cal_risk_level = data['difficulty']*2+data['importance']
            result_level = calculating_urgency_level(cal_risk_level)
            sql_q = """INSERT INTO missions(title, description , location, difficulty, importance, risk_level) VALUES(%s, %s, %s, %s, %s, %s)"""
            values =  [data['title'],data['description'],data['location'],data['difficulty'],data['importance'],result_level]
            cursor.execute(sql_q,values)
            conn.commit()
            return self.get_mission_by_id(cursor.lastrowid)
        finally:
            cursor.close()
            conn.close()

    def get_all_missions(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM missions")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
            

    def get_mission_by_id(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM missions WHERE id = %s",(id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()


    def assign_mission(self,m_id:int, a_id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("UPDATE missions SET assigned_agent_id = %s ,status = 'ASSIGNED' WHERE id = %s",(a_id,m_id))
            conn.commit()
            return {"message":"updated successfully"}
        finally:
            cursor.close()
            conn.close()

    def update_mission_status(self,id:int,status:str):
        mission_data = self.get_mission_by_id(id)
        print(3)
        if status == "IN_PROGRESS":
            print(4)
            if mission_data.get("status") != "ASSIGNED" :
                print(5)
                return "Cannot start a task that is not in an associated status."
        elif status in ["COMPLETED", "FAILED"]:
            if mission_data.get("status") != "IN_PROGRESS" :
                return "It is not possible to close a mission that was not in progress status."
        elif status == "CANCELLED":
            if mission_data.get("status") not in ["NEW","ASSIGNED"]:
                return "Only missions with status NEW or ASSIGNED can be canceled."
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            print(6)
            cursor.execute("UPDATE missions SET status = %s WHERE id = %s",(status,id))
            print(7)
            conn.commit()
            return {"message":"updated successfully"}
        finally:
            cursor.close()
            conn.close()

    def get_open_missions_by_agent(self,id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM missions WHERE id = %s AND status IN ('ASSIGNED', 'IN_PROGRESS')",(id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()


    def count_all_missions(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM missions")
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()




    def count_by_status(self,status):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM missions WHERE status = %s",(status,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()


    def count_open_missions(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM missions WHERE status IN ('NEW', 'ASSIGNED', 'IN_PROGRESS')")
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()


    def count_critical_missions(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM missions WHERE risk_level = 'CRITICAL'")
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def get_top_agent(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM agents ORDER BY completed_missions DESC LIMIT 1")
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()



mission = MissionDB()