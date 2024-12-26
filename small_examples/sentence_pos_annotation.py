import stanza

nlp = stanza.Pipeline(lang='ko', processors='tokenize,pos')

doc = nlp('1980년 초부터 국회와 정부는 유신 헌법을 철폐하기 위한 개헌 논의를 진행했고, 대학생과 재야 세력도 정치 일정 제시와 전두환 퇴진 요구를 바탕으로 민주화 시위를 벌였다.')
for sent in doc.sentences:
    for word in sent.words:
        print(*[f'{word.text} - {word.upos}'], sep='\n')
