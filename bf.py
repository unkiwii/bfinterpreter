import sys
from sys import stdout

# stack class
class stack:
	def __init__(self):
		self.stack = list()
	
	def push(self, item):
		self.stack.insert(0, item)
	
	def pop(self):
		try:
			return self.stack.pop(0)
		except:
			raise 'Error! Can\'t pop from an empty stack'
	
	def __len__(self):
		return len(self.stack)

# sizeof(file) function
def sizeof(f):
   f.seek(0)
   c = 0
   s = f.read(1)
   while s:
      if s == '\n':
         c += 1
      c += 1
      s = f.read(1)
   return c   

# getch() function
class Getch(object):
    """Gets a single character from standard input.  
       Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): 
        return self.impl()

class _GetchUnix(object):
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows(object):
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = Getch()

# brainf*ck interpreter
class BF:
	def __init__(self, f):
		self.CODE_LIST = ['+', '-', '.', ',', '<', '>', '[', ']']
		self.STACK_SIZE = 20971520	# 20MB
		self.FILE_SIZE = sizeof(f)
		self.code = self.ParseCode(f)
		self.point = 0
		self.memory = [0 for i in range(0, self.STACK_SIZE)]
		self.bin, self.bout = self.FindBraces(self.code)
		self.ExecuteAll(self.code)

	def ParseCode(self, f):
		f.seek(0)
		code = ''
		for l in f:
			for c in l:
				if c in self.CODE_LIST:
					code += c
		return code         

	def FindBraces(self, code):
		st = stack()
		bin = dict()
		bout = dict()
		s = ''
		for i in range(0, len(code)):
			c = code[i]
			s += c
			if c == '[':
				st.push(i)
			elif c == ']':
				if len(st) > 0:
					xi = st.pop()
					bout[i] = xi
					bin[xi] = i
				else:
					raise '\nBad Braces Balance! at char ' + str(i) + ':\n\n' + s
		return bin, bout		

	def ExecuteAll(self, code):
		ep = 0
		while ep < len(code):
			ep = self.Execute(code[ep], ep)
			ep += 1

	def Execute(self, c, ep):
		if c == '+':
			self.memory[self.point] += 1 
		elif c == '-':
			self.memory[self.point] -= 1
		elif c == '>':
			self.point += 1
		elif c == '<':
			self.point -= 1
		elif c == ',':
			self.memory[self.point] = ord(getch())
		elif c == '.':
			stdout.write(chr(self.memory[self.point]))
		elif c == '[':
			if self.memory[self.point] == 0:
				ep = self.bin[ep]
		elif c == ']':
			if self.memory[self.point] != 0:
				ep = self.bout[ep]
		return ep

if __name__ == '__main__':
	f = open(sys.argv[1])
	e = BF(f)
	f.close()
