import os
import re
from collections import OrderedDict

path = (r"C:\Users\suraj\Desktop\KG\TestData")
os.chdir(path)

def read_text_file(file_path):
    with open(file_path, 'r') as f:
        contents = f.read()
        with open(r'C:\Users\suraj\Desktop\KG\output.txt', 'a') as outf:
            outf.write(" \n")
            outf.write("FILE_NAME - "+os.path.basename(f.name)+'\n')
            #PETITIONER
            petitioner = re.search('PETITIONER:(.*?)(Vs.|RESPONDENT)', contents)
            
            #RESPONDENT
            respondent = re.search('RESPONDENT:(.*?)DATE', contents)

            #DATE OF JUDGMENT
            date =re.search(r'DATE OF JUDGMENT: (\S+)', contents)

            #CASE_NO
            appeal_no = re.search(r'(?=Appeal No)(\w+\W+)*?\d+(\w+\W+)*?\b\d{4}\b', contents,re.IGNORECASE)
            case_no = re.search(r'(?=CASE NO)(\w+\W+)*?\d+(\w+\W+)*?\b\d{4}\b', contents)

            #CASENAME
            if respondent and petitioner and date:
                case_name  = petitioner.group(1) + 'VS.' + respondent.group(1) + ' on '+date.group(1)
                outf.write("CASE_NAME - "+case_name+"\n")
                outf.write("PETITIONER - "+petitioner.group(1)+"\n")
                outf.write("RESPONDENT - "+respondent.group(1)+"\n")
                outf.write("DATE_OF_JUDGMENT - "+date.group(1)+"\n")
            elif respondent and petitioner:
                case_name  = petitioner.group(1) + 'VS.' + respondent.group(1)
                outf.write("CASE_NAME - "+case_name+"\n")
                outf.write("PETITIONER - "+petitioner.group(1)+"\n")
                outf.write("RESPONDENT - "+respondent.group(1)+"\n")
            
            elif case_no:
                case_name=case_no.group()
                outf.write("CASE_NAME - "+case_name+"\n")
            elif appeal_no:
                case_name=appeal_no.group()
                outf.write("CASE_NAME - "+case_name+"\n")
            if appeal_no:
                outf.write("APPEAL_NO - "+appeal_no.group()+"\n")
            if case_no:
                outf.write("CASE_NO - "+case_no.group()+"\n")

            #CASE_TYPE
            ctyp=re.search('CIVIL',contents,re.IGNORECASE)
            if ctyp:
                ctyp = ctyp.group()
                outf.write("CASE_TYPE - "+ctyp+'\n')
            ctyp=re.search('CRIMINAL',contents,re.IGNORECASE)
            if ctyp:
                ctyp = ctyp.group()
                outf.write("CASE_TYPE - "+ctyp+'\n')

            #AUTHOR
            auth = re.search('BENCH: (.*?) (BENCH)', contents)
            if auth:
                auth = auth.group(1)
                auth = ' '.join(reversed(auth.split(",")))
                if "&" in auth:
                    auth = auth.split("&")[0]
                outf.write("AUTHOR - "+auth+"\n")

            #BENCH
            bench = re.search('BENCH:(.+?)(CITATION:|JUDGMENT|ACT:)', contents)
            if bench:
                if "&" in bench.group(1) :
                    bench = ', '.join((bench.group(1)).split("&"))
                    outf.write("BENCH - "+bench+"\n")
                else:
                    names = re.findall(r'((?:\w+), (?:\w+(?: \w+)?))(?= BENCH:| CITATION:| \w+, | JUDGMENT)', bench.group(0))
                    names = list(OrderedDict.fromkeys(names))
                    names = ', '.join((map(lambda n:' '.join(n.split(', ')[-1::-1]), names)))
                    if (names):
                        outf.write("BENCH - "+names+"\n")
                    else:
                        outf.write("BENCH - "+bench.group(1)+"\n")


            #JURISDICTION
            jur = re.search(r"(\w+\W+){1}(JURISDICTION)", contents)
            if jur:
                outf.write("JURISDICTION - "+jur.group(0)+"\n")

            #COURT TYPE
            jur = re.search('Supreme Court of India', contents,re.IGNORECASE)
            if jur:
                outf.write("COURT_TYPE - "+jur.group()+"\n")
            jur = re.search('High Court', contents)
            if jur:
                outf.write("COURT_TYPE - "+jur.group()+"\n")
            jur = re.search('District Court', contents)
            if jur:
                outf.write("COURT_TYPE - "+jur.group()+"\n")

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

            #COURT DECISION
            dec=re.search('Appeal is disposed',contents,re.IGNORECASE)
            if dec:
                dec = dec.group()
                outf.write("COURT_DECISION - "+dec+'\n')
            dec=re.search('Appeal is disallowed',contents,re.IGNORECASE)
            if dec:
                dec = dec.group()
                outf.write("COURT_DECISION - "+dec+'\n')
            dec=re.search('Appeal is allowed',contents,re.IGNORECASE)
            if dec:
                dec = dec.group()
                outf.write("COURT_DECISION - "+dec+'\n')

for file in os.listdir():
            if file.endswith(".txt"):
                file_path = f"{path}\{file}"
                read_text_file(file_path)