A="""0 1	2	3	1	4	3	2	1	4	2	6
4	1	2	7	1	4	3	2	1	4	6	7
4	1	2	8	5	4	7	2	1	8	6	7
4	1	2	3	1	4	7	2	1	8	2	7
4	1	2	8	1	4	7	2	1	4	2	7
4	1	2	8	1	4	7	2	1	8	6	7
4	1	2	8	1	4	7	2	1	8	2	7
"""
B=A.split()
C=[int(val) for val in B]
D=C[72:84]

def mex(L):
    if L==[0]: return 1
    newL=list(set(L))
    newL.sort()
    for i in range(len(newL)):
        if newL[i]!=i: return i
    return len(newL)

def calculateKayles(n):
    assert(n>=0)
    global C
    global D
    if n<=83:
        return C[n]
    else:
        i=n%12
        return D[i]

assert(calculateKayles(0)==0)
assert(calculateKayles(1)==1)
assert(calculateKayles(83)==7)
assert(calculateKayles(83)==7)
assert(calculateKayles(25)==1)

class yGame(object):

    def __init__(self, gameArray, yDict=dict()):
        self.gameArray=gameArray
        self.yDict=yDict

    def is_valid_gameArray(self): #gameArray -> Boolean
        for val in gameArray:
            if val!=1:
                return False
        return True

    """
    def get_next_states(self): #yGame -> yGame list
        if self.isKayles:
            assert(False)
        else: #self.isKayles==False
            for i in range(len(self.gameArray)-1): pass
    """

    def calculateNimber(self):
        array=self.gameArray
        nimberList=[]
        if len(array) in self.yDict:
            return self.yDict[len(array)]
        else: #not Kayles yo
            assert(len(array)>=3)
            nimberList.append(calculateKayles(len(array)-1))
            nimberList.append(calculateKayles(len(array)-2))
            nimberList.append(calculateKayles(len(array)-3))
            nimberList.append(calculateKayles(len(array)-3)^1)
            nimberList.append(calculateKayles(len(array)-3)^2)
            if len(array)>=4:
                nimberList.append(calculateKayles(len(array)-4)^2)
                nimberList.append(yGame(array[:len(array)-1], self.yDict).calculateNimber())
            for i in range(3, len(array)-1):
                LHS=array[0:i]
                RHS1_nim=calculateKayles(len(array[i+1:]))
                RHS2_nim=calculateKayles(len(array[i+2:]))
                LHS_nim = yGame(LHS, self.yDict).calculateNimber()
                nimberList.append(LHS_nim^RHS1_nim)
                nimberList.append(LHS_nim^RHS2_nim)
            nim=mex(nimberList)
            #print nimberList
            self.yDict[len(array)]=nim
            return nim




        """
            for i in range(len(array)-1):
                #maybe this
                LHS = array[0:i-1] if i>=1 else []
                RHS1_nim = calculateKayles(len(array[i+1:len(array)]))
                RHS2_nim = calculateKayles(len(array[i+2:len(array)]))
                RHS3_nim = (None if i!=0
                    else calculateKayles(len(array[i+3:len(array)])))
                if RHS3_nim!=None:
                    nimberList.append(RHS3_nim)
                if len(LHS) in self.yDict:
                    nimberList.append(self.yDict[len(LHS)]^RHS1_nim)
                    nimberList.append(self.yDict[len(LHS)]^RHS2_nim)

                else:
                    LHS_nim = yGame(LHS, False, self.yDict).calculateNimber()
                    self.yDict[len(LHS)]=LHS_nim
                    nimberList.append(LHS_nim^RHS1_nim)
                    nimberList.append(LHS_nim^RHS2_nim)
        """
yDict=dict()

array1=[1,1]
array2=[1,1,1]
array3=[1,1,1,1]


nims=[0,1,2]
for i in range(3, 1500):
    array=[1 for l in range(i)]
    nims.append(yGame(array, yDict).calculateNimber())
start=5
for i in range(120):
    print i, nims[start:start+12]
    start+=12
