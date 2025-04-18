import re

def pdfTextExtractor(pdf, txtFilePath):

    allText = ''
    pageIndex = 0

    for page in pdf.pages:
        if pageIndex > 1:
            allText += page.extract_text()
        pageIndex += 1

    with open(txtFilePath, "w", encoding="utf-8") as f:
        f.write(allText)

import re

def buildQuestionAndCommentDictionaryArray(textFilePath):
    with open(textFilePath, "r", encoding="utf-8") as f:
        text = f.read()

    is_oab_39 = "oab39" in textFilePath.lower()

    questions = []

    # Regex para identificar todas as ocorrências de questões
    pattern = r"(QUESTÃO\s+\d+\s*\.?.*?)(?=QUESTÃO\s+\d+\s*\.?|$)"
    blocks = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

    # Regex para detectar "Comentários" em linha isolada (com tolerância a OCR quebrado)
    comentario_regex = re.compile(
        r"(?:(?:\n|\A)\s*)(Com\s*e?n?t?\s*[áa]?\s*r?\s*i?\s*o?\s*s?)(?=\s*\n)",
        re.IGNORECASE
    )

    added_q70 = False
    seen_numbers = set()

    for block in blocks:
        block = block.strip()

        # número da questão
        num_match = re.match(r"QUESTÃO\s+(\d+)", block)
        if not num_match:
            continue
        qnum = num_match.group(1)

        if qnum in seen_numbers:
            continue
        seen_numbers.add(qnum)

        # Tratamento especial para OAB 39 - questão 70
        if is_oab_39 and qnum == "70" and not added_q70:
            alt_c_regex = re.search(r"A alternativa correta é (a|a letra)?\s*[Cc]\s*[\.]?", block)
            if alt_c_regex:
                split_index = alt_c_regex.start()
                question = block[:split_index].strip()
                comment = block[split_index:].strip()
            else:
                question = block.strip()
                comment = ""
            questions.append({
                "question": question,
                "comment": comment
            })
            added_q70 = True
            continue

        # Separar comentário se houver marcador "Comentários" (em linha isolada)
        comentario_match = comentario_regex.search(block)
        if comentario_match:
            split_index = comentario_match.start()
            question_text = block[:split_index].strip()
            comment_text = block[split_index:].strip()
        else:
            question_text = block.strip()
            comment_text = ""

        questions.append({
            "question": question_text,
            "comment": comment_text
        })

    return questions




