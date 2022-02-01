# Task API Endpoints

---

**CREATE TASK WITHOUT RULE**

---

**URL** : `task_manager/tasks`

**Method** : `POST/PUT`

**Auth required** : YES

#### Request:

```json
{
    "assigned_to_id":1,
    "created_by_id": 1,
    "name": "Update log sheet1"
    
}
```
**created_by_id**: created by customer id

**assigned_to_id**: assigned to customer id

#### Response:

**Code** : `200 OK`

**Success**

```json
{
    "success": true,
    "msg": "Task has been created/updated!!!"
}
```

<br/>

---

**CREATE TASK WITH RULE**

---

**URL** : `task_manager/tasks`

**Method** : `POST`

**Auth required** : YES

#### Request:

```json
{
    "assigned_to_id":1,
    "created_by_id": 1,
    "name": "fuel greater than 26",
    "rule": {
        "pattern_key": "3vy3vatq5XP8XNhXf",
        "model_name": "VehicleStatus",
        "attributes":{
          "fuel_level": {
            "eq": 26
            }
          },
        "action": "create_task"
    }
}

```
Supported Actions:
* **send_email**
* **store_log**
* **create_task**

Attributes format:
**fuel_level** : ----> column name, if there is a json. use __ notation to access keys under it.
**lt, eq, gt** : (lesser than, equal, greater than)

#### Response:

**Code** : `200 OK`

**Success**

```json
{
    "success": true,
    "msg": "Task has been created/updated!!!"
}
```

<br/>

---

**UPDATE TASK**

---

**URL** : `task_manager/tasks`

**Method** : `PUT`

**Auth required** : YES

#### Request:

```json
{
    "id": 3,
    "assigned_to_id":1,
    "created_by_id": 1,
    "name": "Book the vehicle",
    "status": "complete"
    
}

```
id: send task id to update data (Required to update existing task data)
#### Response:

**Code** : `200 OK`

**Success**

```json
{
    "success": true,
    "msg": "Task has been created/updated!!!"
}
```

---

**GET TASKS OF ASSIGNED/CREATED BY USER**

---

**URL** : `task_manager/tasks/customers?created_by_id=1`

**Method** : `GET`

**Auth required** : YES

#### Request:
created_by_id: customer (owner), who created the task
assigned_to_id: customer (got assigned), to whom task is assigned
(Either one of the values should be provided!!!)

#### Response:

**Code** : `200 OK`

**Success**

```json
{
    "status": true,
    "data": [
        {
            "name": "fuel equal to 70",
            "id": 8,
            "status": "complete",
            "created_by_id": 1,
            "assigned_to_id": 1,
            "created_on": "2021-12-31T20:02:53.603Z"
        },
        {
            "name": "fuel lesser than 65",
            "id": 9,
            "status": "complete",
            "created_by_id": 1,
            "assigned_to_id": 1,
            "created_on": "2021-12-31T20:03:28.680Z"
        },
        {
            "name": "front tire pressure",
            "id": 10,
            "status": "complete",
            "created_by_id": 1,
            "assigned_to_id": 1,
            "created_on": "2021-12-31T20:13:41.565Z"
        },
        {
            "name": "speed check 34",
            "id": 13,
            "status": "complete",
            "created_by_id": 1,
            "assigned_to_id": 1,
            "created_on": "2021-12-31T20:20:59.977Z"
        },
        {
            "name": "speed check 33",
            "id": 16,
            "status": "created",
            "created_by_id": 1,
            "assigned_to_id": 1,
            "created_on": "2021-12-31T20:31:28.796Z"
        }
    ]
}
```


NOTE:
1. If task is created by user with no rule, then status has to be updated through API
2. If task is created by system, due to rule set in task as action **create_task**, then the source task status is updated by system.
3. **attributes structure**
```json
{
  "column_name__(followed by json key if any separated by __)": {
    "operation(lt,eq,gt)": "value"
  }
}
```
4.Task status: created, complete, canceled

```
fleetmanager.model_helpers:create_or_update:23 - update or create >>>>{'name': 'Created by 17', 'status': Task.TaskStatus.CREATED, 'created_by_task_id': 17, 'created_entity': Task.TaskCreator.SYSTEM, 'data_signature': 'Ttb2fDmfoPGC9NJ4KuqqGIqzc+EEU9mjnL1siHFiiRY='}
2021-12-31 20:36:00.060 | INFO     | task_management.task_helpers:trigger_actions:93 - New task 18 got created from 17
2021-12-31 20:36:00.062 | INFO     | task_management.tasks:update_task_rule:28 - Task rule is met and updated. Pattern met: {'gps_position__speed': {'eq': 32}}!!!
```