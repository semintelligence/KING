
# An Indian Court Decision Annotated Corpus and Knowledge Graph Construction

An annotated Indian Court Decision Document Corpus consisting of 
10 coarse-grained classes and 30 fine-grained classes as a 
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
https://doi.org/10.6084/m9.figshare.19719088.v4

To corroborate the domain-specific tags, two semantic classes were defined; namely, coarse-grained
class and fine-grained class, each consisting of 10 and 30 attributes respectively.
Coarse-grained are the more general semantic classes for the legal domain, which
include the classes Court, Party, CourtDecision, Document, Jurisdiction, Location,
CaseType, Author, CourtOfficial, and DateOfJudgment.

![Coarse Grained and Fine Grained Classes](https://github.com/semintelligence/KING/blob/main/pre-processing/classes.PNG "classes")

## Knowledge Graph Construction
The two major steps for the construction of the knowledge graph are Named
Entity Recognition (NER) and Relation Extraction (RE). Various legal entities
identified from the corpus by referring to the [NyOn](https://github.com/semintelligence/NyOn) Ontology are combined together with the relations extracted for the construction of the Knowledge Graph
(KG). 
### Named Entity Recognition
The entity extraction is substantially carried out with the help of regular
expressions and triggering target words. Examples of rules used to extract the entities "JURISDICTION" and "LOCATION" are given below.
```python
#JURISDICTION
    jur = re. search (r"(\w+\W+) {1}( JURISDICTION )", contents )
    if jur:
    data . append (" JURISDICTION $ "+jur . group (0)+"")

#LOCATION
    loc = re. search ('(\w{4 ,}) ( High Court )', contents )
    if loc:
    if (( loc. group (1) ). lower () == 'pradesh '):
    loc = re. search ('(\w{4 ,}) ( Pradesh )', contents ,re.IGNORECASE )
    data . append (" LOCATION $ "+loc. group ()+"")
    elif (( loc. group (1)). lower () == ’kashmir '):
    data . append (" LOCATION $ Jammu and Kashmir "+'')
    elif (( loc. group (1)). lower () == 'haryana '):
    data . append (" LOCATION $ Punjab and Haryana "+'')
    else :
    data . append (" LOCATION $ "+loc. group (1)+"")
```
An example of the output file from the NER phase for the case "KEWAL KRISHAN VS. STATE OF PUNJAB" dated 06/03/1962 is
given below.

![NER Sample Output](https://github.com/semintelligence/KING/blob/main/ner/NER_Sample_Output.PNG "NER_Sample_Output")


### Relation Extraction
Relation extraction phase identifies the relation between the entities extracted
in the NER phase. The NyOn Ontology is referred for identifying the various
relations between the extracted entities. ince there are
no sentences in the output of the NER phase, switch case is used for annotating
the relations between the extracted entities. An example of python rule for extracting and annotating
relations is given below.

```python
#CASE_NAME
    if 'FILE_NAME ' in temp :
        re += '\n'+ tok_ent ['Entity '][i]+ '\n'
        CASENAME =ids [ index ]
        re += 'CASE hasCaseId '+ CASENAME +'\n'
        index +=1

#BENCH
    if 'BENCH ' in temp :
        re += CASENAME +' hasCourtOfficial Judge '+'\n'
        str = tok_ent ['Entity '][i]
        my_list =str. split (",")
        for x in range (len ( my_list )):
            re += 'Judge hasName '+ my_list [x]+ '\n'
```
The triples obtained after annotating the entities with the corresponding relation
for the case "KEWAL KRISHAN VS. STATE OF PUNJAB" dated 06/03/1962
is given below.

![RE Sample Output](https://github.com/semintelligence/KING/blob/main/re/RE_Sample_output.PNG "RE_Sample_output")


### Triple Construction
The Triples were formed by annotating the entities obtained from NER with the relations extracted in the RE phase. 
The output file from the RE phase is passed through a python script to generate the RDF (.ttl) file.
The constructed triples were stored in a triple store (Apache Jena Fuseki) and visualized using GraphDb.
The generated RDF corresponding to all the 50 documents is given [here](https://github.com/semintelligence/KING/blob/main/kg_ttl_file/Triples.ttl) and knowledge graph visualized through GraphDb is given below.

![Knowledge Graph](https://github.com/semintelligence/KING/blob/main/kg_ttl_file/Knowledge_Graph.png "Knowledge Graph visualized through GraphDB")
## Competency Questions and SPARQL Query
The triples formed where tested against competency questions with the help of SPARQL queries.
Screenshots of the competency questions, corresponnding SPARQL queries and outputs are attached below.

1. List all the cases from the month of September.<br />
![Query 1](https://github.com/semintelligence/KING/blob/main/query/query1.PNG "Query 1")<br />
![Output 1](https://github.com/semintelligence/KING/blob/main/query/output/query1_output.PNG)<br />

2. List all the cases filed in the year 1996.<br />
Query:<br />
![Query 2](https://github.com/semintelligence/KING/blob/main/query/query2.PNG "Query 2")<br />
Output:<br />
![Output 2](https://github.com/semintelligence/KING/blob/main/query/output/query2_output.PNG)<br />

3. List all the cases under case type 'criminal'.<br />
![Query 3](https://github.com/semintelligence/KING/blob/main/query/query3.PNG "Query 3")<br />
![Output 3](https://github.com/semintelligence/KING/blob/main/query/output/query3_output.PNG)<br />

4. List all the cases with Vivian Bose/V. Bose as a judge.<br />
![Query 4](https://github.com/semintelligence/KING/blob/main/query/query4.PNG "Query 4")<br />
![Output 4](https://github.com/semintelligence/KING/blob/main/query/output/query4_output.PNG)<br />
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
