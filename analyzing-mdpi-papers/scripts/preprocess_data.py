import pandas as pd 


#import paper links
papers = pd.read_csv("/Users/christianfang/Documents/GitHub/datascienceprojects/analyzing-mdpi-papers/data/all_papers.csv")

#Exclude duplicates
papers["identifier"] = papers["identifier"].dropna()

#Get identifiers
identifiers = papers["identifier"]
identifiers.head()

#Delete oai: prefix and : between mdpi.com and the links
identifiers = identifiers.map(lambda x: x.lstrip('oai:').rstrip('/'))
identifiers = identifiers.str.replace(':','')
identifiers = '"' + 'https://www.' + identifiers + '"'

#Write identifiers as csv
identifiers = pd.DataFrame(identifiers)
identifiers.to_csv("/Users/christianfang/Documents/GitHub/datascienceprojects/analyzing-mdpi-papers/data/identifiers.csv")