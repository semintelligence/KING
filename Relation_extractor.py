
import pandas as pd

tok_ent = pd.read_table('C:\\Users\\shubh\\Desktop\\Dataset\\NER_Dataset\\output.txt',delimiter=' - ',engine='python') 

with open(r'C:\Users\shubh\Desktop\Dataset\RE_Dataset\re_output.txt', 'a') as outf:
    for i in range(tok_ent.shape[0]):
    
        if tok_ent['Token'][i]=='CASE_NAME':
            CASENAME=tok_ent['Entity'][i]

        if tok_ent['Token'][i]=='FILE_NAME':
            outf.write('\n')

        agrument=tok_ent['Token'][i]
        match agrument:
            case 'FILE_NAME' :
                outf.write(tok_ent['Entity'][i]+'\n')
                CASENAME=""
            case 'DATE_OF_JUDGMENT':
                outf.write(CASENAME+' hasDate '+tok_ent['Entity'][i]+'\n')
                
            case 'CASE_NAME':
                outf.write('CASE hasCaseName '+ tok_ent['Entity'][i]+'\n')

            case 'PETITIONER':
                outf.write(CASENAME+' hasParty '+ tok_ent['Token'][i]+'\n')
                outf.write('PETITIONER hasName '+tok_ent['Entity'][i]+'\n')

            case 'RESPONDENT':
                outf.write(CASENAME+' hasParty '+ tok_ent['Token'][i]+'\n')
                outf.write('RESPONDENT hasName '+tok_ent['Entity'][i]+'\n')

            case 'CASE_NO':
                if(CASENAME):
                    outf.write(CASENAME+' hasCaseNo '+ tok_ent['Entity'][i]+'\n')
                else:
                    (outf.write('Case hasCaseNo '+ tok_ent['Entity'][i]+'\n'))

            case 'CASE_TYPE':
                if(CASENAME):
                    outf.write(CASENAME+' hasCaseType '+ tok_ent['Entity'][i]+'\n')
                else:
                    (outf.write('Case hasCaseType '+ tok_ent['Entity'][i]+'\n'))
            
            case 'APPEAL_NO':
                if(CASENAME):
                    outf.write(CASENAME+' hasAppealNo '+ tok_ent['Entity'][i]+'\n')
                else:
                    (outf.write('Case hasAppealNo '+ tok_ent['Entity'][i]+'\n')) 
        
            
            case 'AUTHOR':
                outf.write(CASENAME+' hasAuthor '+tok_ent['Entity'][i]+'\n')

            case 'BENCH':
                outf.write(CASENAME+' hasCourtOfficial Judge '+'\n')
                str=tok_ent['Entity'][i]
                my_list =str.split(",")
                for x in range(len(my_list)):
                    outf.write('Judge hasName '+my_list[x]+'\n')

            case 'JURISDICTION':
                if(CASENAME):
                    outf.write(CASENAME+' hasJurisdiction '+tok_ent['Entity'][i]+'\n')
                else:
                    outf.write('Case hasJurisdiction '+tok_ent['Entity'][i]+'\n')
            
            case 'COURT_TYPE':
                if(CASENAME):
                    outf.write(CASENAME+' hasCourt '+tok_ent['Entity'][i]+'\n')
                else:
                    outf.write('Case hasCourt '+tok_ent['Entity'][i]+'\n')
                
                if(tok_ent['Token'][i+1]=='LOCATION'):
                    outf.write(tok_ent['Entity'][i]+' hasLocation '+tok_ent['Entity'][i+1]+'\n')

            case 'COURT_DECISION':
                if(CASENAME):
                    outf.write(CASENAME+' hasCourtDecision '+tok_ent['Entity'][i]+'\n')
                else:
                    outf.write('Case hasCourtDecision '+tok_ent['Entity'][i]+'\n')
            