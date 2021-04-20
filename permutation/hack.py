#Функция взлома шифра перестановки
def hack(codeFileName):
    #Считываем код из файла
    file = open(codeFileName, 'r')
    code = list(file.read())
    file.close()
 
    codeSize = len(code)
 
    #Найти все возможные делители длины текста
    dividers = []
    for n in range(2, codeSize, 1):
        if codeSize % n == 0:
            dividers.append(n)
 
    #Формируем блоки длины n, не берем в рассчет последний, потому что там рандомные добитки
    currentPermutationSize = 0
    for n in dividers:
        #формируем подстроки
        rows = [] #блоки(строки)
        for i in range(0, codeSize-n, n): #codeSize-n без последнего блока
            row = [ code[i+j] for j in range(n)]
            rows.append(row)
 
 
        #формируем столбцы
        collums = []
        for k in range(n): #выбираем номер столбца
            collum = []
            for i in range(len(rows)): #выбираем строку
                collum.append(rows[i][k])
            collums.append(collum)
        
        '''
        Подставлять столбцы справа и слева, если появилась запрещенная биграмма
        подставить другой, если запретных биграмм нет хотя бы в одной подстановке столбцов,
        берем эту длину перестановки за эталонную. БЕРЕМ ПЕРВУЮ ТАКУЮ ДЛИНУ, потому что дальше
        будут подходить ее множители (если эталонная 12, то и 24 тоже подойдет)
        '''
        findGoodBigrammFlag = False #Флаг, что нашлась подстановка без плохих биграмм
        for i in range(len(collums)): #i - номер столбца, к которому подставляем
            for j in range(len(collums)): #j - номер столбца, который подставляем
                if i == j: #так мы переберем все подстановки столбцов
                    continue
 
                #Составляем список всех биграмм с текущими столбиками
                bigramms = [ collums[i][k] + collums[j][k] for k in range(len(collums[i]))]
 
                '''
                Теперь нужно проверить, есть ли запретные биграммы в такой подстановке столбцов
                если хотя бы в одной подстановке столбцов нет запрещенных биграмм, то
                скорее всего такая длинна эталонная
                '''
                findBadBigrammFlag = False
                for bigramm in bigramms:
                    if bigramm in badBigramms:
                        #Нашли плохую биграмму в такой подстановке столбцов
                        findBadBigrammFlag = True
 
                #Если в такой подстановке столбцов для этой n НЕ БЫЛО плохих биграмм, то
                #эта n наща эталонная
                if findBadBigrammFlag == False:
                    findGoodBigrammFlag = True
 
        #забираем нашу n и уходим из беребора делителей
        if findGoodBigrammFlag == True:
            currentPermutationSize = n
            break
 
    print('currentPermutationSize: ', currentPermutationSize)
 
    '''
    Есть длина, теперь можно найти саму перестановку.
    Будем подставлять столбцы слева и справа. Тем самым формируя текст. Гарантированно, что
    для каждого i-го столбика к нему справа или слева можно подставить ВСЕГО один какой-нибудь столбец
    '''
 
    #формируем блоки для данной длины перестановки
    rows = [] #блоки(строки)
    for i in range(0, codeSize-currentPermutationSize, currentPermutationSize):
        row = [ code[i+j] for j in range(currentPermutationSize)]
        rows.append(row)
 
    #формируем столбцы
    collums = []
    for k in range(currentPermutationSize): #выбираем номер столбца
        collum = []
        for i in range(len(rows)): #выбираем строку
            collum.append(rows[i][k])
        collums.append(collum)
 
    #задача: подставлять столбцы справа и слева к нулевому
    #Если подставить удалось, запомнили это и подставляем к получившемуся еще один справа или слева и так далее
    collumsPositions = [0] #Массив позици столбцов. В начале [0] это стоит только нулевой столбец
    #Если массив [1,0,2] - это значит что мы смогли к нулевому столбцу слева подставить 1, а справа 2
    usedIndexes = [0] #индексы уже подставленных столбцов, их мы больше не подставляем
    while len(collumsPositions) != currentPermutationSize: #вайл до тех пор, пока не подставим все столбцы
        for i in range(len(collums)): #берем какой-то столбец
            if i in usedIndexes: #Проверяем, что еще его не брали
                continue
            #подставляем справа
            bigramms = [ collums[collumsPositions[len(collumsPositions)-1]][k] + collums[i][k] for k in range(len(collums[i]))]
 
            findBadBigrammFlag = False
            for bigramm in bigramms:
                if bigramm in badBigramms:
                    findBadBigrammFlag = True
 
            #Если смогли подставить столбец i справа без плохих биграмм
            if findBadBigrammFlag == False:
                #Формируем правильный список. Добавили справа
                collumsPositions.append(i)
                usedIndexes.append(i)
 
            #подставляем слева
            bigramms = [ collums[i][k] + collums[collumsPositions[0]][k] for k in range(len(collums[i]))]
 
            findBadBigrammFlag = False
            for bigramm in bigramms:
                if bigramm in badBigramms:
                    findBadBigrammFlag = True
 
            #Если смогли подставить столбец i слева без плохих биграмм
            if findBadBigrammFlag == False:
                #Формируем правильный список. Добавили слева
                #Вставки в начало листа нет, поэтому создаем новый и пишем туда, что было
                temp = [i] #i-ый столбец ставим слева
                for k in collumsPositions:
                    temp.append(k)
                collumsPositions = temp
                usedIndexes.append(i)
 
    #Выводим на экран позиции, согласно которым нужно слепить столбики
    print(collumsPositions)
 
    #Получили позиции столбцов, осталось вывести текст в этом порядке и все!
    text = []
    for i in range(len(collums[0])):
        for j in range(len(collumsPositions)):
            text.append(collums[collumsPositions[j]][i])
 
    print('text:')
    print(''.join(text))
 
    return text