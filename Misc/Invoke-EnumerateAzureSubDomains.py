from dns import resolver


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


def BaseQuery(base, verbose=False):
		for i in subdomains:
			for register_type in register_types:
				if(verbose):
					print("Enumerating " + base +" subdomains for "+ i )
				try:
					#Thats doesnt work for MX register
					result = resolver.resolve(rdtype=register_type ,  qname=base+"."+i , raise_on_no_answer=False )
					if(result):
						print(subdomains[i] + ":                   " + base+"."+i )
						break
				except:
					pass

	


def EnumerateAzureSubDomains ( base="" , permutations="permutations.txt" , verbose=False):
	if(base==""):
		print("Not base name especified.")
	else:

		BaseQuery(base)

		try:
			with open(permutations) as permutations_file:
				for line in permutations_file:
					BaseQuery(line+base)
					BaseQuery(base+line)
		except:
			print("Invalid permutation file.")

