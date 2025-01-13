###############################################################################
# Queens.py
###############################################################################

import sys
import csv
from datetime import datetime
import copy
import math
from ortools.linear_solver import pywraplp
  
abc = ["a","b","c","d","e","f","g","h"]

#==============================================================================
# Class Queens. 
#==============================================================================

class Queens:

	#--------------------------------------------------------------------------
	# Queens: Constructor
	#--------------------------------------------------------------------------

	def __init__(self,fileNameIn,fileNameConfig,fileNameOut):
		self.fileNameIn  = fileNameIn	# (in) input data file name
		self.fileNameConfig = fileNameConfig	# (in) configuration file name          
		self.fileNameOut = fileNameOut	# (in) output file name    
		self.n = 0			            # (in) board size
		self.config = {}                # (in) configuration dictionary        

	#--------------------------------------------------------------------------
	# Queens: Read the Config file Config.csv
    #          e.g. C:\Projects\Queens\Problems\p001\Config.csv
	#--------------------------------------------------------------------------
	
	def ReadConfig(self,traceFile):
		t = str(datetime.now())
		traceFile.write(t + " ReadConfig " + self.fileNameConfig + "\n")
		print(t + " ReadConfig " + self.fileNameConfig)
        
		try:
			fileObject = open(self.fileNameConfig, 'r')
		except Exception as e:
			print("Failed to open file: %s" % (str(e)))
			return False

		csv_reader = csv.reader(fileObject, delimiter = ',', \
        quotechar = '"')
		rowCount = 0
		table = ""

		for row in csv_reader:
			if(row):
				if row[0] in {"Constraint","Criterion","Solver"}:
					table = row[0]
					if table == "Constraint":
						self.config[table] = set()
					elif table == "Criterion":
						self.config[table] = {}
					elif table == "Solver":
						self.config[table] = ""
                    
				elif (table == "Constraint") and (row[1] == "1"):
					self.config[table].add(row[0])
				elif (table == "Criterion") and (row[1] == "1"):
					self.config[table][row[0]] = {}
					self.config[table][row[0]]["Goal"] = row[2]                   
				elif (table == "Solver") and (row[1] == "1"):
					self.config[table] = row[0]
					
				rowCount += 1

		fileObject.close()
		print('...read ' + str(rowCount) + ' lines.')
		traceFile.write("...read " + str(rowCount) + " lines.\n")
        
		return True

	#--------------------------------------------------------------------------
	# Queens: Read the input file Input.csv
    #          e.g. C:\Projects\Queens\Problems\p001\Input.csv
	#--------------------------------------------------------------------------
	
	def ReadInput(self,traceFile):
		t = str(datetime.now())
		traceFile.write(t + " ReadInput " + self.fileNameIn + "\n")
		print(t + " ReadInput " + self.fileNameIn)
        
		try:
			fileObject = open(self.fileNameIn, 'r')
		except Exception as e:
			print("Failed to open file: %s" % (str(e)))
			return False
		skipLine = True			# skip the header of the csv file.

		csv_reader = csv.reader(fileObject, delimiter = ',', \
        quotechar = '"')
		rowCount = 0

		for row in csv_reader:
			if( skipLine == False):
				self.n               = int(row[0])
			else:
				skipLine = False
			rowCount += 1

		fileObject.close() 
		print('...read ' + str(rowCount) + ' lines.')
		traceFile.write("...read " + str(rowCount) + " lines.\n") 
		return True

	#--------------------------------------------------------------------------
	# Queens: Print input data.
	#--------------------------------------------------------------------------

	def PrintInput(self):  
		print("boardSize=", self.n )
            
	#--------------------------------------------------------------------------
	# Queens: Print config data.
	#--------------------------------------------------------------------------

	def PrintConfig(self): 
		print(self.config)
                        
	#--------------------------------------------------------------------------
    # Queens: RunModel. It is a function
 	#--------------------------------------------------------------------------
    
	def RunModel(self,traceFile ): 
    
		traceFile.write("Running Model.\n")  
        
        #----------------------------------------------------------------------     
        # Create the MIP solver.
        #----------------------------------------------------------------------

		solverName = self.config["Solver"]
		print("Solver = ", solverName)        
		solver = pywraplp.Solver.CreateSolver(solverName)
        
        #----------------------------------------------------------------------
        # Create the variables.
        #----------------------------------------------------------------------
        
        # Create binary variables x[k] ~ x[i,j](squares of a board)
		x = [] 
		xInd = {}
		k = 0     
		for i in range(self.n):
			xInd[i] = {}
			for j in range(self.n):
				x.append(solver.IntVar(0,1,'x'))
				xInd[i][j] = k       
				k += 1

        # Create an integer variable - number of queens
		numOfQueens = solver.IntVar(0,self.n * self.n,'numOfQueens')
   
        #----------------------------------------------------------------------
        # Create constraints
        #----------------------------------------------------------------------
        
		cstr = []
 
		for constraint in self.config["Constraint"]:
 
        #----------------------------------------------------------------------
        # No two queens are in the same row
        #----------------------------------------------------------------------
        
			if constraint == "No2QueensInRow":		
				for i in range(self.n):
					cstr.append(solver.Constraint(0,1,'No2QueensInRow'))
					for j in range(self.n):
						k = xInd[i][j]
						cstr[-1].SetCoefficient(x[k],1)
                        
        #----------------------------------------------------------------------
        # No two queens are in the same column
        #----------------------------------------------------------------------
        
			if constraint == "No2QueensInColumn":		
				for j in range(self.n):
					cstr.append(solver.Constraint(0,1,'No2QueensInColumn'))
					for i in range(self.n):
						k = xInd[i][j]
						cstr[-1].SetCoefficient(x[k],1)
 
        #----------------------------------------------------------------------
        # No two queens are in the same top-down diagonal
        #----------------------------------------------------------------------
        
			if constraint == "No2QueensInTopDownDiag":	
				for k in range(1,2*self.n-2):
					cstr.append(solver.Constraint(0,1,'No2QueensTopDownDiag'))
					for i in range(self.n):
						j = k-i
						if(j < self.n) and (j >=0):
							l = xInd[i][j]
							cstr[-1].SetCoefficient(x[l],1)
 
        #----------------------------------------------------------------------
        # No two queens are the same bottom-up diagonal
        #----------------------------------------------------------------------
        
			if constraint == "No2QueensInBottomUpDiag":	
				for k in range(1,2*self.n-2):
					cstr.append(solver.Constraint(0,1,'No2QueensBottomUpDiag'))
					for i in range(self.n):
						j = i-k + self.n - 1
						if(j < self.n) and (j >=0):
							l = xInd[i][j]
							cstr[-1].SetCoefficient(x[l],1)                   

        #----------------------------------------------------------------------
        # Number of queens
        #----------------------------------------------------------------------	
        
			if constraint == "NumOfQueens":
				cstr.append(solver.Constraint(0,0,'NumOfQueens'))
				cstr[-1].SetCoefficient(numOfQueens,-1)
				for i in range(self.n):
					for j in range(self.n):
						k = xInd[i][j]
						cstr[-1].SetCoefficient(x[k],1)
        
        #--------------------------------------------------------------------------
        # Create the objective function
        #--------------------------------------------------------------------------
        
		objective = solver.Objective()
		objective.SetCoefficient(numOfQueens, 1)
		objective.SetMaximization()

        #--------------------------------------------------------------------------
        # Solve the model
        #--------------------------------------------------------------------------
        
		solver.Solve()

		print('Solution:')
		print('Objective value =', objective.Value())
            
        #----------------------------------------------------------------------
        # Output solution
        #----------------------------------------------------------------------

		for i in range(self.n):
			for j in range(self.n):
				k = xInd[i][j]
				if( x[k].solution_value() > 0 ):
					print(i,j)              
                       
		print("NumOfQueens =", numOfQueens.solution_value())
        
        #--------------------------------------------------------------------------
        # Convert solver variables to decision variables
        #--------------------------------------------------------------------------
    
		squares = [] 
		k = 0
		for i in range(self.n):
			for j in range(self.n):
				k = xInd[i][j]
				if x[k].solution_value() == 1:
					if( self.n <= len(abc) ):
						squares.append(abc[j] + "-" + str(i+1))
					else:
						squares.append(str(j+1) + "-" + str(i+1))
		return squares     
        
	#--------------------------------------------------------------------------
	# Queens: WriteSquares
	#--------------------------------------------------------------------------

	def WriteSquares(self,traceFile,squares):

		t = str(datetime.now())
		traceFile.write(t + " WriteSquares " + self.fileNameOut + "\n")
		print(t + " WriteSquares " + self.fileNameOut)

		try:
			fileObject = open(self.fileNameOut, 'w')
		except Exception as e:
			print("Failed to open file: %s" % (str(e)))
			return False

		seq = 1
		for square in squares:
			fileObject.write(str(seq) + "," + square + "\n")
			seq += 1

		fileObject.write("\n")
		fileObject.close()

	#--------------------------------------------------------------------------
	# Queens: RunProgram
	#--------------------------------------------------------------------------

	def RunProgram(self,traceFile):
		self.ReadInput(traceFile)
		self.PrintInput()
		self.ReadConfig(traceFile)        
		self.PrintConfig()        
		squares = self.RunModel(traceFile)      
		self.WriteSquares(traceFile,squares)         

    #--------------------------------------------------------------------------
	# Queens: Destructor
	#--------------------------------------------------------------------------

	def __del__(self):
		print("Destructor called, queens is deleted.")
        
###############################################################################
# End of the code
###############################################################################
