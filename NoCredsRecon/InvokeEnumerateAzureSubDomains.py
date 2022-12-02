from dns import resolver
from tabulate import tabulate
from threading import Thread

# Based on https://github.com/NetSPI/MicroBurst/blob/master/Misc/Invoke-EnumerateAzureSubDomains.ps1
# This code is used to enumerate subdomains for Microsoft Azure services. 
# The `threadable` function attempts to resolve the full domain, and if successful it prints a message. 
# The `baseQuery` function takes the domain to use in the subdomain search and creates threads to search the subdomain.
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

def threadable(register_type ,  fulldomain ,subdomain):
	try:
		result = resolver.resolve(rdtype=register_type ,  qname=fulldomain , raise_on_no_answer=False )
		if(result):
			print("Found url for " + subdomain +" at: " + fulldomain)
	except:
		pass


def baseQuery(base, verbose=False):
	threads = []
	for subdomain in subdomains:
		for register_type in register_types:
			if(verbose):
				print("Enumerating " + base +" subdomains for "+ subdomain )
			try:
				#Thats doesnt work for MX register with authoritative answer
				arguments = {"register_type":register_type , "fulldomain":base+"."+subdomain, "subdomain":subdomains[subdomain]}
				thread = Thread(target=threadable, kwargs=arguments)
				threads.append(thread)
				thread.start()
				
			except:
				pass
	
	#Wait for all threads to finish
	for thread in threads:
		thread.join()

def enumerateAzureSubDomains( base="" , permutations="" , verbose=False):
	if(base==""):
		print("Not base name especified.")
	else:
		baseQuery(base,verbose)

		try:
			with open(permutations) as permutations_file:
				for line in permutations_file:
					line_strip = line.rstrip()
					baseQuery(line_strip+base,verbose)
					baseQuery(base+line_strip,verbose)
		except:
			print("Invalid permutation file.")

