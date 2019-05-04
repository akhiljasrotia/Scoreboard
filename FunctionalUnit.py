class FunctionalUnit:

	def __init__(self, fu_type, clock):
		self.fu_type = fu_type
		self.clock = clock
		self.default_clock = clock
		self.busy = False
		self.fi = self.fj = self.fk = None
		self.qj = self.qk = None
		self.rj = self.rk = True
		self.lock = False
		self.inst_pc = -1

	def clear(self):
		self.clock = self.default_clock
		self.busy = False
		self.fi = self.fj = self.fk = None
		self.qj = self.qk = None
		self.rj = self.rk = True
		self.inst_pc = -1

	def issue(self, instr, register_status):
		self.busy = True
		self.fi = instr.fi
		self.fj = instr.fj
		self.fk = instr.fk

		if instr.fj in register_status:
			self.qj = register_status[instr.fj]

		if instr.fk in register_status:
			self.qk = register_status[instr.fk]

		self.rj = not self.qj
		self.rk = not self.qk

	def read_operands(self):
		self.rj = False
		self.rk = False

	def issued(self):
		return self.busy and self.clock > 0

	def execute(self): #Down Counter
		self.clock -= 1

	def write_back(self, units):
		for f in units:
			if f.qj == self:
				f.rj = True
				f.qj = None
			if f.qk == self:
				f.rk = True
				f.qk = None