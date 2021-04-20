alphabeth = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']


#Функция взлома шифра гаммирования
def hack(code):
    codeLen = len(code)

    #Подобрать длину гаммы
    gammaLen = -1
    n = 0
    for n in range(2, codeLen // 2):
        #Формируем столбец
        col = []
        for i in range(0, codeLen, n):
            col.append(code[i])

        #Посчитать индекс Фридмана для каждого нулевого столбика для всех длин,
        #взять за эталонную первую, при которой индекс будет максимально близок к 0.066
        symbolsCount = [0 for i in range(26)]
        for symb in col:
            symbolsCount[alphabeth.index(symb)] += 1

        FriedmanIndex = 0
        for i in range(len(symbolsCount)):
            FriedmanIndex += (symbolsCount[i] * (symbolsCount[i] - 1)) / (len(col) * (len(col) - 1))

        #Проверить индекс на попадание в диапазон
        #if abs(FriedmanIndex - 0.066) < 0.006:
        if FriedmanIndex > 0.053:
            #Если попал, берем n за эталон и уходим
            gammaLen = n
            break

    print('gamma len = ', gammaLen)

    #Теперь можно определить саму гамму

    #Разбиваем текст на столбцы по этой длине гаммы
    #формируем подстроки
    rows = [] #блоки(строки)
    for i in range(0, codeLen - gammaLen, gammaLen): #без последнего блока
        row = [ code[i + j] for j in range(gammaLen)]
        rows.append(row)

    #формируем столбцы
    collumns = []
    for k in range(n): #выбираем номер столбца
        collumn = []
        for i in range(len(rows)): #выбираем строку
            collumn.append(rows[i][k])
        collumns.append(collumn)

    #Находим относительные сдвиги столбцов с помощью взаимного индекса Фридмана(совпадений)
    slides = []
    for n in range(1, gammaLen):
        #Находим встречаемость каждого символа в первом столбике
        firstSymbolsCount = [0 for i in range(26)]
        for symb in collumns[n - 1]:
            firstSymbolsCount[alphabeth.index(symb)] += 1

        #Ищем сдвиг для второго столбца такой, чтобы взаимный индекс Фридмана был близок к 0.066
        for m in range(26):
            #сдвинуть второй столбец
            slideSecondCol = []
            for symb in collumns[n]:
                slideSecondCol.append(alphabeth[(alphabeth.index(symb) + m) % 26])

            #Находим встречаемость каждого символа во втором столбике 
            secondSymbolsCount = [0 for i in range(26)]
            for symb in slideSecondCol:
                secondSymbolsCount[alphabeth.index(symb)] += 1

            #Находим взаимный индекс Фридмана
            FriedmanIndex = 0
            for i in range(len(firstSymbolsCount)):
                FriedmanIndex = FriedmanIndex + ((firstSymbolsCount[i] * secondSymbolsCount[i]) / (len(collumns[n])**2))

            #Проверяем диапазон
            #if abs(FriedmanIndex - 0.066) < 0.006:
            if FriedmanIndex > 0.053:
                #Если попали, запоминаем это смещение и останавливаем перебор
                slides.append((26 - m) % 26)
                break

    #У нас есть взаимные сдвиги всех столбцов, теперь нужно найти сдвиг первого
    #искать будем с помощью частотного анализа символов(как в шифре Цезаря)
    currentSymbolsFreq = [0 for i in range(26)]
    for symb in collumns[0]:
        currentSymbolsFreq[alphabeth.index(symb)] += 1
    for i in range(len(currentSymbolsFreq)):
        currentSymbolsFreq[i] = currentSymbolsFreq[i] / len(collumns[0]) * 100

    #Находим все возможные сдвиги для первого столбца
    slidesOfFirstCol = []
    for i in range(len(currentSymbolsFreq)):
        for j in range(len(currentSymbolsFreq)):
            if abs(currentSymbolsFreq[i] - currentSymbolsFreq[j]) < 0.12: #0.25
                slidesOfFirstCol.append(i - j)

    #Берем за эталонное такое смещение, которое встречалось чаще всего
    finalSlide = slidesOfFirstCol[0]
    maximum = slidesOfFirstCol.count(slidesOfFirstCol[0])
    for slide in slidesOfFirstCol:
        if slidesOfFirstCol.count(slide) > maximum:
            maximum = slidesOfFirstCol.count(slide)
            finalSlide = slide

    #Посчитать сдвиги для столбиков, зная сдвиг первого
    finalSlides = []
    finalSlides.append(finalSlide)
    for slide in slides:
        finalSlides.append(slide)
    #считаем сдвиги столбиков
    for i in range(1, len(finalSlides)):
        finalSlides[i] = (finalSlides[i-1] + finalSlides[i]) % 26

    #Мы нашли гамму в виде сдвигов, осталось преобразовать ее в слово
    gamma = []
    for slide in finalSlides:
        gamma.append(alphabeth[slide])

    return ''.join(gamma)
    
def main():
    print(hack("snmdtgimgrtzkdthmd"))
    
if __name__ == '__main__':
    main()
