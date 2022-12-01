from dns import resolver
from tabulate import tabulate
from threading import Thread

# Based on https://github.com/NetSPI/MicroBurst/blob/master/Misc/Invoke-EnumerateAzureSubDomains.ps1
# Enumerate azure public subdomains
# The function will check for valid Azure subdomains, based off of a base word, via DNS. 

register_types = ["A","AAAA","MX"]
subdomains = {	"onmicrosoft.com" : "Microsoft Hosted Domain",
				"scm.azurewebsites.net" : "App Services - Management",
				"azurewebsites.net" : "App Services",
				"p.azurewebsites.net" : "App Services",
				"cloudapp.net" : "App Services",
				"file.core.windows.net" : "Storage Accounts - Files",
				"blob.core.windows.net" : "Storage Accounts - Blobs",
				"queue.core.windows.net" : "Storage Accounts - Queues",
				"table.core.windows.net" : "Storage Accounts - Tables",
				"mail.protection.outlook.com" : "Email",
				"sharepoint.com" : "SharePoint",
				"redis.cache.windows.net" : "Databases-Redis",
				"documents.azure.com" : "Databases-Cosmos DB",
				"database.windows.net" : "Databases-MSSQL",
				"vault.azure.net" : "Key Vaults",
				"azureedge.net" : "CDN",
				"search.windows.net" : "Search Appliance",
				"azure-api.net" : "API Services",
				"azurecr.io" : "Azure Container Registry"}
final_table = []

def threadable(register_type ,  fulldomain ,subdomain):
	try:
		result = resolver.resolve(rdtype=register_type ,  qname=fulldomain , raise_on_no_answer=False )
		if(result):
			table = [ subdomain, fulldomain]
			print("Found url for " + subdomain +" at: " + fulldomain)
	except:
		pass


def BaseQuery(base, verbose=False):
	threads = []
	for i in subdomains:
		for register_type in register_types:
			if(verbose):
				print("Enumerating " + base +" subdomains for "+ i )
			try:
				#Thats doesnt work for MX register
				arguments = {"register_type":register_type , "fulldomain":base+"."+i, "subdomain":subdomains[i]}
				thread = Thread(target=threadable, kwargs=arguments)
				threads.append(thread)
				thread.start()
				
			except:
				pass
	
	#Wait for all threads to finish
	for thread in threads:
		thread.join()

	


def EnumerateAzureSubDomains( base="" , permutations="" , verbose=False):
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

	return final_table


