import argparse
import settings
from tester import Tester

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--function", required=True,
                help="function to be called: template, tester")
ap.add_argument("-c", "--checker", required=True,
                help="tester name, syntaxis: 'all' to run all checker,\
                checker:name to run a specific checker.\n\
                Examples: \t- 'all'\n\
                          \t- widget:chart, widget:double-axis\n\
                          \t- widget, dashboard:checks")
ap.add_argument("--checker_prefix", help="Optional, checker prefix,\
     'check' by default", default="check")
args = vars(ap.parse_args())


def check():
    function = args["function"]
    checkers = args["checker"]
    checker_prefix = args["checker_prefix"]
    checkers.replace(" ", "")

    tester = Tester(checkers.split(','), checker_prefix=checker_prefix)
    if function == "tester":
        tester.tester()
    if function == "template":
        tester.create_templates()

def main():
    attempts = 0

    while attempts < 5:
        try:
            print("[INFO] Running check routine, attempt: {}".format(attempts))
            check()
            return True
        except Exception as e:
            print("[ERROR] {}".format(e))
            attempts += 1


if __name__ == '__main__':
    main()
