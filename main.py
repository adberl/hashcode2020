INPUT_FILE = "a_example.txt"
FULL_PATH = "inputs/"+INPUT_FILE

all_data = open(FULL_PATH, 'r').readlines()

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

idx = 0
LIBS = []
books = []
libinfo = []


for line in all_data:
	if(idx % 2 == 0):
		libinfo = [int(item) for item in line.rstrip().split(' ')]		
	else:
		books = [int(item) for item in line.rstrip().split(' ')]
		LIBS.append( (libinfo, books) )
	idx += 1

for lib in LIBS:
	lib[1].sort(key=lambda x: SCORES[x])


#print(SCORES)
#print(SCORES[LIBS[1][1][3]])

who_proc = 0
is_proc = -1
v_libs = dict()
current = []

for day in range(TOTAL_DAYS):
	for alib in v_libs : 
		for _ in range(LIBS[alib][0][2]):
			try:
				v_libs[alib].append(LIBS[alib][1].pop())
			except:
				break
	if(is_proc <= 0):
		if(who_proc < TOTAL_LIBS):	
			#current = LIBS.pop(0)	
			v_libs[who_proc] = []
			is_proc = LIBS[who_proc][0][1]
			who_proc += 1
	is_proc -= 1

#print(v_libs)
		
final = open(INPUT_FILE+"_output.txt", 'w')
final.write(str(len(v_libs)) + '\n')
#print(str(len(v_libs)))
for key, value in v_libs.items():
	final.write(str(key) + ' ' + str(len(value)) + '\n')
	for book in value:
		print(book, end=' ', file=final)
	final.write('\n')



