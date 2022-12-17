from Bio import Entrez

Entrez.email = "tmkluiters@tudelft.nl"

handle = Entrez.esummary(db='bioproject', id='PRJNA555636')
result = Entrez.parse(handle)
for record in result:
    print(record)
