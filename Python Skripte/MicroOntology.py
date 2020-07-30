import os
import csv
import time

epsSingletonNodes = []
epsCombNodes = []
epsNodes = []
rg = []
rs429358Nodes = []
rs7412Nodes = []
rsCombNodes = []
rs429358isPartOfEdges = []
rs7412isPartOfEdges = []
belongsToEdges = []
isIncludedInEdges = []
correspondsToEdges = []
rs7412refersToEdges = []
rs429358refersToEdges = []

pathHeaderNodes = '/Users/Tobias/Documents/Uni/Bachelorarbeit/CSVExport/import2/CSVHeaderFiles/nodes'
pathHeaderRelations = '/Users/Tobias/Documents/Uni/Bachelorarbeit/CSVExport/import2/CSVHeaderFiles/relations'
pathNodes = '/Users/Tobias/Documents/Uni/Bachelorarbeit/CSVExport/import2/nodes'
pathRelations = '/Users/Tobias/Documents/Uni/Bachelorarbeit/CSVExport/import2/relations'


def createPath():
    # create directories
    os.makedirs(pathHeaderNodes)
    os.makedirs(pathHeaderRelations)
    os.makedirs(pathNodes)
    os.makedirs(pathRelations)

class eps:
    def __init__(self, _i):
        self.epsID = 'epsilon' + str(_i)
        
def createEpsNodes():
    for k in [1,2,3,4]:
        tempEps = eps(k)
        epsSingletonNodes.append(tempEps)
        
class riskgroup():
    def __init__(self, _risk):
        self.riskID = _risk
        self.identifier = _risk
        self.category = 'rg'
        
def createRiskGroups():
    #low, medium, high
    rg.append(riskgroup('low'))
    rg.append(riskgroup('medium'))
    rg.append(riskgroup('high'))
  
    
class rs429358:
    def __init__(self, _snp):
        self.rsID = _snp
        self.label = 'rs429358'
        
class rs7412:
    def __init__(self, _snp):
        self.rsID = _snp
        self.label = 'rs7412'
        
class rsCombination:
    def __init__(self, _first, _second, _third, _fourth):
        self.rsCombID = str(_first.rsID) + str(_second.rsID) + str(_third.rsID) + str(_fourth.rsID)
        self.rs429358Tupel = [_first.rsID, _second.rsID]
        self.rs7412Tuple = [_third.rsID, _fourth.rsID]
        self.rsComb = [_first.rsID, _second.rsID, _third.rsID, _fourth.rsID]
        
def createRsCombinations():
    # possible combination of SNPs for both rs codes
    for k in ['C', 'T']:
        tempRs429358 = rs429358(k)
        rs429358Nodes.append(tempRs429358)
        tempRs7412 = rs7412(k)
        rs7412Nodes.append(tempRs7412)

    # create rs4tuples
    #CCTT
    rsCombNodes.append(rsCombination(rs429358Nodes[0], rs429358Nodes[0], rs7412Nodes[1], rs7412Nodes[1]))
    #CTTT
    rsCombNodes.append(rsCombination(rs429358Nodes[0], rs429358Nodes[1], rs7412Nodes[1], rs7412Nodes[1]))
    #CTCT
    rsCombNodes.append(rsCombination(rs429358Nodes[0], rs429358Nodes[1], rs7412Nodes[0], rs7412Nodes[1]))
    #CCCT
    rsCombNodes.append(rsCombination(rs429358Nodes[0], rs429358Nodes[0], rs7412Nodes[0], rs7412Nodes[1]))
    #TTTT
    rsCombNodes.append(rsCombination(rs429358Nodes[1], rs429358Nodes[1], rs7412Nodes[1], rs7412Nodes[1]))
    #TTCT
    rsCombNodes.append(rsCombination(rs429358Nodes[1], rs429358Nodes[1], rs7412Nodes[0], rs7412Nodes[1]))
    #TTCC
    rsCombNodes.append(rsCombination(rs429358Nodes[1], rs429358Nodes[1], rs7412Nodes[0], rs7412Nodes[0]))
    #CTCC
    rsCombNodes.append(rsCombination(rs429358Nodes[0], rs429358Nodes[1], rs7412Nodes[0], rs7412Nodes[0]))
    #CCCC
    rsCombNodes.append(rsCombination(rs429358Nodes[0], rs429358Nodes[0], rs7412Nodes[0], rs7412Nodes[0]))

        
class epsilonComb:
    def __init__(self, _i, _j):
        self.epsCombID = str(_i.epsID) + str(_j.epsID)
        self.epsilon = [_i, _j]
        
