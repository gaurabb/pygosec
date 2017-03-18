import sys
import os
import getopt
import subprocess
from scannerwrappers.scannerwrappers import ScannerWraps
from goinstallchecks.goinstallchecks import GoInstallChecks
from installscanners.installscanners import InstallGOScanners

scanners = {
    "safesql": 0,
    "gas": 0
}

go_command = "/usr/local/bin/go"

go_list_pkg_cmd = "list"

install_options = ['y', 'yes']

static_msgs = {
    "unable_to_check_installed_pkgs": "ERROR: Unable check for installed packages.",

    "found_installed_packages": "INFO: Found installed packages. Checking for the security static analyzers... ",

    "unavailable_pkg": "WARNING: [{0}] package is not installed.\n\rINFO: This can be installed from {1}",

    "install_pkg_q": "\nDo you want to install the {0} package? Enter Y to install or any other "
                     "key to continue:"
}


scanner_install_instructions = {
                                "safesql": "https://github.com/stripe/safesql",
                                "gas": "https://github.com/GoASTScanner/gas/"
                                }

''' chkinstalledscanners() will check if the scanners are installed in the machine where this wrapper is running.

'''


def chkinstalledscanners(gopath):

    try:
        installed_packages = subprocess.check_output([go_command, go_list_pkg_cmd, "..."]).decode("utf-8")

        if not installed_packages:
            print(static_msgs["unable_to_check_installed_pkgs"])
            return False
        else:
            print(static_msgs["found_installed_packages"])

            # Check for available scanners
            for scanner in scanners:

                print("INFO: Checking for the [{0}] package.".format(scanner))

                if scanner in installed_packages:

                    print("INFO: [{0}] package is available.".format(scanner))

                    scanners[scanner] = 1

                else:

                    print(static_msgs["unavailable_pkg"].format(scanner, scanner_install_instructions[scanner]))

                    install_scanner = input(static_msgs["install_pkg_q"].format(scanner))

                    if install_scanner in install_options:
                        objInstallGOScanners = InstallGOScanners()
                        print("\nINFO: Installing {0} in gopath: {1}".format(scanner, gopath))
                        scanners[scanner] = objInstallGOScanners.install_scanner(scanner)

            # Confirmation check that at least one scanner is installed
            for scanner in scanners:
                if scanners[scanner] == 1:
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

    path_to_code_to_scan = ""

    objgochecker = GoInstallChecks()
    objgopathchecker = GoInstallChecks()

    # Check for command line arguments, display usage if not provided
    if len(sys.argv[1:]) < 1:
        # Path to code t scan is not provided so display usage and exit
        displayusage()
        return
    elif objgochecker.checkgoversion() is False:
            print("\nERROR: GO installation is not found. GO is required for these scanners to work. \nPlease install GO "
                  "and try again")
            return
    elif objgopathchecker.checkforgopath() is False:
        print("\nERROR: gopath environment variable is NOT set and is required.\nPlease set gopath and try again\n\r")
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
                        print("\nWARNING: Path to code to scan is not provided. The script will exit.\n")
                        return
                    print("\nINFO: Directory to be scanned: {0}".format(a))

                    path_to_code_to_scan = a

            gopath = objgopathchecker.getgopath() # Assign gopath environment variable value to gopath variable
            os.chdir(gopath) # For [GoAStScan] change the CWD to gopath

            # Check for installed scanner packages
            if not chkinstalledscanners(gopath):
                print("INFO: None of the required scanner packages are not installed. Exit")
                return

            # Iterate through installed scanners and run against the code directory
            objscannerwraps = ScannerWraps()
            for scanner in scanners:
                if scanner == "safesql" and scanners[scanner] == 1:
                    objscannerwraps.runsafesql(path_to_code_to_scan)
                elif scanner == "gas" and scanners[scanner] == 1:
                    objscannerwraps.rungas("/src/"+path_to_code_to_scan)
        except getopt.GetoptError as err:
            print("ERROR: Following error processing command line arguments:    [{0}]. The script will exit.\n".format(str(err)))


if __name__ == "__main__":
    main()
