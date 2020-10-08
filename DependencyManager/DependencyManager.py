import re 
import pip

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search
	
def findLinesWithWord(file, word, nword):
	pos=[]
	fromcicle=0
	i=0
	restsentence=''
	for line in file:
		if findWholeWord(nword)(line):
			if findWholeWord(word)(line):
				pos.append(line)
				continue
			fromcicle=1
			restsentence=line	
		elif findWholeWord(word)(line) and fromcicle==1:
			pos.append(restsentence+line)
			fromcicle=0
			pos[i].replace('\n', '')
			i=i+1
		elif findWholeWord(word)(line) and fromcicle==0:
			pos.append(line)
			pos[i].replace('\n', '')
			i=i+1
	for i in range(len(pos)):
		pos[i]=pos[i].replace("\n","")
	return pos

def tryImportElseDownload(strWithImp):
	imports=[]
	for line in strWithImp:
		try:
			exec(line)
		except ModuleNotFoundError:
			print (line + ' not installed in this computer')
			if (findWholeWord('import')(line) and findWholeWord('from')(line)):	
				imports.append(re.findall(r'from\s+(.+?)\s+import',line)[0])	
			else:
				obj=re.findall(r'import\s+(.+)',line)[0].split(',')	
				for word in obj:
					imports.append(word)
	import sys
	import subprocess
	print('this libreries weren\'t installed in this computer ')
	print(imports)
	if input("\nIf you want to install missing dependencies print \"Yes\"\n else print any thing to exit programm...\n")=="Yes":
		for word in imports:
			try:
				subprocess.check_call([sys.executable, '-m', 'pip', 'install', word])
				__import__(word)
				print('Librery  \"' + word +'\" was installed\n' + word)
			except:
				print('Librery \"' + word +'\" was not found' )
		
	else:
		print("Dependencies weren't installed")
		


f = open(input("enter python file path\n"))


strWithImp=findLinesWithWord(f, 'import','from')

print(strWithImp)
tryImportElseDownload(strWithImp)

