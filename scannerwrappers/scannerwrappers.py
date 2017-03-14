
import subprocess

class ScannerWraps:

    '''
    The method [rungas] will run the GoASTScanner on the GO files in the path supplied
    '''
    def rungas(self, PATH_TO_CODE_TO_SCAN):
        return False

    '''
    The method [runsafesql] will be used to run safesql on the
    '''

    def runsafesql(self, PATH_TO_CODE_TO_SCAN):

        safesql_success_message = "You're safe from SQL injection! Yay \o/"
        starry_line="***************"
        straight_line="------------------"
        try:
            print("\nINFO:Running [safesql]...")
            safesql_run = subprocess.Popen(["safesql", PATH_TO_CODE_TO_SCAN], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print("INFO: Processing the results...")
            safesql_return_code = safesql_run.wait()
            safesql_result = safesql_run.stdout.read().decode("utf-8")
            if (safesql_return_code == 0):
                if safesql_result.strip() == safesql_success_message:
                    print("{0}\nNO ISSUES DETECTED\n{3}\n[safesql] scan result for GO project, {1}: \n{2}\n{0}".format(starry_line, PATH_TO_CODE_TO_SCAN, safesql_result, straight_line))
                else:
                    print("{0}\nISSUES DETECTED\n{3}\n[safesql] scan result for GO project, {1}: \n{2}\n{0}".format(starry_line, PATH_TO_CODE_TO_SCAN, safesql_result, straight_line))
            else:
                print("ERROR: [safesql] exit with an error code {0} and following message \n{1}".format(safesql_return_code,
                                                                                                          safesql_result))
        except:
            raise


