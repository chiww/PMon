```
import redis
import pprint
import json

r = redis.Redis(host='127.0.0.1', db=2)

keys = [
    "celery-task-meta-a8cfcf32-1a32-44e8-8021-a3453003a4a2",
    "celery-task-meta-51026561-8a0a-4394-aaee-e3d04b7608f9",
    "celery-task-meta-f31de87a-b2dd-48c7-9e8c-bbc50b49799e",
    "celery-task-meta-70f8c550-e249-40c6-8091-83f6d7936053",
    "celery-task-meta-20d9656d-7fbf-4e3b-a319-054811502d29",
]

result = r.mget(keys)

"""
['{"status": "SUCCESS", "date_done": "2020-01-23T02:34:12.266167", "task_id": "a8cfcf32-1a32-44e8-8021-a3453003a4a2", "traceback": null, "result": [{"status": "up", "service": {}, "timestamp": 1579746852, "address": "10.0.0.97", "close": [], "open": ["80", "22"]}, {"status": "up", "service": {}, "timestamp": 1579746852, "address": "10.0.0.1", "close": [], "open": ["80"]}, {"status": "up", "service": {}, "timestamp": 1579746852, "address": "10.0.0.102", "close": [], "open": ["22"]}, {"status": "up", "service": {}, "timestamp": 1579746852, "address": "10.0.0.55", "close": [], "open": ["80"]}], "children": []}',
 '{"status": "SUCCESS", "date_done": "2020-01-23T03:16:36.401175", "task_id": "51026561-8a0a-4394-aaee-e3d04b7608f9", "traceback": null, "result": [{"status": "up", "service": {}, "timestamp": 1579749396, "address": "10.0.0.55", "close": [], "open": ["80"]}, {"status": "up", "service": {}, "timestamp": 1579749396, "address": "10.0.0.97", "close": [], "open": ["80", "22"]}, {"status": "up", "service": {}, "timestamp": 1579749396, "address": "10.0.0.1", "close": [], "open": ["80"]}, {"status": "up", "service": {}, "timestamp": 1579749396, "address": "10.0.0.102", "close": [], "open": ["22"]}], "children": []}',
 '{"status": "SUCCESS", "date_done": "2020-01-23T02:37:18.618419", "task_id": "f31de87a-b2dd-48c7-9e8c-bbc50b49799e", "traceback": null, "result": [{"status": "up", "service": {}, "timestamp": 1579747038, "address": "10.0.0.97", "close": [], "open": ["22", "80"]}, {"status": "up", "service": {}, "timestamp": 1579747038, "address": "10.0.0.1", "close": [], "open": ["80"]}, {"status": "up", "service": {}, "timestamp": 1579747038, "address": "10.0.0.55", "close": [], "open": ["80"]}, {"status": "up", "service": {}, "timestamp": 1579747038, "address": "10.0.0.102", "close": [], "open": ["22"]}], "children": []}',
 '{"status": "SUCCESS", "date_done": "2020-01-23T03:32:26.389194", "task_id": "70f8c550-e249-40c6-8091-83f6d7936053", "traceback": null, "result": [{"status": "up", "service": {}, "timestamp": 1579750346, "address": "10.0.0.97", "close": [], "open": ["80", "22"]}, {"status": "up", "service": {}, "timestamp": 1579750346, "address": "10.0.0.1", "close": [], "open": ["80"]}, {"status": "up", "service": {}, "timestamp": 1579750346, "address": "10.0.0.102", "close": [], "open": ["22"]}, {"status": "up", "service": {}, "timestamp": 1579750346, "address": "10.0.0.55", "close": [], "open": ["80"]}], "children": []}',
 '{"status": "SUCCESS", "date_done": "2020-01-23T03:36:02.368637", "task_id": "20d9656d-7fbf-4e3b-a319-054811502d29", "traceback": null, "result": [{"status": "up", "service": {}, "timestamp": 1579750562, "address": "10.0.0.1", "close": [], "open": ["80"]}, {"status": "up", "service": {}, "timestamp": 1579750562, "address": "10.0.0.97", "close": [], "open": ["22", "80"]}, {"status": "up", "service": {}, "timestamp": 1579750562, "address": "10.0.0.102", "close": [], "open": ["22"]}, {"status": "up", "service": {}, "timestamp": 1579750562, "address": "10.0.0.55", "close": [], "open": ["80"]}], "children": []}']
"""


for res in result:
    pprint.pprint(json.loads(res))
```