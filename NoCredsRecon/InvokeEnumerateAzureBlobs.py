from dns import resolver
import requests
from threading import Thread

# Based on https://github.com/NetSPI/MicroBurst/blob/master/Misc/Invoke-EnumerateAzureBlobs.ps1
# This code is used to enumerate public Azure Blobs and Containers. 
# The code first attempts to resolve the DNS query of a given base name with the ".blob.core.windows.net" suffix. 
# If the DNS query is successful, the base name is then added to the valid_domains list. 
# The GetBlob function will then make a request to the specified domain and folder and, if successful, print the URL of the folder and its contents. 
# Finally, the EnumerateAzureBlobs function will iterate through the specified list of folders and will create a thread for each folder with the specified domain.

valid_domains =[]

def baseQuery(base, verbose=False):
	if(verbose):
		print("Fetching " + base +".blob.core.windows.net" )

	try:
		result = resolver.resolve(rdtype="A" ,  qname=base+".blob.core.windows.net" , raise_on_no_answer=False )
		if(result):
			valid_domains.append(base +".blob.core.windows.net")

	except:
			pass


def getBlob(domain, folder , verbose=False):
	uri = "https://" + domain + "/" + folder + "?restype=container"
	response = requests.get(uri)
	if(response.status_code == 200):
		urilist = "https://" + domain + "/" + folder + "?restype=container&comp=list"
		print("Found folder " + folder +" at " + domain + " you can try to see the list of files at " + urilist)
		


def enumerateAzureBlobs(base="" , verbose=False , folders="folders.txt" ):
	domain = '.blob.core.windows.net'
	if(base==""):
		print("Not base name especified.")
	else:

		baseQuery(base)

		threads = []

		for domain in valid_domains:
			try:
				with open(folders) as folders_file:
					for line in folders_file:
						arguments = {"domain":domain , "folder":line.strip() , "verbose":verbose}
						thread = Thread(target=getBlob, kwargs=arguments)
						threads.append(thread)
						thread.start()
			except:
				if(verbose):
					print("Invalid folders file.")
				
		for thread in threads:
			thread.join()

