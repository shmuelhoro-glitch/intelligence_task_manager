## Intelligence Task Manager
#
The system is designed to manage intelligence missions. It contains tables of information about agents and missions.

You can add new agents. Get a list of all agents. Or one agent by their id. You can update their fields and the status of completed/failed tasks. You can also see how many active agents there are and what percentage of tasks were completed successfully.

#
You can also add tasks to the system, get the list of all tasks. Or a task by id. Associate a list with an agent. Update the status of a task. See the number of tasks / by status / number of open tasks. You can also get the agent who has the largest number of completed tasks.

#

## File structure

    intelligence-task-manager/
    ├── database/
    │ ├── db_connection.py
    │ ├── agent_db.py
    │ └── mission_db.py
    |── image_for_readme/
    | |── 
    ├── README.md
    ├── requirements.txt
    └── .gitignore

#

## Agents table
![alt text](/image_for_readme/agent_table_image.png)
#

## missions table
![alt text](/image_for_readme/missions_table_image.png)
#


## Explanation of classes and methods

**DB_connection**

This class is responsible for connecting the system to the database. It is also responsible for creating the database and tables at system startup if they do not exist.
#
### The get_connection method
The purpose of the method is to create a connection to the database system if it is not already connected.
#
### The create_database method
Creates the database at system startup if it does not exist.
#
### The create_tables method
Creates both tables at system startup if they do not exist.
#

**AgentDB**

#### Agents class
![alt text](/image_for_readme/agent_db_image.png)

#
**MissionDB**

#### Missions class

![alt text](/image_for_readme/mission_db_image.png)
#

## System rules
![alt text](/image_for_readme/System%20rules_image.png)
#


# Running instructions

``docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 \
 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0``

#

**Database name**
Intelligence_db

#





