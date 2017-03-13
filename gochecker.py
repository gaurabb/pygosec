
import os
import subprocess

CMD="echo $GOPATH"
PATH_TO_CODE_TO_SCAN = "github.com/testweb" # ToDo: Move to configuration file or command line input
SAFESQL_SUCCESS_MESSAGE = "You're safe from SQL injection! Yay \o/"

#  Step 1: Check if GO is installed. If not show an error and return
try:
    go_version= subprocess.check_output(["/usr/local/bin/go","version"]).decode("utf-8")
    print("INFO:Installed GO version: {0}".format(go_version))
except OSError as err:
    if err.errno == os.errno.ENOENT:
        print("ERR:GO is not installed. Install GO and try again.")
    else:
        raise

# Step 2: Confirm if GOPATH is set

try:
    go_path=os.environ["GOPATH"]
    print("INFO:GOPATH is set to: {0}\n".format(go_path))
except:
    raise

# Step 3: Check all scanners are available
try:
    installed_packages=subprocess.check_output(["/usr/local/bin/go", "list", "..."]).decode("utf-8")
    if not installed_packages:
        print("Cannot check for installed packages.")
    else:
       print("INFO:Found installed packages.")
    # Check for safesql
    print("\tChecking for the [safesql] package")
    if "safesql" in installed_packages:
        print("\tINFO: safesql package is available")
    else:
        print("\tERR: safesql package is not available. Please run [go get github.com/stripe/safesql] to install")
except:
    raise

# Step 4: Run the scanners, 1 at a time
try:
    print("INFO:Running [safesql]...")
    safesql_run=subprocess.Popen(["safesql", PATH_TO_CODE_TO_SCAN], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print("\tINFO: Processing the results...")
    ##safesql_return_code = safesql_run.wait()
    safesql_result = safesql_run.stdout.read().decode("utf-8")
    print("\t[safesql] scan result for GO project, {0}: \n\t\t{1}".format(PATH_TO_CODE_TO_SCAN, safesql_result))
except:
    raise
