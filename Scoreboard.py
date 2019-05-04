import sys, os
from InstructionClass import instructions, memory
from FunctionalUnit import FunctionalUnit

class Scoreboard:

	def __init__(self):
		self.fu = []
		self.instr = []
		self.pc = 0
		self.clock = 1
		self.register_status = {} #Qj Qk

	def complete(self): #If the instruction is complete or not
		execution_complete = True
		remaining_instr = not self.has_remaining_instr()
		# print(self.clock, self.pc, remaining_instr)
		if remaining_instr:
			for f in self.fu:
				if f.busy:
					remaining_instr = False #If one of the instruction is still getting executed
					break
		return execution_complete and remaining_instr

	def has_remaining_instr(self):
		return self.pc < len(self.instr)

	def fu_can_issue(self, fu, inst):
		if inst:
			return not fu.busy and inst.unit == fu.fu_type and not (inst.fi in self.register_status) #busy, waw hazard

		return False

	def issue_to_fu(self, fu, next_instruction):
		fu.issue(next_instruction, self.register_status)
		self.register_status[next_instruction.fi] = fu
		# print(next_instruction.inst, self.register_status)
		next_instruction.issue = self.clock #Clock of the issuance
		fu.inst_pc = self.pc #Current PC

	def fu_can_read(self, fu):
		return fu.busy and fu.rj and fu.rk

	def read_to_fu(self, fu):
		fu.read_operands()
		self.instr[fu.inst_pc].read_ops = self.clock

	def fu_can_exec(self, fu):
		return (not fu.rj and not fu.rk) and fu.issued()

	def exec_by_fu(self, fu):
		fu.execute()
		if fu.clock == 0:
			self.instr[fu.inst_pc].ex_cmplt = self.clock
			thisIntruction = self.instr[fu.inst_pc]
			unitType = thisIntruction.unit
			inst = thisIntruction.inst
			# print(thisIntruction.issue)
			execName = thisIntruction.inst.split()[0] + str(thisIntruction.issue) + '.vvp';
			fileName = thisIntruction.inst.split()[0] + str(thisIntruction.issue) + '.txt';
			if unitType == 'add' :
				if 'ADD' in inst:
					memory[thisIntruction.fi] = memory[thisIntruction.fj] + memory[thisIntruction.fk]
					multiply = os.system('iverilog -o ' + execName + ' -DA=' + str(memory[thisIntruction.fj]) + ' -DB=' + str(memory[thisIntruction.fk]) + ' -Dcin=0 ../16bit_Adder/Adder_tb.v')
					runScript = os.system('./' + execName + '>' + fileName)

				elif 'SUB' in inst:
					memory[thisIntruction.fi] = memory[thisIntruction.fj] - memory[thisIntruction.fk]
				elif 'ADC' in inst:	
					memory[thisIntruction.fi] = memory[thisIntruction.fj] + memory[thisIntruction.fk] + 1;
					multiply = os.system('iverilog -o ' + execName + '-DA=' + str(memory[thisIntruction.fj]) + '-DB' + str(memory[thisIntruction.fk])+ ' -Dcin=1 ../16bit_Adder/Adder_tb.v')
					runScript = os.system('./' + execName + '>' + fileName)

			elif unitType == 'mult':
				memory[thisIntruction.fi] = memory[thisIntruction.fj] * memory[thisIntruction.fk]
				command = 'iverilog -o ' + execName + ' -DA=' + str(memory[thisIntruction.fj]) +' -DB=' + str(memory[thisIntruction.fk])+ ' -Dcin=1 ../Wallace_tree_mult/Wallace_tb.v'
				multiply = os.system(command)
				runScript = os.system('./' + execName + '>' + fileName)	

			elif unitType == 'logical':
				if 'CMP' in inst:
					memory[thisIntruction.fi] = ~memory[thisIntruction.fk]
					print()
					cmp = os.system('iverilog -o ' + execName + ' -DA=0' + ' -DB=' +str(memory[thisIntruction.fk]) + '-Dselect=1 ../Logical/logical_tb.v')
					runScript = os.system('./' + execName + '>' + fileName)

				elif 'AND' in inst: 
					memory[thisIntruction.fi] = memory[thisIntruction.fj] & memory[thisIntruction.fk]
					and1 = os.system('iverilog -o ' + execName + ' -DA=' + str(memory[thisIntruction.fj]) + ' -DB=' + str(memory[thisIntruction.fk]) + '-Dselect=2 ../Logical/logical_tb.v')
					runScript = os.system('./' + execName + '>' +fileName)
			
				elif 'XOR' in inst:
					memory[thisIntruction.fi] = memory[thisIntruction.fj] ^ memory[thisIntruction.fk]
					xor = os.system('iverilog -o '+ execName+ ' -DA=' + str(memory[thisIntruction.fj])+ ' -DB=' + str(memory[thisIntruction.fk]) + ' -Dselect=3 ../Logical/logical_tb.v')
					runScript = os.system('./' + execName + '>' +fileName)
		
				elif 'SHR' in inst:
					memory[thisIntruction.fi] = memory[thisIntruction.fj] >> memory[thisIntruction.fk];
					shr = os.system('iverilog -o '+ execName+ ' -DA='+ str(memory[thisIntruction.fj])+ ' -DB=' + str(memory[thisIntruction.fk]) + '-Dselect=4 ../Logical/logical_tb.v')
					runScript = os.system('./' + execName +'>' +fileName)
							
				elif 'LHR' in inst:
					memory[thisIntruction.fi] = memory[thisIntruction.fj] << memory[thisIntruction.fk];
					lhr = os.system('iverilog -o '+ execName+ ' -DA=' +str(memory[thisIntruction.fj])+ ' -DB=' + str(memory[thisIntruction.fk]) + '-Dselect=5 ../Logical/logical_tb.v')
					runScript = os.system('./' + execName +'>'+ fileName)

			elif unitType == 'memory':
				if 'LDR' in thisIntruction.inst:
					memory[thisIntruction.fi] = memory[thisIntruction.fk];
	
				elif 'STR' in thisIntruction.inst:
					memory[thisIntruction.fk] = memory[thisIntruction.fi];

			elif unitType == 'float_add':
				if 'FADD' in inst:
					list_exponent1 = ''.join(list(bin(int(str(memory[thisIntruction.fj]).split('.')[0])))[2:])
					fje = list_exponent1.rjust(5, '0')
					list_mantissa1 = ''.join(list(bin(int(str(memory[thisIntruction.fj]).split('.')[1])))[2:])
					fjm = list_mantissa1.rjust(10, '0')
					list_exponent2 = ''.join(list(bin(int(str(memory[thisIntruction.fk]).split('.')[0])))[2:])
					fke = list_exponent2.rjust(5, '0')
					list_mantissa2 = ''.join(list(bin(int(str(memory[thisIntruction.fk]).split('.')[1])))[2:])
					fkm = list_mantissa2.rjust(10, '0')
					finalA = '0' + str(fje) + str(fjm) if memory[thisIntruction.fj] > 0 else '1' + str(fje) + str(fjm)
					finalB = '0' + str(fke) + str(fkm) if memory[thisIntruction.fk] > 0 else '1' + str(fke) + str(fkm)
					memory[thisIntruction.fi] = memory[thisIntruction.fj] + memory[thisIntruction.fk]
					fadd = os.system('iverilog -o'+ execName+ ' -DA=' + finalA + ' -DB=' +finalB + ' -DaddOrSub=0 ../Lab3/FPA_tb.v')
					runScript = os.system('./' + execName + '>' + fileName)

				elif 'FSUB' in inst:
					list_exponent1 = ''.join(list(bin(int(str(memory[thisIntruction.fj]).split('.')[0])))[2:])
					fje = list_exponent1.rjust(5, '0')
					list_mantissa1 = ''.join(list(bin(int(str(memory[thisIntruction.fj]).split('.')[1])))[2:])
					fjm = list_mantissa1.rjust(10, '0')
					list_exponent2 = ''.join(list(bin(int(str(memory[thisIntruction.fk]).split('.')[0])))[2:])
					fke = list_exponent2.rjust(5, '0')
					list_mantissa2 = ''.join(list(bin(int(str(memory[thisIntruction.fk]).split('.')[1])))[2:])
					fkm = list_mantissa2.rjust(10, '0')
					finalA = '0' + str(fje) + str(fjm) if memory[thisIntruction.fj] > 0 else '1' + str(fje) + str(fjm)
					finalB = '0' + str(fke) + str(fkm) if memory[thisIntruction.fk] > 0 else '1' + str(fke) + str(fkm)
					memory[thisIntruction.fi] = memory[thisIntruction.fj] + memory[thisIntruction.fk]
					fadd = os.system('iverilog -o'+ execName+ ' -DA=' + finalA + ' -DB=' +finalB + ' -DaddOrSub=1 ../Lab3/FPA_tb.v')
					runScript = os.system('./' + execName + '>' + fileName)

			elif unitType == 'float_mult':
				if 'FMUL' in inst:
					list_exponent1 = ''.join(list(bin(int(str(memory[thisIntruction.fj]).split('.')[0])))[2:])
					fje = list_exponent1.rjust(5, '0')
					list_mantissa1 = ''.join(list(bin(int(str(memory[thisIntruction.fj]).split('.')[1])))[2:])
					fjm = list_mantissa1.rjust(10, '0')
					list_exponent2 = ''.join(list(bin(int(str(memory[thisIntruction.fk]).split('.')[0])))[2:])
					fke = list_exponent2.rjust(5, '0')
					list_mantissa2 = ''.join(list(bin(int(str(memory[thisIntruction.fk]).split('.')[1])))[2:])
					fkm = list_mantissa2.rjust(10, '0')
					finalA = '0' + str(fje) + str(fjm) if memory[thisIntruction.fj] > 0 else '1' + str(fje) + str(fjm)
					finalB = '0' + str(fke) + str(fkm) if memory[thisIntruction.fk] > 0 else '1' + str(fke) + str(fkm)
					memory[thisIntruction.fi] = memory[thisIntruction.fj] + memory[thisIntruction.fk]
					fadd = os.system('iverilog -o'+ execName+ ' -DA=' + finalA + ' -DB=' +finalB + ' ../Lab4/FPM_tb.v')
					runScript = os.system('./' + execName + '>' + fileName)

							
	
	def fu_can_write(self, fu):
		can_write_back = False
		for f in self.fu:
			# Check for WAR before write back
			can_write_back = (f.fj != fu.fi or not f.rj) and (f.fk != fu.fi or not f.rk)
			# print(f.fj, f.fk, not f.rj, not f.rk, fu.fi)
			# print(can_write_back)
			if not can_write_back:
				break
		return can_write_back

	def write_back(self, fu):
		fu.write_back(self.fu)
		self.instr[fu.inst_pc].write_back = self.clock
		del self.register_status[fu.fi]
		fu.clear()
		
	def tick(self):
		for f in self.fu:
			f.lock = False

		next_instruction = self.instr[self.pc] if self.has_remaining_instr() else None

		for fu in self.fu:
			if self.fu_can_issue(fu, next_instruction): # Check for structural hazard and WAW
				self.issue_to_fu(fu, next_instruction)
				self.pc+=1
				fu.lock = True
			elif self.fu_can_read(fu): #check for RAW
				self.read_to_fu(fu)
				fu.lock = True
			elif self.fu_can_exec(fu):
				self.exec_by_fu(fu)
				fu.lock = True
			elif fu.issued():
				fu.lock = True

		for fu in self.fu:
			if not fu.lock and self.fu_can_write(fu): #check for WAR
				self.write_back(fu)

		self.clock += 1