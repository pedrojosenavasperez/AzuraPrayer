from dns import resolver
from tabulate import tabulate

# Based on https://github.com/NetSPI/MicroBurst/blob/master/Misc/Invoke-EnumerateAzureSubDomains.ps1
# Enumerate public Azure Blobs and Containers.
# The function will check for valid .blob.core.windows.net host names via DNS


final_table=[]

def BaseQuery(base, verbose=False):
	if(verbose):
		print("Fetching " + base +".blob.core.windows.net" )
	try:
		result = resolver.resolve(rdtype="A" ,  qname=base+".blob.core.windows.net·" , raise_on_no_answer=False )
		if(result):
			final_table.append("Found Storage Account "+ base +".blob.core.windows.net" )
	except:
			pass


def EnumerateAzureBlobs(base="" , permutations="permutations.txt" , verbose=False , folders="permutations.txt" , OutputFile="" , BingAPIKey=""):
	domain = '.blob.core.windows.net'
	if(base==""):
		print("Not base name especified.")
	else:

		BaseQuery(base)

		try:
			with open(permutations) as permutations_file:
				for line in permutations_file:
					line_strip = line.rstrip()
					BaseQuery(line_strip+base)
					BaseQuery(base+line_strip)
		except:
			print("Invalid permutation file.")
		
		print(tabulate(final_table, headers=['Findings'], tablefmt='fancy_grid'))

		if(verbose):
				print("DNS bruteforce finished , starting container enumeration")

		if(BingAPIKey != ""):
			BingQuery = "site:blob.core.windows.net "+ Base
			# To DO implement this

		for domain in final_table:
			try:
				with open(permutations) as permutations_file:
					for line in permutations_file:
						line_strip = line.rstrip()
						BaseQuery(line_strip+base)
						BaseQuery(base+line_strip)
			except:
				print("Invalid permutation file.")
				

