import numpy as np
import pandas as pd
from pydantic import BaseModel
import requests 
import json 
import time


def setUpGeminiToExtractLaws(modelName, prompt):
    modelName = modelName.replace("google/", "")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelName}:generateContent?key=[API_KEY]" 

    headers = { 
        'Content-Type': 'application/json'
    }

    requestParams = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "response_mime_type": "application/json",
                "response_schema": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT", 
                        "properties": {
                            "QuestionNumber": {"type": "STRING"},
                            "legalPrinciples": {
                                "type": "ARRAY", 
                                "items": {"type": "STRING"}
                            }
                        }
                    }
                }
            }
        }
    response = requests.post(url, headers = headers, json = requestParams) 
    response = response.json()['candidates'][0]['content']['parts'][0]['text']
    responsesList = list()
    responsesList.append(dict())
    responsesList[0]['generated_text'] = response
    time.sleep(30)
    return responsesList    


def processOabQuestions(oab_exam_df, model_name):
    responses = []
    for index, comment in enumerate(oab_exam_df['comment'], start=1):  # Apenas percorre a coluna 'comment'
        print(index)
        prompt = f"""A partir de agora você deve atuar como um crawler que extrai informações jurídicas de um texto.
Estou construindo um dataframe sobre a prova da OAB no qual possuo as seguintes colunas: questão, comentário,
principiosJuridicos. A questão é a questão da prova, o comentário é o comentário explicando a resposta correta dessa questão
e principiosJuridicos são os conhecimentos jurídicos necessários para construir essa questão como por exemplo: artigos,
leis, constituição, jurisprudência, doutrina, Súmulas, Orientações, tratados, normas, principios e etc. Você deve analisar o
comentário sobre uma das questões abaixo e extrair desse texto todos os princípios jurídicos necessários para
responder a alternativa correta. Não invente nem adicione nenhum elemento além dos fornecidos no texto.

Comentário Questão {index}:
{comment}

Retorne esses dados na estrutura pedida:
{{"QuestionNumber": "str", "legalPrinciples": ["str"]}}
"""
        
        response = setUpGeminiToExtractLaws(model_name, prompt)
        responses.append(response)
    
    return responses


def createLegalPrincipalsColumn(oab_exam_df, all_responses):
    for i, response in enumerate(all_responses):
        if response and isinstance(response, list) and 'generated_text' in response[0]:
            extracted_data = json.loads(response[0]['generated_text'])  # Convertendo string JSON para lista de dicionários
            if extracted_data:
                oab_exam_df.at[i, 'legalPrinciples'] = ", ".join(extracted_data[0]['legalPrinciples'])
    return oab_exam_df