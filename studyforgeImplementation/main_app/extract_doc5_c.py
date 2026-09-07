import re
doc = open(r'F:\Code by Akshat\testgemini\studyforge\resource\notes\new architect\StudyForge_Document_5_Missing_Features_and_Agreed_Amendments_Register.md', encoding='utf-8').read()
m = re.search(r'## C\..*?(?=## D|$)', doc, re.DOTALL)
open('doc5_section_c.txt', 'w', encoding='utf-8').write(m.group(0) if m else 'Not found')
