import os
import subprocess

CMD = "echo $GOPATH"
PATH_TO_CODE_TO_SCAN = "github.com/testweb"  # ToDo: Move to configuration file or command line input
SAFESQL_SUCCESS_MESSAGE = "You're safe from SQL injection! Yay \o/"
DICT_SCANNERS = {"safesql": 0}

# Step 2: Confirm if GOPATH is set


def ChkForGOPATH():
    try:
        go_path = os.environ["GOPATH"]
        print("INFO:GOPATH is set to: {0}\n".format(go_path))
        return True
    except:
        return False


# Step 3: Check all scanners are available

def ChkInstalledPkgs():
    try:
        installed_packages = subprocess.check_output(["/usr/local/bin/go", "list", "..."]).decode("utf-8")
        if not installed_packages:
            print("ERROR: Cannot check for installed packages.")
            return False
        else:
            print("INFO:Found installed packages.")

        # Check for safesql
        print("\tChecking for the [safesql] package")
        if "safesql" in installed_packages:
            print("\tINFO: safesql package is available")
            DICT_SCANNERS["safesql"] = 1
        else:
            print("\tERR: safesql package is not available. Please run [go get github.com/stripe/safesql] to install")
        return True
    except:
        return False

# Step 4: Run the scanners, 1 at a time

def RunScans():
    try:
        print("\nINFO:Running [safesql]...")
        safesql_run = subprocess.Popen(["safesql", PATH_TO_CODE_TO_SCAN], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print("\tINFO: Processing the results...")
        safesql_return_code = safesql_run.wait()
        safesql_result = safesql_run.stdout.read().decode("utf-8")
        if (safesql_return_code == 0):
            if safesql_result.strip() == SAFESQL_SUCCESS_MESSAGE:
                print("\t***NO ISSUES DETECTED***\n\t[safesql] scan result for GO project, {0}: \n\t\t{1}".format(
                    PATH_TO_CODE_TO_SCAN, safesql_result))
            else:
                print("\t***ISSUES DETECTED***\n\t[safesql] scan result for GO project, {0}: \n\t\t{1}".format(
                    PATH_TO_CODE_TO_SCAN, safesql_result))
        else:
            print("\tERROR: [safesql] exit with an error code {0} and following message \n{1}".format(safesql_return_code,
                                                                                                      safesql_result))
    except:
        raise


def main():
    #  Step 1: Check if GO is installed. If not show an error and return
    #  If GO is installed the proceed to next steps
    try:
        go_version = subprocess.check_output(["/usr/local/bin/go", "version"]).decode("utf-8")
        print("INFO:Installed GO version: {0}".format(go_version))
        if not go_version:
            print("ERROR: Either a valid GO installation in not detected or there was some issue with the available \n installation. The script will exit.")
            return
        # Step 2: Check if GOPATH is set. If not set, print message and return
        if not ChkForGOPATH():
            print("ERROR: GOPATH environment variable is NOT set and is required.\n The script will exit")
            return
        # Step 3: Check for installed scanner packages
        if not ChkInstalledPkgs():
            print("INFO: Some or All of the required scanner packages are not installed. Exit")
            return
        # Step 4: Run the scanners, 1 at a time
    except OSError as err:
        if err.errno == os.errno.ENOENT:
            print("ERR:GO is not installed. Install GO and try again.")
        else:
            raise


if __name__ == "__main__":
    main()
