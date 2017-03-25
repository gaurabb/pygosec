import subprocess
import os

Log_Messages={
    "gopath_resource":"https://github.com/golang/go/wiki/GOPATH",
    "go_installed": "\nINFO:Installed GO version: {0}",
    "unknown_go_installation_error": "ERROR: Either a valid GO installation in not detected or there was some issue "
                                     "with the available installation. The script will now exit.",
    "go_not_installed":"ERROR:GO is not installed. Install GO and try again.",
    "go_installation_error":"ERROR:  Checking for GO version resulted in the following error \n {0}",
    "gopath_value":"INFO: GOPATH is set to: {0}\n",
    "gopath_not_set":"ERROR: GOPATH is not set\n"
    }

class GoInstallChecks:

    def checkgoversion(self):
        '''
        Check the current version of GO installed
        :return True/False:
        '''
        try:
            go_version = subprocess.check_output(["go", "version"]).decode("utf-8")
            print(Log_Messages["go_installed"].format(go_version))
            if not go_version:
                print(Log_Messages["unknown_go_installation_error"])
                return False
        except OSError as err:
            if err.errno == os.errno.ENOENT:
                print(Log_Messages["go_not_installed"])
                return False
        except Exception as e:
            print(Log_Messages["go_installation_error"].format(str(e)))
            return False


    def checkforgopath(self):
        '''
        Check if the GOPATH environment variable is set
        :return True/False:
        '''
        try:
            if "GOPATH" in os.environ:
                go_path = os.environ["GOPATH"]
                print(Log_Messages["gopath_value"].format(go_path))
                return True
            else:
                # Check if the user will want to have the GOPATH set
                # If yes: give the option to type in the GOPATH
                # If not provided, exit
                usr_gopath=str(input("\nPlease enter the GOPATH value: "))
                if not usr_gopath or not os.path.isdir(usr_gopath):
                    print("\nERROR: The input value is not a valid GOPATH.\nINFO: "
                          "Review GOPATH information here: {0}".format(Log_Messages["gopath_resource"]))
                    return False
                else:
                    # Set the GOPATH environment variable
                    os.environ["GOPATH"] = usr_gopath
                    print(Log_Messages["gopath_value"].format(usr_gopath))
                    return True
        except Exception:
            print("\nThe error is an error while checking for GOPATH. Error is:")
            return False


    def getgopath(self):
        try:
            go_path = os.environ["GOPATH"]
            return go_path
        except:
            return Log_Messages["gopath_not_set"]
