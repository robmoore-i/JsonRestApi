import os
import sys
import time
import requests

from termcolor import colored
from assertpy import assert_that

def test(test_function):
    def test_wrapper():
        test_function()

    test_wrapper.__basename__ = test_function.__name__
    return test_wrapper

QHOME = os.environ["QHOME"]

def start_backend():
  os.system(QHOME + "/l32/q backend.q &")


def stop_backend():
  os.system("pkill -f \"" + QHOME + "/l32/q backend.q\"")


@test
def default_path():
  res = requests.get("http://localhost:8000/")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("Hello there, my favourite browser:  python-requests/2.20.1")


@test
def hello():
  res = requests.get("http://localhost:8000/hello")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("hello")


@test
def json():
  res = requests.get("http://localhost:8000/json")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to({"a":1,"b":2,"c":3})


@test
def goodbye():
  res = requests.post("http://localhost:8000/goodbye", json={"name":"python"})
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("Goodbye now python")


@test
def cookie():
  session = requests.Session()
  res = session.get("http://localhost:8000/cookie")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("Check your cookies!")
  assert_that(session.cookies.get_dict()).is_equal_to({"sid":"s355IonT0k3n"})


@test
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


@test
def path_args():
  res = requests.get("http://localhost:8000/pathargs/one/two")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("pathargs -> one -> two")


@test
def path_args_with_cookies():
  session = requests.Session()
  res = session.get("http://localhost:8000/cookie")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("Check your cookies!")
  assert_that(session.cookies.get_dict()).is_equal_to({"sid":"s355IonT0k3n"})
  res = session.get("http://localhost:8000/pathargs/one/two")
  assert_that(res.status_code).is_equal_to(200)
  assert_that(res.json()).is_equal_to("pathargs -> one -> two")


def get_test_functions(local_values):
    test_functions = []
    local_function_names = [name for name in local_values if local_values[name].__class__.__name__ == "function"]
    for function_name in local_function_names:
        function = local_values[function_name]
        if function.__name__ == "test_wrapper":
            test_functions.append(function)

    return test_functions

def run_test(test):
  print("=== === ===")
  print("Running: " + test.__basename__)
  try:
    test()
    print(colored("- " + test.__basename__ + " - pass", "green"))
    print("=== === ===")
    return True
  except AssertionError as e:
    print(colored(str(e), "red"))
    print(colored("- " + test.__basename__ + " - fail", "red"))
    print("=== === ===")
    return False

usage = "USAGE: " + sys.argv[0] + " [a|r]\na => don't start the server because it's (a)lready running.\nr => (r)un the server."

def run_tests(local_values):
    results = {}
    for test_function in get_test_functions(local_values):
        result = run_test(test_function)
        results[test_function.__basename__] = result

    return results

def print_results(results):
    print("=== results ===\n")
    for test_function_name in results:
        if results[test_function_name]:
            print(colored("- " + test_function_name + " - pass", "green"))
        else:
            print(colored("- " + test_function_name + " - fail", "red"))

    print("")

def main(local_values):
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
    results = run_tests(local_values)
    print_results(results)

    if start_server:
        print("=== killing backend ===")
        stop_backend()

    print("=== finished tests ===")


main(locals())
exit(0)
