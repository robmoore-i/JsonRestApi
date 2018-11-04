import os
import time
import requests
from assertpy import assert_that

QHOME = os.environ["QHOME"]

def start_backend_q():
  # Start with a random seed (S) of 10 for predictable test results.
  os.system(QHOME + "/l32/q backend.q -S 10 &")


def kill_backend_q():
  os.system("pkill -f \"" + QHOME + "/l32/q backend.q\"")


def canIdentifyAndGetSessionToken():
  session = requests.Session()
  res = session.post("http://localhost:8000/identify", json={"username": "Lauren"})
  assert_that(res.status_code).is_equal_to(200)
  assert_that(session.cookies.get_dict()).is_equal_to({"sid": "be86cf166c10a3d5c2ceb85c22adfbff699f40625db6a6dcd89682179665ca404eec1d40464871c0c7fa83a209dc49c4b07d9ded6fa31e34358f58c6736b7ef7"})


def run_test(test_name, test):
  try:
    print("- " + test_name)
    test()
  except AssertionError as e:
    print("fail\n\t" + str(e))


def tests():
  run_test("canIdentifyAndGetSessionToken", canIdentifyAndGetSessionToken)


def main():
    print("=== starting backend ===")
    start_backend_q()
    time.sleep(1)

    print("=== starting tests ===")
    tests()

    print("=== killing backend ===")
    kill_backend_q()

    print("=== finished tests ===")


main()
exit(0)
