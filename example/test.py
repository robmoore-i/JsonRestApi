#!/usr/local/bin/python3

import os
import time
import sys
import requests
from assertpy import assert_that

QHOME = os.environ["QHOME"]

def start_backend():
  # Start with a random seed (S) of 10 for predictable test results.
  os.system(QHOME + "/m32/q backend.q -S 10 &")


def stop_backend():
  os.system("pkill -f \"" + QHOME + "/m32/q backend.q\"")


def canIdentifyAndGetSessionToken():
  session = requests.Session()
  res = session.post("http://localhost:8000/identify", json={"username": "Lauren"})
  assert_that(res.status_code).is_equal_to(200)
  assert_that(session.cookies.get_dict()).is_equal_to({"sid": "be86cf166c10a3d5c2ceb85c22adfbff699f40625db6a6dcd89682179665ca404eec1d40464871c0c7fa83a209dc49c4b07d9ded6fa31e34358f58c6736b7ef7"})


def identificationFailsIfNotAnExistingUser():
  session = requests.Session()
  res = session.post("http://localhost:8000/identify", json={"username": "Nobody"})
  assert_that(res.status_code).is_equal_to(401)
  assert_that(session.cookies.get_dict()).is_equal_to({})


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


def canCaptureEvent():
  session = requests.Session()
  session.post("http://localhost:8000/identify", json={"username": "Dan"})
  res = session.post("http://localhost:8000/event/capture", json={"description": "Captured an event"})
  assert_that(res.status_code).is_equal_to(200)


def captureEventFailsWithoutSessionToken():
  session = requests.Session()
  res = session.post("http://localhost:8000/event/capture", json={"description": "This should not be caught"})
  assert_that(res.status_code).is_equal_to(401)


def run_test(test_name, test):
  try:
    print("- " + test_name)
    test()
  except AssertionError as e:
    print("fail\n\t" + str(e))


def tests():
  run_test("canIdentifyAndGetSessionToken", canIdentifyAndGetSessionToken)
  run_test("identificationFailsIfNotAnExistingUser", identificationFailsIfNotAnExistingUser)
  run_test("canGetEvent", canGetEvent)
  run_test("canCaptureEvent", canCaptureEvent)
  run_test("captureEventFailsWithoutSessionToken", captureEventFailsWithoutSessionToken)


usage = "USAGE: ./test.py [a|r]\na => don't start the server because it's (a)lready running.\nr => (r)un the server."

def main():
    print("Running: " + str(sys.argv))

    if len(sys.argv) != 2:
        print(usage)
        exit(1)
    elif sys.argv[1] == "a":  # 'a' is for 'already running'
        start_server = False
    elif sys.argv[1] == "r":  # 'r' is for 'run it yourself'
        start_server = True
    else:
        print(usage)
        exit(1)

    if start_server:
        print("=== starting backend ===")
        start_backend()
        time.sleep(1)

    print("=== starting tests ===")
    tests()

    if start_server:
        print("=== killing backend ===")
        stop_backend()

    print("=== finished tests ===")


main()
exit(0)
