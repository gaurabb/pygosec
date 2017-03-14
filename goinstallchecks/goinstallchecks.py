import subprocess
import os


class GoInstallChecks:

    def checkGoVersion(self):
        try:
            go_version = subprocess.check_output(["go", "version"]).decode("utf-8")
            print("\nINFO:Installed GO version: {0}".format(go_version))
            if not go_version:
                print("ERROR: Either a valid GO installation in not detected or there was some issue with the available \n "
                      "installation. The script will exit.")
                return False
        except OSError as err:
            if err.errno == os.errno.ENOENT:
                print("ERR:GO is not installed. Install GO and try again.")
                return False
        except Exception as e:
            print("ERROR INFO:  Checking for GO version resulted in the following error \n {0}".format(str(e)))
            return False


    def checkForGOPATH(self):
        try:
            go_path = os.environ["GOPATH"]
            print("INFO: GOPATH is set to: {0}\n".format(go_path))
            return True
        except:
            return False

    def getGOPATH(self):
        try:
            go_path = os.environ["GOPATH"]
            print("INFO: GOPATH is set to: {0}\n".format(go_path))
            return go_path
        except:
            return "Not found!"
