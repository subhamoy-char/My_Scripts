import io
import os

with open('out-N48', 'r') as file:
	contents = file.read()
	character = 'end'
	result = contents.split(character)
nlength = len(result)
print(nlength)
#
for i in range(nlength-1):
	with io.open("file_" + str(i) + ".dat", 'w', encoding='utf-8', buffering=100000000) as f:
		f.write(result[i])
for i in range(nlength-1):
	with open('file_' + str(i) + '.dat') as reader, open('file_' + str(i) + '.dat', 'r+') as writer:
		for line in reader:
			if line.strip():
				 writer.write(line)
		writer.truncate()
atoms_data = []
ncharge_config = 0
for i in range(nlength-1):
	atoms_data.clear()
	Zr_atom = 0
	La_atom = 0
	Si_atom = 0
	O_atom = 0
	Vac = 0
	with open('file_' + str(i) + '.dat') as reader:
		atoms_data.append([line.split() for line in reader])
	nlen=len(atoms_data[0])
	for j in range(6,nlen,1):
		#print(atoms_data[0][j][3]) 
		if atoms_data[0][j][3].strip('\n') == 'Zr':
			Zr_atom = Zr_atom + 1
		elif atoms_data[0][j][3].strip('\n') == 'Si':
			Si_atom = Si_atom + 1
		elif atoms_data[0][j][3].strip('\n') == 'La':
                        La_atom = La_atom + 1
		elif atoms_data[0][j][3].strip('\n') == 'O':
                        O_atom = O_atom + 1
	#print(Zr_atom, Si_atom, La_atom, O_atom)
	if ((4*Zr_atom + 3*La_atom + 4*Si_atom - 2*O_atom) == 0):
		print(i,Zr_atom, Si_atom, La_atom, O_atom)
		ncharge_config = ncharge_config + 1
		#print(len(atoms_data[0]))
		with open('newfile_' + str(i) + '.dat', 'w') as file:
			for k in range(len(atoms_data[0])):
				s =  ' '.join(atoms_data[0][k])
				file.write(str(s))
				file.write("\n")
			#print(len(atoms_data[0]))
	os.remove('file_' + str(i) + '.dat')
	#print(Zr_atom, Si_atom, La_atom, O_atom)
print(ncharge_config)
