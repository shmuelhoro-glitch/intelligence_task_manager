from database.db_connection import DB_connection
from pydantic import BaseModel



class Create_Agent(BaseModel):
    name : str
    specialty : str
    agent_rank : str

class Update_Agent(BaseModel):
    name : str | None = None
    specialty : str | None = None
    agent_rank : str | None = None



class AgentDB:
    def __init__(self):
        self.db = DB_connection()
    def create_agent(self,data:dict):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql_q = """INSERT INTO agents(name, specialty, agent_rank) VALUES(%s, %s, %s)"""
            values =  list(data.values())
            cursor.execute(sql_q,values)
            conn.commit()
            return self.get_agent_by_id(cursor.lastrowid)
        finally:
            cursor.close()
            conn.close()


    def get_all_agents(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM agents")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
            
    def get_agent_by_id(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM agents WHERE id = %s",(id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()



    def update_agent(self,id:int,data:Update_Agent):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            dict_data = data.model_dump(exclude_unset=True)
            key_with_change = ", ".join(f"{key} = %s "for key in dict_data)
            values = list(dict_data.values()) + [id]
            sql_q = f"""UPDATE agents SET {key_with_change} WHERE id = %s"""
            cursor.execute(sql_q,values)
            conn.commit()
            if cursor.rowcount > 0 :
                return "updated successfully"
            else:
                return "There is nothing new in what you sent."
        finally:
            cursor.close()
            conn.close()


    def deactivate_agent(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE agents SET is_active = FALSE WHERE id = %s",(id,))
            conn.commit()
            if cursor.rowcount > 0:
                return "Updated successfully"
        finally:
            cursor.close()
            conn.close()


    def increment_completed(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE agents SET completed_missions = completed_missions + 1 WHERE id = %s",(id,))
            conn.commit()
            if cursor.rowcount > 0:
                return "Updated successfully"
        finally:
            cursor.close()
            conn.close()



    def increment_failed(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE agents SET failed_missions = failed_missions + 1 WHERE id = %s",(id,))
            conn.commit()
            if cursor.rowcount > 0:
                return "Updated successfully"
        finally:
            cursor.close()
            conn.close()




    def get_agent_performance(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM agents WHERE id = %s ",(id,))
            data = cursor.fetchone()
            
            completed = int(data["completed_missions"])
            failed = int(data["failed_missions"])
            total = completed+failed
            return {"completed":completed,"failed":failed,"total":total}
            
            
        finally:
            cursor.close()
            conn.close()





    def count_active_agents(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM agents WHERE is_active = TRUE")
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()



# data = {"name":"shmuel","specialty":"general","agent_rank":"Senior"}

agent = AgentDB()
# print(agent.get_all_agents())
# print(agent.get_agent_by_id(1))
















# agent = AgentDB()
