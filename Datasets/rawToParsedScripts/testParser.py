from PyPDF2 import PdfReader
from testParserFunctions import pdfTextExtractor, buildQuestionAndCommentDictionaryArray
from lawsExtractionFunctions import processOabQuestions, createLegalPrincipalsColumn
import pandas as pd

OAB38 = "../rawTests/OAB-38-resolution.pdf"
OAB39 = "../rawTests/OAB-39-resolution.pdf"
OAB40 = "../rawTests/OAB-40-resolution.pdf"
OAB41 = "../rawTests/OAB-41-resolution.pdf"

oabTests = [OAB38, OAB39, OAB40, OAB41]

for testPath in oabTests:
    filePath = testPath
    pdf = PdfReader(filePath)
    oabNumber = filePath.split('/')[2].split('-')[1]

    pdfTextExtractor(pdf, f"extractedText/oab{oabNumber}extractedText.txt")
    questionAndAnswerList = buildQuestionAndCommentDictionaryArray(f"extractedText/oab{oabNumber}extractedText.txt")

    questionsList = []
    commentList = []
    legalPrinciples = []
    for questionAndAnswer in questionAndAnswerList:
        questionsList.append(questionAndAnswer["question"])
        commentList.append(questionAndAnswer['comment'])
        legalPrinciples.append('Não preenchido')


    df = pd.DataFrame({"question":questionsList, "comment":commentList, "legalPrinciples": legalPrinciples})
    df.to_csv(f'../parsedTests/OAB-{oabNumber}.csv', index=False)
    df.to_excel(f'../parsedTests/OAB-{oabNumber}.xlsx', index=False, engine="openpyxl")

OAB38CSV = "../parsedTests/OAB-38.csv"
OAB39CSV = "../parsedTests/OAB-39.csv"
OAB40CSV = "../parsedTests/OAB-40.csv"
OAB41CSV = "../parsedTests/OAB-41.csv"

oabCsvPathList = [OAB38CSV, OAB39CSV, OAB40CSV, OAB41CSV]

for oabCsvPath in oabCsvPathList:
    oabCsv = pd.read_csv(oabCsvPath)
    newCsvName =   oabCsvPath.split('/')[2].split('.')[0]
    
    allExtractedLawsResponse = processOabQuestions(oabCsv, 'gemini-2.0-flash')
    oabCsvLegalPrincipals = createLegalPrincipalsColumn(oabCsv, allExtractedLawsResponse)
    oabCsvLegalPrincipals.to_csv(f'../parsedTests/{newCsvName}.csv', index=False)
    oabCsvLegalPrincipals.to_excel(f'../parsedTests/{newCsvName}.xlsx', index=False, engine="openpyxl")
    print(f'Csv {newCsvName} Gerado')


    
