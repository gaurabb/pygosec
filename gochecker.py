
import sys
import getopt
import os
import subprocess
from scannerwrappers.scannerwrappers import ScannerWraps
from goinstallchecks.goinstallchecks import GoInstallChecks

DICT_SCANNERS = {"safesql": 0, "gas":0}
SCANNER_INSTALLATION_INSTRUCTIONS = {"safesql":"https://github.com/stripe/safesql",
                                     "gas":"https://github.com/GoASTScanner/gas"}

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
                    print("WARNING: [{0}] package is not installed.\n\rThis can be installed from {1}"
                          .format(scanner, SCANNER_INSTALLATION_INSTRUCTIONS[scanner]))
            # Check that atleast one scanner is installed
            for scanner in DICT_SCANNERS:
                if DICT_SCANNERS[scanner] == 1:
                    print("INFO: Atleast 1 static analyzer is available.")
                    return True
            return False
    except:
        return False


'''
usage(): Displays usage of the pygostaticscanwrapper.py
'''
def displayusage():
    print("GO Static Scan Wrapper in Python")
    print("Usage: gochecker.py -p <path to code to scan> -gp <custom GO Path> <options>\r\n"
          "Options:\r\n-h=Display help/usage")


def main():
    GOPATH = ""
    # Check for command line arguments
    if len(sys.argv[1:]) < 1:
        # Display usage
        displayusage()
    else:
        try:
            opts, args = getopt.getopt(sys.argv[1:],"p:gp:h")
            for o, a in opts:
                if o == "-h":
                    displayusage()
                elif o == "-p":
                    PATH_TO_CODE_TO_SCAN = a
                elif o == "-gp":
                    GOPATH = a
                else:
                    assert False, "ERROR: Unhandled option detected."

            # Validate that the argument values are valid
            if not PATH_TO_CODE_TO_SCAN:
                PATH_TO_CODE_TO_SCAN = "github.com/testweb" ## MOve to COnfig

            #  Step 1: Check if GO is installed. If not show an error and return
            #  If GO is installed the proceed to next steps
            objgochecker = GoInstallChecks()
            if objgochecker.checkGoVersion() is False:
                print("INFO: The script will now exit. Please review the messages above to troubleshoot.")
                return

            # Step 2: Check if GOPATH is set. If not set, print message and return
            objgopathchecker = GoInstallChecks()
            if GOPATH == "" and objgopathchecker.checkForGOPATH() == False:
                print("ERROR: GOPATH environment variable is NOT set and is required.\nThe script will exit\n\r")
                return

            # Step 3: Check for installed scanner packages
            if not ChkInstalledScanners():
                print("INFO: None of the required scanner packages are not installed. Exit")
                return

            # Step 4: Run the scanners, 1 at a time
            objscannerwraps = ScannerWraps()
            for scanner in DICT_SCANNERS:
                if scanner == "safesql" and DICT_SCANNERS[scanner]==1:
                    objscannerwraps.runsafesql(PATH_TO_CODE_TO_SCAN)
                elif scanner == "gas" and DICT_SCANNERS[scanner]==1:
                    print("Run GAS")
        except getopt.GetoptError as err:
            print("ERROR: Error processing command line arguments:\n\t {0}".format(str(err)))


if __name__ == "__main__":
    main()
