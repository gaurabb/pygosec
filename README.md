# pygostaticscanwrapper
Python wrapper for GO static analyzers

## Description
Create a python wrapper for various GO security static analyzers and 
obtain the results in one place.

Following static analyzers are run:
1. [**safesql**](https://github.com/stripe/safesql)
2. [**GOASTScanner**](https://github.com/GoASTScanner/gas)

### Prerequisites
1. [GO must be installed](https://golang.org/doc/install)
2. [GOPATH Environment variable must be defined](https://github.com/golang/go/wiki/GOPATH) 
3. MAC and Linux machines only

### Install
```
1. git clone git@github.com:gaurabb/pygosec.git
2. CD into the **pygosec** directory
3. gochecker.py -p <path to code to scan> 
```

### Usage
```
Usage: python gochecker.py -p <path to code to scan>
          Options:
            -h=Display help/usage
```

### Example
```
gaurabb$ python3 gochecker.py -p "github.com/testweb"

INFO:Installed GO version: go version go1.6.2 darwin/amd64

INFO: GOPATH is set to: /path/to/GO/Workspace/


INFO: Directory to be scanned: github.com/testweb
INFO: Found installed packages. Checking for the security static analyzers... 
INFO: Checking for the [gas] package.
INFO: [gas] package is available.
INFO: Checking for the [safesql] package.
INFO: [safesql] package is available.

INFO: Atleast 1 static analyzer is available.

INFO: Running [GoASTScanner]...
INFO: Processing the results...
INFO: ISSUES DETECTED during [GoASTScanner] scan for GO project at : /src/github.com/testweb
INFO: Scan results written to: /path/to/GO/Workspace/src/github.com/testweb

INFO: Running [safesql]...
INFO: Processing the results...
INFO: NO ISSUES DETECTED during [safesql] scan for GO project at: github.com/testweb
```

### Notes
* GoASTScanner results are written to a json file in the CWD
* SafeSQL results are shown on the terminal only
