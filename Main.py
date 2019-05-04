import sys, os
from InstructionClass import instructions, memory  #importing the instructions and memory
from FunctionalUnit import FunctionalUnit  #importing the FunctionalUnit dictionary
from Scoreboard import Scoreboard  #importing the VerilogLinker


INPUT_FILE = ['ADD  R1, R2, R6',
'ADD  R5, R1, R6',
'ADD  R7, R1, R3',
'ADD  R3, R2, R1',
'ADD  R6 ,R7 ,R8',
'fu memory 1 1',
'fu mult 1 11',
'fu add 1 4',
'fu logical 1 1',
'fu float_add 1 21',
'fu float_mult 1 17'] 


class Parsing:
	def __init__(self, INPUT_FILE):
		self.object = Scoreboard() #Calling the Scoreboard Verilog Module 
		self.INPUT_FILE = INPUT_FILE 

	def fileInput(INPUT_FILE):
		print(list(INPUT_FILE))
		fileInput=INPUT_FILE
		parser = Parsing(INPUT_FILE) 
		for line in fileInput:
			#print(line)
			parser.Input(line)
		return parser.object

	def Input(self, instruction):
		ListItem = instruction.split()
		flag=0
		#print(ListItem)
		if ListItem[0] == 'fu': #If Fu is there then it is a functional unit
			flag=1 #1 for functional units
		else:
			flag=2 #2 for instructions

		if flag==1:
			self.FunctionalUnits(ListItem) #Passing FUs
		elif flag==2:
			self.Instructions(ListItem)#Passing Instructions


	def FunctionalUnits(self, ListItem):
		print("The Functional Units are ")
		print(ListItem)
		fu = ListItem[1] #The second item of the list is used as FU type
		units = int(ListItem[2]) #The third item of the list is used as Number of units
		cycles = int(ListItem[3]) #The fourth item of the list is used as Clock cycles
		for no in range(0, units):
			self.object.fu.append(FunctionalUnit(fu, cycles))

	def Instructions(self, ListItem):
		print("The instructions are ")
		print(ListItem)
		inst = ListItem[0]
		inst_func = instructions[inst] #Arithmetic or Load Store
		tokenized_inst = inst_func(' '.join(ListItem))
		#print(tokenized_inst)
		self.object.instr.append(tokenized_inst)

if __name__ == "__main__":
	object1 = Parsing.fileInput(INPUT_FILE) #Sending input to the parser class
	print("\n \n \n")
	print("\n \n \n")
	while not object1.complete():
		object1.tick()
	print(' Instructions              Issue - Read - Execution - Write Back') #Final Output printing
	for instr in object1.instr:
		print(str(instr))