def createEpsilonCombination():
    # e1/e1

    epsCombNodes.append(epsilonComb(epsSingletonNodes[0], epsSingletonNodes[0]))
    # e1/e2 etc
    epsCombNodes.append(epsilonComb(epsSingletonNodes[0], epsSingletonNodes[1]))
    epsCombNodes.append(epsilonComb(epsSingletonNodes[0], epsSingletonNodes[2]))
    epsCombNodes.append(epsilonComb(epsSingletonNodes[1], epsSingletonNodes[3]))
    epsCombNodes.append(epsilonComb(epsSingletonNodes[0], epsSingletonNodes[3]))
    epsCombNodes.append(epsilonComb(epsSingletonNodes[1], epsSingletonNodes[1]))
    epsCombNodes.append(epsilonComb(epsSingletonNodes[1], epsSingletonNodes[2]))
    epsCombNodes.append(epsilonComb(epsSingletonNodes[2], epsSingletonNodes[2]))
    epsCombNodes.append(epsilonComb(epsSingletonNodes[2], epsSingletonNodes[3]))
    epsCombNodes.append(epsilonComb(epsSingletonNodes[3], epsSingletonNodes[3]))

            
class edgeOnt:
    def __init__(self, _type, _startNode, _endNode):
        self.type = _type
        self.startNode = _startNode
        self.endNode = _endNode

