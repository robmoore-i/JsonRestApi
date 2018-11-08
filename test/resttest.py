import os
import sys
import time

from termcolor import colored

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
