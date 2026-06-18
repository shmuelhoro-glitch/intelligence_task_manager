from database.db_connection import DB_connection



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



    def update_agent(self,id:int,data:dict):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            key_with_change = ", ".join(f"{key} = %s "for key in data)
            values = list(data.values()) + [id]
            sql_q = f"""UPDATE agents SET {key_with_change} WHERE id = %s"""
            cursor.execute(sql_q,values)
            conn.commit()
            if cursor.rowcount > 0 :
                return {"message":"updated successfully"}
            else:
                return {"message":"There is nothing new in what you sent."}
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
                return {"message":"Updated successfully"}
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
                return {"message":"Updated successfully"}
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
                return {"message":"Updated successfully"}
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
            success_rate = (completed/total)*100
            return {"completed":completed,"failed":failed,"total":total,"success_rate":success_rate}
            
            
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




agent = AgentDB()


















