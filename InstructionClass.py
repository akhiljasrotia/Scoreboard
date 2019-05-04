import re

class Instruction:

	def __init__(self, inst, unit, fi, fj, fk):
		self.issue = self.read_ops = self.ex_cmplt = self.write_back = -1
		self.unit = unit
		self.fi = fi
		self.fj = fj 
		self.fk = fk
		self.inst = inst

	def __str__ (self):
		return "%-30s%-10d%-15d%-20d%-15d" % \
			(self.inst, self.issue, self.read_ops, self.ex_cmplt, self.write_back)

def tokenize_instruction(inst):
	tokens = re.split(',| ', inst)
	return list(filter(None, tokens))

def arithmetic(inst):
	instruction_tokens = tokenize_instruction(inst)
	fi = instruction_tokens[1]
	fj = instruction_tokens[2]
	fk = instruction_tokens[3]
	unit_for_instr = units_mapping[instruction_tokens[0]]
	return Instruction(inst, unit_for_instr, fi, fj, fk)

def load_store(inst):
	instruction_tokens = tokenize_instruction(inst)
	fi = instruction_tokens[1]
	fk = re.search ('\((.*)\)', instruction_tokens[2]).group(1)
	unit_for_instr = units_mapping[instruction_tokens[0]]
	return Instruction(inst, unit_for_instr, fi, None, fk)

instructions = {
	'ADD': arithmetic,
	'MUL': arithmetic,
	'SUB': arithmetic,
	'ADC': arithmetic,
	'SBB': arithmetic,
	'FADD': arithmetic,
	'FSUB': arithmetic,
	'FMUL': arithmetic,
	# 'CMP': compliment,
	'AND': arithmetic,
	'XOR': arithmetic,
	'SHR': arithmetic,
	'LHR': arithmetic,
	'LDR': load_store,
	'STR': load_store
}

memory = {
	'R0': 1,
	'R1': 2,
	'R2': 3,
	'R3': 4,
	'R4': 5,
	'R5': 6,
	'R6': 7,
	'R7': 8,
	'R8': 9,
	'R9': 0,
	'R10': 1.00,
	'R11': 1.11,
	'R12': 1.22,
	'R13': 1.33,
	'R14': 1.44,
	'R15': 1.55,


}

units_mapping = {
	'ADD': 'add',
	'MUL': 'mult',
	'SUB': 'add',
	'ADC': 'add',
	'SBB': 'add',
	'FADD': 'float_add',
	'FSUB': 'float_add',
	'FMUL': 'float_mult',
	'AND': 'logical',
	'XOR': 'logical',
	'SHR': 'logical',
	'LHR': 'logical',
	'CMP': 'logical',
	'LDR': 'memory',
	'STR': 'memory'
}