def createEdgeOnts():
    
    # eps <-> C,T

    # eps1 has C,T
    rs429358refersToEdges.append(edgeOnt('429358refersTo', rs429358Nodes[0].rsID, epsSingletonNodes[0].epsID))
    rs7412refersToEdges.append(edgeOnt('7412refersTo', rs7412Nodes[1].rsID, epsSingletonNodes[0].epsID))

    
    # eps2 has T,T:
    rs429358refersToEdges.append(edgeOnt('429358refersTo', rs429358Nodes[1].rsID, epsSingletonNodes[1].epsID))
    rs7412refersToEdges.append(edgeOnt('7412refersTo', rs7412Nodes[1].rsID, epsSingletonNodes[1].epsID))
    
    # eps3 has T,C:
    rs429358refersToEdges.append(edgeOnt('429358refersTo', rs429358Nodes[1].rsID, epsSingletonNodes[2].epsID))
    rs7412refersToEdges.append(edgeOnt('7412refersTo', rs7412Nodes[0].rsID, epsSingletonNodes[2].epsID))
 
    # eps4 has C,C:
    rs429358refersToEdges.append(edgeOnt('429358refersTo', rs429358Nodes[0].rsID, epsSingletonNodes[3].epsID))
    rs7412refersToEdges.append(edgeOnt('7412refersTo', rs7412Nodes[0].rsID, epsSingletonNodes[3].epsID))
            
    # -------------------------------------------------------------------
    
    # rsComb has rs429358 and rs7412 
    
    #CCTT
    rs429358isPartOfEdges.append(edgeOnt('429358isPartOf', rs429358Nodes[0].rsID, rsCombNodes[0].rsCombID))
    rs7412isPartOfEdges.append(edgeOnt('7412isPartOf', rs7412Nodes[1].rsID, rsCombNodes[0].rsCombID))
    #CTTT
    rs429358isPartOfEdges.append(edgeOnt('429358isPartOf', rs429358Nodes[0].rsID, rsCombNodes[1].rsCombID))
    rs429358isPartOfEdges.append(edgeOnt('429358isPartOf', rs429358Nodes[1].rsID, rsCombNodes[1].rsCombID))
    rs7412isPartOfEdges.append(edgeOnt('7412isPartOf', rs7412Nodes[1].rsID, rsCombNodes[1].rsCombID))
    #CTCT
    rs429358isPartOfEdges.append(edgeOnt('429358isPartOf', rs429358Nodes[0].rsID, rsCombNodes[2].rsCombID))
    rs429358isPartOfEdges.append(edgeOnt('429358isPartOf', rs429358Nodes[1].rsID, rsCombNodes[2].rsCombID))
    rs7412isPartOfEdges.append(edgeOnt('7412isPartOf', rs7412Nodes[0].rsID, rsCombNodes[2].rsCombID))
    rs7412isPartOfEdges.append(edgeOnt('7412isPartOf', rs7412Nodes[1].rsID, rsCombNodes[2].rsCombID))
    #CCCT
    rs429358isPartOfEdges.append(edgeOnt('429358isPartOf', rs429358Nodes[0].rsID, rsCombNodes[3].rsCombID))
    rs7412isPartOfEdges.append(edgeOnt('7412isPartOf', rs7412Nodes[0].rsID, rsCombNodes[3].rsCombID))
    rs7412isPartOfEdges.append(edgeOnt('7412isPartOf', rs7412Nodes[1].rsID, rsCombNodes[3].rsCombID))
    #TTTT
    rs429358isPartOfEdges.append(edgeOnt('429358isPartOf', rs429358Nodes[1].rsID, rsCombNodes[4].rsCombID))
    rs7412isPartOfEdges.append(edgeOnt('7412isPartOf', rs7412Nodes[1].rsID, rsCombNodes[4].rsCombID))
    #TTCT
    rs429358isPartOfEdges.append(edgeOnt('429358isPartOf', rs429358Nodes[1].rsID, rsCombNodes[5].rsCombID))
    rs7412isPartOfEdges.append(edgeOnt('7412isPartOf', rs7412Nodes[0].rsID, rsCombNodes[5].rsCombID))
    rs7412isPartOfEdges.append(edgeOnt('7412isPartOf', rs7412Nodes[1].rsID, rsCombNodes[5].rsCombID))
    #TTCC
    rs429358isPartOfEdges.append(edgeOnt('429358isPartOf', rs429358Nodes[1].rsID, rsCombNodes[6].rsCombID))
    rs7412isPartOfEdges.append(edgeOnt('7412isPartOf', rs7412Nodes[0].rsID, rsCombNodes[6].rsCombID))
    #CTCC
    rs429358isPartOfEdges.append(edgeOnt('429358isPartOf', rs429358Nodes[0].rsID, rsCombNodes[7].rsCombID))
    rs429358isPartOfEdges.append(edgeOnt('429358isPartOf', rs429358Nodes[1].rsID, rsCombNodes[7].rsCombID))
    rs7412isPartOfEdges.append(edgeOnt('7412isPartOf', rs7412Nodes[0].rsID, rsCombNodes[7].rsCombID))
    #CCCC
    rs429358isPartOfEdges.append(edgeOnt('429358isPartOf', rs429358Nodes[0].rsID, rsCombNodes[8].rsCombID))
    rs7412isPartOfEdges.append(edgeOnt('7412isPartOf', rs7412Nodes[0].rsID, rsCombNodes[8].rsCombID))

    
    
    
    # -------------------------------------------------------------------
    
    # eps <-> eps comb
    
    belongsToEdges.append(edgeOnt('belongsTo', epsSingletonNodes[0].epsID, epsCombNodes[0].epsCombID))
    belongsToEdges.append(edgeOnt('belongsTo', epsSingletonNodes[0].epsID, epsCombNodes[1].epsCombID))
    belongsToEdges.append(edgeOnt('belongsTo', epsSingletonNodes[0].epsID, epsCombNodes[2].epsCombID))
    belongsToEdges.append(edgeOnt('belongsTo', epsSingletonNodes[0].epsID, epsCombNodes[4].epsCombID))
    
    belongsToEdges.append(edgeOnt('belongsTo', epsSingletonNodes[1].epsID, epsCombNodes[1].epsCombID))
    belongsToEdges.append(edgeOnt('belongsTo', epsSingletonNodes[1].epsID, epsCombNodes[3].epsCombID))
    belongsToEdges.append(edgeOnt('belongsTo', epsSingletonNodes[1].epsID, epsCombNodes[5].epsCombID))
    belongsToEdges.append(edgeOnt('belongsTo', epsSingletonNodes[1].epsID, epsCombNodes[6].epsCombID))
    
    belongsToEdges.append(edgeOnt('belongsTo', epsSingletonNodes[2].epsID, epsCombNodes[2].epsCombID))
    belongsToEdges.append(edgeOnt('belongsTo', epsSingletonNodes[2].epsID, epsCombNodes[6].epsCombID))
    belongsToEdges.append(edgeOnt('belongsTo', epsSingletonNodes[2].epsID, epsCombNodes[7].epsCombID))
    belongsToEdges.append(edgeOnt('belongsTo', epsSingletonNodes[2].epsID, epsCombNodes[8].epsCombID))
    
    belongsToEdges.append(edgeOnt('belongsTo', epsSingletonNodes[3].epsID, epsCombNodes[3].epsCombID))
    belongsToEdges.append(edgeOnt('belongsTo', epsSingletonNodes[3].epsID, epsCombNodes[4].epsCombID))
    belongsToEdges.append(edgeOnt('belongsTo', epsSingletonNodes[3].epsID, epsCombNodes[8].epsCombID))
    belongsToEdges.append(edgeOnt('belongsTo', epsSingletonNodes[3].epsID, epsCombNodes[9].epsCombID))
   
    # -------------------------------------------------------------------
            
    # eps comb <-> rs comb
    #CCTT
    #CTTT
    #CTCT
    #CCCT
    #TTTT
    #TTCT
    #TTCC
    #CTCC
    #CCCC
    
    # e1 = CT, e2 = TT, e3 = TC, e4 = CC
             
    # e1/e1 <-> CCTT
    # e1/e2 <-> CTTT
    # e1/e3 <-> CTCT
    # e2/e4 <-> CTCT
    # e1/e4 <-> CCCT
    # e2/e2 <-> TTTT
    # e2/e3 <-> TTCT    
    # e3/e3 <-> TTCC
    # e3/e4 <-> CTCC
    # e4/e4 <-> CCCC
    
    correspondsToEdges.append(edgeOnt('correspondsTo', epsCombNodes[0].epsCombID, rsCombNodes[0].rsCombID))
    correspondsToEdges.append(edgeOnt('correspondsTo', epsCombNodes[1].epsCombID, rsCombNodes[1].rsCombID))
    correspondsToEdges.append(edgeOnt('correspondsTo', epsCombNodes[2].epsCombID, rsCombNodes[2].rsCombID))
    correspondsToEdges.append(edgeOnt('correspondsTo', epsCombNodes[3].epsCombID, rsCombNodes[2].rsCombID))
    correspondsToEdges.append(edgeOnt('correspondsTo', epsCombNodes[4].epsCombID, rsCombNodes[3].rsCombID))
    correspondsToEdges.append(edgeOnt('correspondsTo', epsCombNodes[5].epsCombID, rsCombNodes[4].rsCombID))
    correspondsToEdges.append(edgeOnt('correspondsTo', epsCombNodes[6].epsCombID, rsCombNodes[5].rsCombID))
    correspondsToEdges.append(edgeOnt('correspondsTo', epsCombNodes[7].epsCombID, rsCombNodes[6].rsCombID))
    correspondsToEdges.append(edgeOnt('correspondsTo', epsCombNodes[8].epsCombID, rsCombNodes[7].rsCombID))
    correspondsToEdges.append(edgeOnt('correspondsTo', epsCombNodes[9].epsCombID, rsCombNodes[8].rsCombID))
    
    # riskgroups
    
    # low risk <-> no e4
    isIncludedInEdges.append(edgeOnt('isIncludedIn', epsCombNodes[0].epsCombID, rg[0].riskID))
    isIncludedInEdges.append(edgeOnt('isIncludedIn', epsCombNodes[1].epsCombID, rg[0].riskID))
    isIncludedInEdges.append(edgeOnt('isIncludedIn', epsCombNodes[2].epsCombID, rg[0].riskID))
    isIncludedInEdges.append(edgeOnt('isIncludedIn', epsCombNodes[5].epsCombID, rg[0].riskID))
    isIncludedInEdges.append(edgeOnt('isIncludedIn', epsCombNodes[6].epsCombID, rg[0].riskID))
    isIncludedInEdges.append(edgeOnt('isIncludedIn', epsCombNodes[7].epsCombID, rg[0].riskID))
    # medium risk <-> one e4
    isIncludedInEdges.append(edgeOnt('isIncludedIn', epsCombNodes[3].epsCombID, rg[1].riskID))
    isIncludedInEdges.append(edgeOnt('isIncludedIn', epsCombNodes[4].epsCombID, rg[1].riskID))
    isIncludedInEdges.append(edgeOnt('isIncludedIn', epsCombNodes[8].epsCombID, rg[1].riskID))
    # high risk <-> two e4
    isIncludedInEdges.append(edgeOnt('isIncludedIn', epsCombNodes[9].epsCombID, rg[2].riskID))

