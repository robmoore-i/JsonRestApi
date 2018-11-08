import os
import sys
import time
import requests

from termcolor import colored
from assertpy import assert_that

QHOME = os.environ["QHOME"]

def start_backend():
  os.system(QHOME + "/l32/q backend.q &")


def stop_backend():
  os.system("pkill -f \"" + QHOME + "/l32/q backend.q\"")


def default_path():
  res = requests.get("http://localhost:8000/")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("Hello there, my favourite browser:  python-requests/2.20.0")


def hello():
  res = requests.get("http://localhost:8000/hello")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("hello")


def json():
  res = requests.get("http://localhost:8000/json")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to({"a":1,"b":2,"c":3})


def goodbye():
  res = requests.post("http://localhost:8000/goodbye", json={"name":"python"})
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("Goodbye now python")


def cookie():
  session = requests.Session()
  res = session.get("http://localhost:8000/cookie")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("Check your cookies!")
  assert_that(session.cookies.get_dict()).is_equal_to({"sid":"s355IonT0k3n"})


def cors():
  # The preflight request must pass
  headers = { "access-control-request-method": "GET" , "access-control-request-headers": "Content-Type" }
  options = requests.options("http://localhost:8000/cors", headers=headers)
  assert_that(options.headers["Access-Control-Allow-Origin"]).is_equal_to("http://localhost:3000")
  assert_that(options.headers["Access-Control-Allow-Methods"]).is_equal_to("GET")
  assert_that(options.headers["Access-Control-Allow-Headers"]).is_equal_to("Content-Type")
  assert_that(options.status_code).is_equal_to(200)

  # And also the browser must be assured that the response was intended for them
  get = requests.get("http://localhost:8000/cors")
  assert_that(get.headers["Access-Control-Allow-Origin"]).is_equal_to("http://localhost:3000")
  assert_that(get.status_code).is_equal_to(200)


def path_args():
  res = requests.get("http://localhost:8000/pathargs/one/two")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("pathargs -> one -> two")


def path_args_with_cookies():
  session = requests.Session()
  res = session.get("http://localhost:8000/cookie")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("Check your cookies!")
  assert_that(session.cookies.get_dict()).is_equal_to({"sid":"s355IonT0k3n"})
  res = session.get("http://localhost:8000/pathargs/one/two")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("pathargs -> one -> two")


def run_test(test):
  print("\n")
  print("Running: " + test.__name__)
  print("\n")
  try:
    test()
    print("\n")
    print(colored("- " + test.__name__ + " - pass", "green"))
    print("\n")
    return True
  except AssertionError as e:
    print("\n")
    print(colored(str(e), "red"))
    print("\n")
    print(colored("- " + test.__name__ + " - fail", "red"))
    print("\n")
    return False


def tests():
  run_test(default_path)
  run_test(hello)
  run_test(json)
  run_test(goodbye)
  run_test(cookie)
  run_test(cors)
  run_test(path_args)
  run_test(path_args_with_cookies)

usage = "USAGE: " + sys.argv[0] + " [a|r]\na => don't start the server because it's (a)lready running.\nr => (r)un the server."

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
