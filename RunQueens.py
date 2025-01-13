###############################################################################
# RunOptInvDisc
###############################################################################

"""
To run from the Anaconda console:

run RunQueens --in "C:\Projects\Queens\Problems\p001\Input.csv"

"""

"""
iPython
import os
folder = "C:\\Projects\\Queens\\PythonCode"
os.chdir(folder)
os.getcwd()
"""

#==============================================================================
# 	Get command line arguments.
#==============================================================================

import os.path
import sys, getopt
import csv
from datetime import datetime
from shutil import copyfile
import ntpath
import Queens
sys.path.insert(0, "C:\\Projects\\PythonLibrary")
import MyLibrary

numArguments = len(sys.argv)
print ("Number of arguments =", numArguments)
print ("Argument List:", str(sys.argv))
argList 	= sys.argv
fileNameIn	= argList[2]

dirName     = os.path.dirname(fileNameIn)
fileNameOut = dirName + "\\" + "Output.csv"
fileNameTrace = dirName + "\\" + "Trace.txt"
fileNameConfig = dirName + "\\" + "Config.csv"

print("Input file  = ", fileNameIn)
print("Directory   = ", dirName)
print("Output file = ", fileNameOut)
print("Trace file = " , fileNameTrace)
print("Config file = ", fileNameConfig)

# open trace file
# '+' sign means it will create a new file if it does not exist.
try:
    if os.path.exists(fileNameTrace):
        os.remove(fileNameTrace)
    fileObjectTrace = open(fileNameTrace,'a+')
except Exception as e:
    sys.exit("Failed to open file: %s" % (str(e)))    

#==============================================================================
# 	Run the program.
#==============================================================================

if __name__ == '__main__':

    # instantiate an object of class Queens
    queens = Queens.Queens(fileNameIn,fileNameConfig,fileNameOut)

    # run the object queens
    queens.RunProgram(fileObjectTrace) 
    
    # close the trace file
    fileObjectTrace.close()
    
    # destruct the object queens
    print("Calling the destructor")
    del queens
                        
###############################################################################
# End of code
###############################################################################