def writeHeadersToCSV():
    #relations
    os.chdir(pathHeaderRelations)
    headerName = 'belongsTo-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(epsID)', ':END_ID(epsCombID)', 'type'])
        
    headerName = 'isIncludedIn-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(epsCombID)', ':END_ID(riskID)', 'type'])
    
    headerName = 'rs7412isPartOf-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(rs7412ID)', ':END_ID(rsCombID)', 'type'])
        
    headerName = 'rs429358isPartOf-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(rs429358ID)', ':END_ID(rsCombID)', 'type'])
    
    headerName = '7412refersTo-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(rs7412ID)', ':END_ID(epsID)', 'type'])
        
    headerName = '429358refersTo-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(rs429358ID)', ':END_ID(epsID)', 'type'])
        
    headerName = 'correspondsTo-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(epsCombID)', ':END_ID(rsCombID)', 'type'])
    
    #nodes
    os.chdir(pathHeaderNodes)
    headerName = 'riskgroups-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow(['riskgroup:ID(riskID)'])
    
    headerName = 'epsilon-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow(['epsilon:ID(epsID)'])
        
    headerName = 'riskgroup-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow(['riskgroup:ID(riskID)', 'identifier', 'category'])
        
    headerName = 'rs429358-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow(['rs429358:ID(rs429358ID)', 'label'])
    
    headerName = 'rs7412-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow(['rs7412:ID(rs7412ID)', 'label'])
        
    headerName = 'rsCombination-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow(['rsComb:ID(rsCombID)'])
    
    headerName = 'epsilonCombination-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow(['epsComb:ID(epsCombID)'])
        
