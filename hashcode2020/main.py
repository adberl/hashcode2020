"""
a_example
b_read_on
c_incunabula
d_tough_choices
e_so_many_books
f_libraries_of_the_world
"""

INPUT_FILE = "d_tough_choices" + ".txt"

FULL_PATH = "inputs/"+INPUT_FILE

all_data = open(FULL_PATH, 'r').readlines()

class Lib:
	def __init__(self, idx, nr_books, days_proc, books_per_day, books):
		self.nr_books = nr_books
		self.days_proc = days_proc
		self.books_per_day = books_per_day
		self.books = books
		self.idx = idx

firstline = all_data[0].split(' ')
TOTAL_BOOKS = firstline[0]
TOTAL_LIBS = int(firstline[1])
TOTAL_DAYS = int(firstline[2].rstrip())

SCORES = [int(item) for item in all_data[1].rstrip().split(' ')]
#print(TOTAL_BOOKS, TOTAL_LIBS, TOTAL_DAYS)
#print(SCORES)
all_data.pop(0)
all_data.pop(0)
#print(all_data)

id_map = dict()

idx = 0
LIBS = []
books = []
libinfo = []
my_id = 0

for line in all_data:
	if(idx % 2 == 0):
		libinfo = [int(item) for item in line.rstrip().split(' ')]		
	else:
		books = [int(item) for item in line.rstrip().split(' ')]
		LIBS.append( 
			Lib(my_id, libinfo[0], libinfo[1], libinfo[2], books))
		my_id += 1	
	idx += 1
	
for lib in LIBS:
	lib.books.sort(key=lambda x: SCORES[x])

LIBS.sort(key=lambda x: x.days_proc)

my_id = 0
for lib in LIBS:
	id_map[lib.idx] = my_id
	my_id += 1

#print(SCORES)
#print(SCORES[LIBS[1][1][3]])

who_proc = 0
is_proc = -1
v_libs = dict()
current = []

for day in range(TOTAL_DAYS):
	for alib in v_libs : 
		for _ in range(LIBS[alib].books_per_day):
			try:
				v_libs[alib].append(LIBS[id_map[alib]].books.pop())
				#print(alib, id_map[alib])
				#print(v_libs)
				#print(LIBS[alib].proc)
			except:
				break
	if(is_proc <= 0):
		if(who_proc < TOTAL_LIBS):	
			#current = LIBS.pop(0)	
			v_libs[LIBS[who_proc].idx] = []
			is_proc = LIBS[who_proc].days_proc
			who_proc += 1
	is_proc -= 1
	#day += 1

#print(v_libs)
		
final = open(INPUT_FILE+"_output.txt", 'w')
final.write(str(len(v_libs)) + '\n')
#print(str(len(v_libs)))
for key, value in v_libs.items():
	final.write(str(key) + ' ' + str(len(value)) + '\n')
	for book in value:
		print(book, end=' ', file=final)
	final.write('\n')



