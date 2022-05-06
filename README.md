
# An Indian Court Decision Annotated Corpus and Knowledge Graph Construction

An annotated Indian Court Decision Document Corpus consisting of 
16 coarse-grained classes and 41 fine-grained classes as a 
benchmark dataset for constructing the knowledge graph. 
Indian Court Case Documents’ knowledge graph constructed by 
utilizing a rule-based approach for Named Entity Recognition (NER) 
and Relation Extraction (RE).
## Authors

- [Pariskhit Kamat](https://github.com/parikkamat)
- [Shubham Kalson](https://github.com/ShubhamKalson)
- [Suraj S](https://github.com/surajsuresh29)
- [Pooja Harde](https://github.com/PoojaHarde)
- [Nandana Mihindukulasooriya](https://github.com/nandana)
- [Sarika Jain](https://github.com/semintelligence)



## Indian Court Decision Annotated Corpus
The legal documents for creating the corpus were collected from 
’[Indian Kanoon](https://indiankanoon.org/)’, an online search engine
for Indian legal documents. The data from the text files were split 
into sentences, tokenized word by word and annotated with POS 
tags using SPACY. Named Legal Entities were identified manually 
from these tokens and were tagged with domain specific tags using 
CoNLL-2003 format. The dataset is provided in three different encoding schemes of the CoNLL-2003
An Indian Court Decision Annotated Corpus and KG Construction 7
format, namely BILOU ((B-Beginning, I-Internal, L-Last, O-outside,U-Unit),
IOB (I-Inside, O-Outside, B-Beginning) and IOBES (I-Inside, O-Outside, B-
Beginning, E-End, S-Single). The dataset is published using FigShare with CC by 4.0 licence with the DOI:
https://doi.org/10.6084/m9.figshare.19719088.v1
## Knowledge Graph Construction
The two major steps for the construction of the knowledge graph are Named
Entity Recognition (NER) and Relation Extraction (RE). Various legal entities
identified from the corpus by referring to the [NyOn](https://github.com/semintelligence/NyOn) Ontology are combined together with the relations extracted for the construction of the Knowledge Graph
(KG). 
### Natural Entity Recognition
The entity extraction is substantially carried out with the help of regular
expressions and triggering target words. Examples of rules used to extract the entities "JURISDICTION" and "LOCATION" are given below.
```python
#JURISDICTION
jur = re.search(r"(\w+\W+){1}(JURISDICTION)", contents)
if jur:
    outf.write("JURISDICTION - "+jur.group(0)+"\n")

#LOCATION
loc = re.search('(\w{4,}) (High Court)', contents)
if loc:
    if ((loc.group(1)).lower()=='pradesh'):
        loc = re.search('(\w{4,}) (Pradesh)', contents,re.IGNORECASE)
        outf.write("LOCATION - "+loc.group()+"\n")
    elif ((loc.group(1)).lower()=='kashmir'):
        outf.write("LOCATION - Jammu and Kashmir"+'\n')
    elif ((loc.group(1)).lower()=='haryana'):
        outf.write("LOCATION - Punjab and Haryana"+'\n')
    else:
        outf.write("LOCATION - "+loc.group(1)+"\n")

```
The output from the NER phase is stored in a single text file with the token
and entity separated by the delimiter ’-’.

### Relation Extraction
Relation extraction phase identifies the relation between the entities extracted
in the NER phase. The NyOn Ontology is referred for identifying the various
relations between the extracted entities. ince there are
no sentences in the output of the NER phase, switch case is used for annotating
the relations between the extracted entities. An example of python rule for extracting and annotating
relations is given below.

```python
    #CASE_NAME
    if tok_ent['Entity'][i]=='CASE_NAME':
        CASENAME=tok_ent['Token'][i]
    agrument=tok_ent['Entity'][i]
    match agrument:

    #JURISDICTION
    case 'JURISDICTION':
        if(CASENAME):
            outf.write(CASENAME+' hasJurisdiction '+tok_ent['Entity'][i]+'\n')
        else:
            outf.write('Case hasJurisdiction '+tok_ent['Entity'][i]+'\n')
```
### Triple Construction

The Triples were formed by annotating the entities obtained from NER with the relations exrtracted in the RE phase.
The constructed triples were stored in a triple store (Apache Jena Fuseki) by manualy converting it to turtle(.ttl) format  and visualized using GraphDb.
An example of the manualy constructed RDf(.ttl) file and knowledge graph visualized through GraphDb are given below.

```
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix schema: <http://schema.org/> .
@prefix : <http://example.org/#> .

:Case a schema:Thing ;
   dc:hasCaseName :case1, :case2 ;
.

:case2
          a schema:KT_Varghese_Ors_VS_State_of_Kerala ;
          rdfs:label "K.T. Varghese & Ors VS. State of Kerala & Ors. on 24/01/2008" ;                                
          dc:hasParty :case2P1, :case2P2;
 rdfs:hasAppealNo "Appeal No.547/1998";
 rdfs:hasCaseNo "Appeal (civil) 6456 of 2001";
 rdfs:hasCaseType "civil";
 rdfs:hasDate "24/01/2008";
 rdfs:hasAuthor :case2Judge2;
          rdfs:hasCourtDecision "Appeal is Allowed" ;
          dc:hasCourtOfficial :case2Judge1, :case2Judge2, :case2Judge3 ;
         
.

:case2P1 a schema:Petitioner, foaf:Person ;
            rdfs:hasName "K.T. Varghese & Ors" ;
.

:case2P2 a schema:Respondent, foaf:Person ;
            rdfs:hasName "State of Kerala & Ors" ;
.
```

![Knowledge Graph](https://github.com/semintelligence/KING/blob/main/kg%20ttl%20file/kg.jpg "Knowledge Graph visualized through GraphDB")
## Competency Questions and SPARQL Query
The triples formed where tested against competency questions with the help of SPARQL queries.
Screenshots of the competency questions, corresponnding SPARQL queries and outputs are attached below.

1. List all court officials that come under 'K.T. Varghese & Ors VS. State of Kerala & Ors.'
![Query 1](https://github.com/semintelligence/KING/blob/main/query/query1.JPG "Query 1")
![Output 1](https://github.com/semintelligence/KING/blob/main/output/output1.JPG)

2. What is the case number of case 'K.T. Varghese & Ors VS. State of Kerala & Ors.'
![Query 2](https://github.com/semintelligence/KING/blob/main/query/query2.JPG "Query 2")
![Output 2](https://github.com/semintelligence/KING/blob/main/output/output2.JPG)

3. Who is the Petitioner of 'K.T. Varghese & Ors VS. State of Kerala & Ors.'?
![Query 3](https://github.com/semintelligence/KING/blob/main/query/query3.JPG "Query 3")
![Output 3](https://github.com/semintelligence/KING/blob/main/output/output3.JPG)

4. List all the parties that come under case 'K.T. Varghese & Ors VS. State of Kerala & Ors.'
![Query 4](https://github.com/semintelligence/KING/blob/main/query/query4.JPG "Query 4")
![Output 4](https://github.com/semintelligence/KING/blob/main/output/output4.JPG)
## Acknowledgements

 This work is supported by the IHUB-ANUBHUTI-IIITD FOUNDATION set up under the NM-ICPS scheme of the Department of Science and Technology, India.
We thank Mr. Vaibhav Vats, Advocate, Punjab and Haryana High Court, Chandigarh for providing his valuable reviews for the dataset.
## Contacts

**Pariskhit Kamat (National Institute of Technology, Kurukshetra, India)** pariskhit_52010088@nitkkr.ac.in

**Shubham Kalson (National Institute of Technology, Kurukshetra, India)** shubham_52010087@nitkkr.ac.in

**Suraj S (National Institute of Technology, Kurukshetra, India)** suraj_52010085@nitkkr.ac.in

**Pooja Harde (National Institute of Technology, Kurukshetra, India)** pmharde29@gmail.com

**Nandana Mihindukulasooriya (IBM Research, Dublin, Ireland)** nandana@ibm.com

**Dr. Sarika Jain (National Institute of Technology, Kurukshetra, India)** jasarika@nitkkr.ac.in