epsSingletonNodes = []
epsCombNodes = []
epsNodes = []
rg = []
rs429358Nodes = []
rs7412Nodes = []
rsCombNodes = []
isPartOfEdges = []
belongsToEdges = []
isIncludedInEdges = []
correspondsToEdges = []
refersToEdges = []

def writeRgToCSV():
    os.chdir(pathNodes)
    fileName = 'riskgroups.csv'
    with open(fileName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)
        for element in rg:
            writeCSV.writerow([element.riskID, element.identifier, element.category])

def writeEpsilonToCSV():
    os.chdir(pathNodes)
    fileName = 'epsilon.csv'
    with open(fileName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)
        for element in epsSingletonNodes:
            writeCSV.writerow([element.epsID])
            
def writeEpsilonCombinationToCSV():
    os.chdir(pathNodes)
    fileName = 'epsilonCombination.csv'
    with open(fileName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)
        for element in epsCombNodes:
            writeCSV.writerow([element.epsCombID])
            
def writeRs429358ToCSV():
    os.chdir(pathNodes)
    fileName = 'rs429358.csv'
    with open(fileName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)
        for element in rs429358Nodes:
            writeCSV.writerow([element.rsID, element.label])
            
def writeRs7412ToCSV():
    os.chdir(pathNodes)
    fileName = 'rs7412.csv'
    with open(fileName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)
        for element in rs7412Nodes:
            writeCSV.writerow([element.rsID, element.label])

def writeRsCombToCSV():
    os.chdir(pathNodes)
    fileName = 'rsCombination.csv'
    with open(fileName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)
        for element in rsCombNodes:
            writeCSV.writerow([element.rsCombID])            

def writeNodesToCSV():
    writeRgToCSV()
    writeEpsilonToCSV()
    writeEpsilonCombinationToCSV()
    writeRs429358ToCSV()
    writeRs7412ToCSV()
    writeRsCombToCSV()
    
def writeEdgesFromListToCSV(_list, _type):
    os.chdir(pathRelations)
    fileName = str(_type) + '.csv'
    with open(fileName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)
        for element in _list:
            writeCSV.writerow([element.startNode, element.endNode, element.type])
        
def writeEdgesToCSV():
    writeEdgesFromListToCSV(rs7412isPartOfEdges, 'rs7412isPartOf')
    writeEdgesFromListToCSV(rs429358isPartOfEdges, 'rs429358isPartOf')
    writeEdgesFromListToCSV(belongsToEdges, 'belongsTo')
    writeEdgesFromListToCSV(isIncludedInEdges, 'isIncludedIn')
    writeEdgesFromListToCSV(correspondsToEdges, 'correspondsTo')
    writeEdgesFromListToCSV(rs7412refersToEdges, 'rs7412refersTo')
    writeEdgesFromListToCSV(rs429358refersToEdges, 'rs429358refersTo')
    
def writeToCSV():
    writeHeadersToCSV()
    writeNodesToCSV()
    writeEdgesToCSV()
           
def createAll():
    tic = time.time()
    createPath()
    createEpsNodes()
    createRiskGroups()
    createRsCombinations()
    createEpsilonCombination()
    createEdgeOnts()
    writeToCSV()
    toc = time.time()
    # timer
    print("--- %s seconds ---" % (toc - tic))
    for element in epsCombNodes:
        print(element.epsCombID)
    
    
createAll()
    

        
