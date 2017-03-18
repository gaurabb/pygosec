
import subprocess
import os

SCAN_LOG_MESSAGES={
    "safesql_start_message" : "\nINFO: Running [safesql]...",
    "safesql_success_message" : "You're safe from SQL injection! Yay \o/",
    "safe_sql_no_issues" : "INFO: NO ISSUES DETECTED during [safesql] scan for GO project at: {0}",
    "safe_sql_issues_detected" : "\nISSUES DETECTED during [safesql] scan for GO project at: {0}",
    "safe_sql_run_error" : "ERROR: [safesql] exit with an error code {0} and following message \n{1}",
    "gas_start_message" : "\nINFO: Running [GoASTScanner]...",
    "gas_success_message" : "*****Write******",
    "gas_sql_no_issues" : "INFO: NO ISSUES DETECTED during [GoASTScanner] scan for GO project at : {0}",
    "gas_sql_run_error" : "ERROR: [GoASTScanner] exit with an error code {0} and following message \n{1}",
    "gas_sql_issues_detected" : "INFO: ISSUES DETECTED during [GoASTScanner] scan for GO project at : {0}"
}


class ScannerWraps:

    '''The method [rungas] will run the GoASTScanner on the GO files in the path supplied

    '''

    def rungas(self, PATH_TO_CODE_TO_SCAN):


        wd = os.getcwd()  + PATH_TO_CODE_TO_SCAN #"/Users/gaurabb/Desktop/Coding-Projects/GO-Workspace/src/github.com/gaurabb/gocsp"
        os.chdir(wd)

        try:
            print(SCAN_LOG_MESSAGES["gas_start_message"])
            gas_run = subprocess.Popen(["gas", "-fmt=json", "-out=results.json", "./..."],
                                       cwd= os.getcwd(),
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
            print("INFO: Processing the results...")

            gas_return_code = gas_run.wait()
            gas_result = gas_run.stdout.read().decode("utf-8")
            if gas_return_code:
                if gas_result.strip() == SCAN_LOG_MESSAGES["gas_success_message"]:
                    print(SCAN_LOG_MESSAGES["gas_sql_no_issues"].format(PATH_TO_CODE_TO_SCAN))
                else:
                    print(SCAN_LOG_MESSAGES["gas_sql_issues_detected"].format(PATH_TO_CODE_TO_SCAN))
                    print(("INFO: Scan results written to: {0}".format(wd)))
            else:
                print(SCAN_LOG_MESSAGES["gas_sql_run_error"].format(gas_return_code,gas_result))
        except Exception as err:
            raise
            '''print(str(err))
            return False'''



    def runsafesql(self, PATH_TO_CODE_TO_SCAN):

        ''' The method [runsafesql] will be used to run safesql on the code files in PATH_TO_CODE_TO_SCAN

        '''


        try:
            print(SCAN_LOG_MESSAGES["safesql_start_message"])
            safesql_run = subprocess.Popen(["safesql", PATH_TO_CODE_TO_SCAN], stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT)
            print("INFO: Processing the results...")
            safesql_return_code = safesql_run.wait()
            safesql_result = safesql_run.stdout.read().decode("utf-8")
            if (safesql_return_code == 0):
                if safesql_result.strip() == SCAN_LOG_MESSAGES["safesql_success_message"]:
                    print(SCAN_LOG_MESSAGES["safe_sql_no_issues"].format(PATH_TO_CODE_TO_SCAN))
                else:
                    print(SCAN_LOG_MESSAGES["safe_sql_issues_detected"].format(PATH_TO_CODE_TO_SCAN))
            else:
                print(SCAN_LOG_MESSAGES["safe_sql_run_error"].format(
                    safesql_return_code,safesql_result))
        except:
            raise


