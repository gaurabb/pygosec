import sys
import os
import getopt
import subprocess
from scannerwrappers.scannerwrappers import ScannerWraps
from goinstallchecks.goinstallchecks import GoInstallChecks
from installscanners.installscanners import InstallGOScanners

DICT_SCANNERS = {
    "safesql": 0,
    "gas": 0
}

GO_CMD = "/usr/local/bin/go"

GO_PACKAGE_LIST_CMD = "list"

SCANNER_INSTALLATION_INSTRUCTIONS = {"safesql": "https://github.com/stripe/safesql",
                                     "gas": "https://github.com/GoASTScanner/gas",
                                     "safesql": "github.com/stripe/safesql"
                                     }
INSTALL_OPTIONS = ['y', 'yes']

MESSAGES = {
    "unable_to_check_installed_pkgs": "ERROR: Unable check for installed packages.",

    "found_installed_packages": "INFO:Found installed packages. Checking for the security static analyzers... ",

    "unavailable_pkg": "WARNING: [{0}] package is not installed.\n\rINFO: This can be installed from {1}",

    "install_pkg_q": "\nDo you want to install the {0} package? Enter Y to install or any other "
                     "key to continue:"
}

''' ChkInstalledScanners() will check if the scanners are installed in the machine where this wrapper is running.

'''


def ChkInstalledScanners(GOPATH):


    try:
        installed_packages = subprocess.check_output([GO_CMD, GO_PACKAGE_LIST_CMD, "..."]).decode("utf-8")

        if not installed_packages:
            print(MESSAGES["unable_to_check_installed_pkgs"])
            return False
        else:
            print(MESSAGES["found_installed_packages"])

            # Check for available scanners
            for scanner in DICT_SCANNERS:

                print("INFO: Checking for the [{0}] package.".format(scanner))

                if scanner in installed_packages:

                    print("INFO: [{0}] package is available.".format(scanner))

                    DICT_SCANNERS[scanner] = 1

                else:

                    print(MESSAGES["unavailable_pkg"].format(scanner, SCANNER_INSTALLATION_INSTRUCTIONS[scanner]))

                    install_scanner = input(MESSAGES["install_pkg_q"].format(scanner))

                    if install_scanner in INSTALL_OPTIONS:
                        objInstallGOScanners = InstallGOScanners()
                        print("\nINFO: Installing {0} in GOPATH: {1}".format(scanner, GOPATH))
                        DICT_SCANNERS[scanner] = objInstallGOScanners.install_scanner(scanner)

            # Confirmation check that at least one scanner is installed
            for scanner in DICT_SCANNERS:
                if DICT_SCANNERS[scanner] == 1:
                    print("\nINFO: Atleast 1 static analyzer is available.")
                    return True
            return False
    except Exception as err:
        print("ERROR: Something went wrong:\n{0}".format(str(err)))
        raise


'''
usage(): Displays usage of the pygostaticscanwrapper.py
'''


def displayusage():
    print("GO Static Scan Wrapper in Python")
    print("Usage: gochecker.py -p <path to code to scan> <options>\r\n"
          "Options:\r\n-h=Display help/usage")


def main():

    PATH_TO_CODE_TO_SCAN = ""

    # Check for command line arguments
    if len(sys.argv[1:]) < 1:
        # Path to code t scan is not provided so display usage and exit
        displayusage()
        return
    else:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "p:h")
            for o, a in opts:
                if o == "-h":
                    displayusage()
                    return
                elif o == "-p":
                    if not a:
                        print("\nWARNING: No code files provided to scan. The script will exit.\n\n")
                        return
                    print("\nINFO: Directory that will be scanned: {0}".format(a))
                    PATH_TO_CODE_TO_SCAN = a
                    #PATH_TO_CODE_TO_SCAN = "github.com/testweb"  ## Move to Config
                else:
                    assert False, "ERROR: Unhandled option provided."

            # Step 1: Check if GO is installed. If not show an error and return
            #  If GO is installed the proceed to next steps

            objgochecker = GoInstallChecks()
            if objgochecker.checkGoVersion() is False:
                print("INFO: The script will now exit. Please review the messages above to troubleshoot.")
                return

            # Step 2: Check if GOPATH is set. If not set, print message and return
            objgopathchecker = GoInstallChecks()
            if objgopathchecker.checkForGOPATH() == False:
                print("ERROR: GOPATH environment variable is NOT set and is required.\nThe script will exit\n\r")
                return
            GOPATH = objgopathchecker.getGOPATH()

            # Step 3: Check for installed scanner packages
            if not ChkInstalledScanners(GOPATH):
                print("INFO: None of the required scanner packages are not installed. Exit")
                return

            # Step 4: Run the scanners, 1 at a time
            objscannerwraps = ScannerWraps()
            for scanner in DICT_SCANNERS:
                if scanner == "safesql" and DICT_SCANNERS[scanner] == 1:
                    objscannerwraps.runsafesql(PATH_TO_CODE_TO_SCAN)
                elif scanner == "gas" and DICT_SCANNERS[scanner] == 1:
                    objscannerwraps.rungas(PATH_TO_CODE_TO_SCAN)
        except getopt.GetoptError as err:
            print("ERROR: Error processing command line arguments:\n\t {0}".format(str(err)))


if __name__ == "__main__":
    main()
