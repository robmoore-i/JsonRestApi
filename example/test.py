import os

import requests
from rest_test import *
from assertpy import assert_that

QHOME = os.environ["QHOME"]

def start_server():
  # Start with a random seed (S) of 10 for predictable test results.
  os.system(QHOME + "/l32/q backend.q -S 10 &")

def stop_server():
  os.system("pkill -f \"" + QHOME + "/l32/q backend.q\"")

@test
def canIdentifyAndGetSessionToken():
  session = requests.Session()
  res = session.post("http://localhost:8000/identify", json={"username": "Lauren"})
  assert_that(res.status_code).is_equal_to(200)
  assert_that(session.cookies.get_dict()).is_equal_to({"sid": "452d90d21321ace85f9453a5c5604b025044067e9453c11103a9401fe4b944dbab9d84407e3ad431aee659d470ba9c445b22c55ba5d1819affaaad2244631de0"})

@test
def identificationFailsIfNotAnExistingUser():
  session = requests.Session()
  res = session.post("http://localhost:8000/identify", json={"username": "Nobody"})
  assert_that(res.status_code).is_equal_to(401)
  assert_that(session.cookies.get_dict()).is_equal_to({})

@test
def canGetEvent():
  session = requests.Session()
  res = session.get("http://localhost:8000/event/get/Kyle")
  assert_that(res.status_code).is_equal_to(200)
  res_json = res.json()
  assert_that(len(res_json)).is_equal_to(1)
  event = res_json[0]
  assert_that(event["timestamp"]).is_equal_to("2018-11-05T09:21:35.000")
  assert_that(event["username"]).is_equal_to("Kyle")
  assert_that(event["description"]).is_equal_to("Started server")

@test
def canCaptureEvent():
  session = requests.Session()
  session.post("http://localhost:8000/identify", json={"username": "Dan"})
  res = session.post("http://localhost:8000/event/capture", json={"description": "Captured an event"})
  assert_that(res.status_code).is_equal_to(200)

@test
def captureEventFailsWithoutSessionToken():
  session = requests.Session()
  res = session.post("http://localhost:8000/event/capture", json={"description": "This should not be caught"})
  assert_that(res.status_code).is_equal_to(401)

main(locals(), start_server, stop_server)
exit(0)
