from pwn import *
import time
import subprocess
from functools import reduce

def send(r, data):
	r.send(data)
	time.sleep(0.1)

def print_red(str):
	print("\033[91m" + str + "\033[0m")

def genbin(binary_name):
	command = f"genbin ~/challenges/playroom/shellcodes/{binary_name}"
	try:
		return bytes.fromhex(subprocess.check_output(command, shell=True, universal_newlines=True))
	except (subprocess.CalledProcessError, ValueError) as e:
		print(f"An exception occurred: {e}")
		exit(-1)

def rop_chain(chain):	
	for i in range(len(chain)):
		chain[i] = p64(chain[i])
	return reduce(lambda x, y: x + y, chain)

# transforms an integer to bytes with the minimum number of bytes possible
def int2bytes(num: int) -> bytes:
	return num.to_bytes((num.bit_length() + 7) // 8, byteorder='little', signed=True if num < 0 else False)).ljust(8, b"\x00")


#I/O functions

context.terminal = ['tmux', 'splitw', '-h']
#context.log_level = "warn"
logging.getLogger('pwnlib.elf').setLevel(logging.ERROR)

# breakpoints
b_main = 0xffff

one_gadget=0x00
if args["ONE_GADGET"]:
	one_gadget = int(args["ONE_GADGET"], 16)

if args["REMOTE"]:
	r = remote()
else:
	r = process()
	if args["GDB"]:
		gdb.attach(r, f"""
		# b *{b_main}
		unset env
		set disable-randomization off
		set debuginfod enabled on
		c
		""")
		input("wait")

#LIBC = ELF("./path")
#LIBC.address = 0xbase
#LIBC.symbols["__symol_name"]

r.interactive()