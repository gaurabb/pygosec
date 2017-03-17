# pygostaticscanwrapper
Python wrapper for GO static analyzers

## Description
Create a python wrapper for various GO static analyzers and obtain the 
results in one place.

Following static analyzers will be covered:
1. [**safesql**](https://github.com/stripe/safesql)
2.  [**GOASTScanner**](https://github.com/GoASTScanner/gas)

### Prerequisites
1. [GO must be installed](https://golang.org/doc/install)
2. [GOPATH Environment variable must be defined](https://github.com/golang/go/wiki/GOPATH) 

### Usage
```
Usage: python gochecker.py -p <path to code to scan> <options>
          Options:
            -h=Display help/usage
```

### Example
```
$ python gochecker.py -p /path/to/code/
INFO:Installed GO version: go version go1.6.2 darwin/amd64

INFO: GOPATH is set to: /Projects/GO-Workspace/

INFO:Found installed packages. Checking for the security static analyzers... 
INFO: Checking for the [safesql] package.
INFO: [safesql] package is available.
INFO: Checking for the [gas] package.
WARNING: [gas] package is not installed.
This can be installed from https://github.com/GoASTScanner/gas
INFO: Atleast 1 static analyzer is available.

INFO:Running [safesql]...
INFO: Processing the results...
***************
NO ISSUES DETECTED
------------------
[safesql] scan result for GO project, github.com/testweb: 
You're safe from SQL injection! Yay \o/

***************
```
