#Senem Yalın/180709009
import os, hashlib, requests, multiprocessing


links_array = ["https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg",
"https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png",
"http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
"http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg"]

def download_file(url, file_name=None):
	r = requests.get(url, allow_redirects = True)
	file = file_name if file_name else str(uuid.uid4())
	open(file, 'wb').write(r.content)

def child_process():
	process = os.fork()
	if (process <= 0):
		#to print child process
		print("PID of child process is ", os.getpid())
		count = 0

		#to download the files with the child process 
		while(count < len(links_array)):
			download_file(links_array[count], "File{}".format(count+1))
			count = count + 1
	else: #(process > 0)
	
		#to avoid the orphan process situation
		os.wait()
		print("PID of parent process is ", os.getpid())
		exit()

#calling function
child_process()

hash_array={}
hash_unique_array={}

def hashing(name, pipe):
	with open('/home/kali/Downloads/{}'.format(name),'rb') as f:
			content = f.read()

			#to find "file checksums"
			md5_hash = hashlib.md5()
			md5_hash.update(content)

			digest = md5_hash.hexdigest()

			#to put "file checksums" in hash_array with the file names
			pipe.send(digest);
				

def multi_processing():

	spath = r"/home/kali/Downloads"

#	list_of_files = os.listdir(spath)

	for name in os.listdir(spath):
		parentPipe, childPipe=multiprocessing.Pipe()
		p1 = multiprocessing.Process(target=hashing, args=(name,childPipe))
		p1.start()
		hash_array[name]=parentPipe.recv()
		p1.join()

#	hashing(list_of_files[0])
#	hashing(list_of_files[1])
#	hashing(list_of_files[2])
#	hashing(list_of_files[3])
#	hashing(list_of_files[4])

#calling function
multi_processing()

#to find unique files and list in hash_unique_array
def controlling_duplicate_files():

	for first in hash_array.keys():
		count = 0
		for second in hash_unique_array.keys():
			if (count > 0):
				break
			elif (hash_array[first] == hash_unique_array[second]):
				count=count+1
			else:
				continue
		if(count == 0):
			#to remove duplications and find unique files
			hash_unique_array[first] = hash_array[first]
			print(first)
			print(hash_unique_array[first])
		else:
			continue
#calling function
controlling_duplicate_files()
