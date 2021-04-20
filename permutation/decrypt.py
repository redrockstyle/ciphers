#Функция дешифрования кода с помощью перестановки permutation
def decrypt(code, permutation):
    blockSize = len(permutation)
    codeSize = len(code)
 
    #Дешифрование
    for i in range(0, codeSize, blockSize):
        string = [ code[i+j] for j in range(blockSize)]
        for j in range(blockSize):
            code[i + j] = string[permutation[j]]
 
    return