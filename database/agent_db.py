from db_connection import DB_connection
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
    def create_agent(self,data:Create_Agent):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            sql_q = """INSERT INTO agents(name, specialty, agent_rank) VALUES(%s, %s, %s)"""
            values = data.model_dump()
            cursor.execute(sql_q,values)
            conn.commit()
            return cursor.lastrowid
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
            dict_data = data.model_dump()
            key_with_change = ", ".join(f"{key} = %s "for key in dict_data)
            values = list(dict_data.values()) + [id]
            sql_q = f"""UPDATE agents SET {key_with_change} WHERE id = %s"""
            cursor.execute(sql_q,values)
            return {"message":"updated successfully"}
        finally:
            cursor.close()
            conn.close()


    def deactivate_agent(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("UPDATE agents SET is_active = FALSE WHERE id = %s",(id,))
            if cursor.rowcount > 0:
                return {"message": "Updated successfully"}
        finally:
            cursor.close()
            conn.close()


   

































agent = AgentDB()
print(agent.create_agent({"name":"shmuel","specialty":"general","agent_rank":"Senior"}))
