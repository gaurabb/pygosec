
import os
import subprocess
from scannerwrappers.scannerwrappers import ScannerWraps
from goinstallchecks.goinstallchecks import GoInstallChecks

CMD = "echo $GOPATH"
PATH_TO_CODE_TO_SCAN = "github.com/testweb"  # ToDo: Move to configuration file or command line input

DICT_SCANNERS = {"safesql": 0, "gas":0}

'''
This function will check if the scanners are installed in the machine
where this wrapper is running.
'''
def ChkInstalledScanners():
    try:
        installed_packages = subprocess.check_output(["/usr/local/bin/go", "list", "..."]).decode("utf-8")
        if not installed_packages:
            print("ERROR: Unable check for installed packages.")
            return False
        else:
            print("INFO:Found installed packages. Checking for the security static analyzers... ")
            # Check for safesql
            for scanner in DICT_SCANNERS:
                print("INFO: Checking for the [{0}] package.".format(scanner))
                if scanner in installed_packages:
                    print("INFO: [{0}] package is available.".format(scanner))
                    DICT_SCANNERS[scanner] = 1
                else:
                    print("WARNING: [{0}] package is not installed.".format(scanner))
            # Check that atleast one scanner is installed
            for scanner in DICT_SCANNERS:
                if DICT_SCANNERS[scanner] == 1:
                    print("INFO: Atleast 1 static analyzer is available.")
                    return True
            return False
    except:
        return False

def main():
    #  Step 1: Check if GO is installed. If not show an error and return
    #  If GO is installed the proceed to next steps
    try:

        if GoInstallChecks.checkGoVersion() is False:
            print("INFO: The script will now exit. Please review the messages above to troubleshoot.")
            return

        # Step 2: Check if GOPATH is set. If not set, print message and return

        if GoInstallChecks.checkForGOPATH() == False:
            print("ERROR: GOPATH environment variable is NOT set and is required.\n The script will exit")
            return

        # Step 3: Check for installed scanner packages
        if not ChkInstalledScanners():
            print("INFO: Some or All of the required scanner packages are not installed. Exit")
            return
        # Step 4: Run the scanners, 1 at a time
        for scanner in DICT_SCANNERS:
            if scanner == "safesql":
                ScannerWraps.runsafesql(PATH_TO_CODE_TO_SCAN)

    except OSError as err:
        if err.errno == os.errno.ENOENT:
            print("ERR:GO is not installed. Install GO and try again.")
        else:
            raise


if __name__ == "__main__":
    main()
