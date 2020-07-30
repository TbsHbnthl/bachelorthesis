import csv
import os
import time

# datatypes = [personID, siteAbbreviation, visitNo, sex, rg, diagnosis, HG]
#----------------------------------------------------------------------------------------------------------------------
# specify paths to store csv files
pathHeaderNodes = '/Users/Tobias/Documents/Uni/Bachelorarbeit/CSVExport/import/CSVHeaderFiles/nodes'
pathHeaderRelations = '/Users/Tobias/Documents/Uni/Bachelorarbeit/CSVExport/import/CSVHeaderFiles/relations'
pathNodes = '/Users/Tobias/Documents/Uni/Bachelorarbeit/CSVExport/import/nodes'
pathRelations = '/Users/Tobias/Documents/Uni/Bachelorarbeit/CSVExport/import/relations'
pathFile = '/Users/Tobias/Documents/Uni/Bachelorarbeit/TestdatenJensArtifiziell.csv'
#----------------------------------------------------------------------------------------------------------------------
# lists for temporal storage of values from csv file (prevent duplicates)
personId = set()
visitSite = set()
visitNo = set()
sex = set()

#----------------------------------------------------------------------------------------------------------------------
# store objects from file reader

# stores sexNodes
sexNodes = []
# store patient objects
patientNodes = []
# store entity nodes:
# all entities together
entityNodes = []
# separated by label
rgNodes = []
hgNodes = []
diagnNodes = []
# store unstructured values
unstructuredNodes = []
# store source nodes
sourceNodes = []
sourceAllNodes = []
# hasSourceTogether = []

# relation types for edges (inspired by dublin core schema)
relType = ['hasSex', 'patientHasSource', 'hasPatient', 'hasDiagnosis', 'hasGeneNomenclature', 'hasValue', 'isSubSource', 'entityHasSourceAll', 'unstructuredHasSourceAll', 'patientHasSourceAll', 'hasEpsCombination', 'rgHasSourceAll', 'epsilonCombinationHasSourceAll']

# edge patientNode-[hasSex]->sexNode
patSex = []
# edge patientNode-[hasSource(All)]->source(All)Node
patSourceAll = []
patSource = []
# edge patientNode<-[hasRelation]->entityNode
patRg = []
patHg = []
patDiagn = []
patEpsComb = []
# edge patientNode-[hasValue]->unstructuredNode
patUn = []
# edge entityNode-[hasSource]->sourceAllNode
rgSourceAll = []
diagnSourceAll = []
hgSourceAll = []
epsCombSourceAll = []
# edge unstructuredNode-[hasSource]->sourceAllNode
unSourceAll = []
# edge sourceAll-[isSubSource]-source
sASource = []
#----------------------------------------------------------------------------------------------------------------------

# dictionary for riskgroups:

epsRgDict = {
    'epsilon1epsilon1': 'low',
    'epsilon1epsilon2': 'low',
    'epsilon1epsilon3': 'low',
    'epsilon2epsilon2': 'low',
    'epsilon2epsilon3': 'low',
    'epsilon3epsilon3': 'low',
    'epsilon1epsilon4': 'medium',
    'epsilon2epsilon4': 'medium',
    'epsilon3epsilon4': 'medium',
    'epsilon4epsilon4': 'high'    
    }


#----------------------------------------------------------------------------------------------------------------------

# node classes
# uri not given
class nodeEntity:
    def __init__(self, _entityID, _source, _id, _preferredLabel, _uri):
        self.entityID = _entityID
        self.source = _source
        self.id = _id
        self.preferredLabel = _preferredLabel
        # self.uri = _uri

class sexNode:
    def __init__(self, _sex):
        self.sex = _sex

class unstructuredNode:
    def __init__(self, _unstructuredID, _value, _uri):
        self.unstructuredID = _unstructuredID
        self.value = _value
        # self.uri = _uri

class patientNode:
    def __init__(self, _id):
        self.id = _id

class sourceNode:
    def __init__(self, _sourceID, _source, _site):
        self.sourceID = _sourceID
        self.source = _source
        self.site = _site
        
class sourceAllNode:
    def __init__(self, _sourceAllID, _source, _site, _provenance):
        self.sourceAllID = _sourceAllID
        self.source = _source
        self.site = _site
        self.provenance = _provenance



#----------------------------------------------------------------------------------------------------------------------

# edge class

class edge:
    def __init__(self, _type, _provenance, _startNode, _endNode, _time):
        self.provenance = _provenance
        self.type = _type
        self.time = _time
        self.startNode = _startNode
        self.endNode = _endNode
        # source/sourceAll

#----------------------------------------------------------------------------------------------------------------------

# function that reads csv file, splits information and allocate to different objects

def impCSVFile(_filename):

    with open(_filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        

        # provenance dummy for test data
        provenance = -1
        # placeholder uri
        uriPlaceholder = 0
        # check first line
        firstLine = True

        # create source:
        source = _filename

        # iterate through all rows
        for row in readCSV:
            
            # helping variables
            tempPatientId = None
            tempVisitNumber = None
            tempSex = 'female'
            tempSite = None
            tempProv = None
            tempRg = None
            #tempRiskGroup = None
            tempDiagn = None
            tempEpsCombId = None
            avoidDoubleRel = True

            # skip first row (header)
            if firstLine:
                firstLine = False
                continue

            # raise provenance for this row
            provenance += 1

            # split first entry into three parts visit = [patientID, visitSite, visitNumber]
            # e.g. 0_BN_1
            visit = row[0].split('_')
            # split last entry into parts (split HGNC markers)
            l = len(row)
            # "['HGNC_XXXX', 'HGNC_YYYY', 'HGNC_ZZZZ']"
            # listHGNCValues = [HGNC_XXXX, HGNC_YYYY,...]
            listHGNCValues = row[l-1].strip('][').split(', ')            

            # check for doubles and otherweise create person and add it to duplicates and nodes
            # visit[0] is patient-id
            tempPatientId = visit[0]
            if tempPatientId not in personId:
                avoidDoubleRel = False
                personId.add(visit[0])
                createPerson(visit[0])
            
            # visit[1] is site
            # create attributes for sourceAll node
            tempSite = 'site_' + str(visit[1])
            tempProv = 'provenanceID_' + str(provenance)
            # as each line in the csv file is assigned to a unique provenance, there is no need to filter with if-clause
            # creates sourceAll node and stores it in list, sourceALl-ID can therefore be the provenance
            createSourceAll(tempProv, source, visit[1], provenance)
            # check for doubles and otherweise create site and add it to duplicates and nodes
            if visit[1] not in visitSite:
                visitSite.add(visit[1])
                # here siteID is used as sourceID because of the limited given set of data
                # Normally data sets would come from different locations, creating different sources witch could
                # then be categorized by their siteID as a sourceID as well.
                # createEntity(sourceID, source, visit[1], 'visitSite', uriPlaceholder)
                createSource(tempSite, source, visit[1])
            # visit[2] is visit number
            tempVisitNumber = 'visitNumber_' + str(visit[2])
            if visit[2] not in visitNo:
                visitNo.add(visit[2])
                createUnstData(tempVisitNumber, visit[2], uriPlaceholder)

            
            # at the beginning sex is set to female, in other cases change it
            if row[1] == '0':
               tempSex = 'male'
               
            tempDiagn = 'DO_' + str(row[3])
            
            # store espilons (given as 0-3, needed as 1-4)
            e1 = int(row[4]) + 1
            e2 = int(row[5]) + 1
            
            # create tempEpsId for edge to eps1/eps2 combination
            if e1 > e2:
                tempEpsCombId = 'epsilon' + str(e2) + 'epsilon' + str(e1)
            else:
                tempEpsCombId = 'epsilon' + str(e1) + 'epsilon' + str(e2)
            
            # find corresponding riskgroup 
            tempRg = epsRgDict[tempEpsCombId]

            # create edges
            
# relType = ['hasSex', 'patientHasSource', 'hasPatient', 'hasDiagnosis', 'hasGeneNomenclature', 'hasValue', 
#           'isSubSource', 'entityHasSourceAll', 'unstructuredHasSourceAll', 'patientHasSourceAll', 
#           'hasEpsCombination' ]

            
            # edge patientNode-[hasSex]->sexNode
            patSex.append(createEdges(relType[0], provenance, tempPatientId, tempSex, visit[2]))
            
            # edge patientNode-[patientHasSourceAll]->sourceAllNode
            patSourceAll.append(createEdges(relType[9], provenance, tempPatientId, tempProv, visit[2]))

            # edge patientNode<-[hasRelation]->entityNode (rg, epsilon, diagn, hg)
            # patient <-> riskgroup
            patRg.append(createEdges(relType[2], provenance, tempRg, tempPatientId, visit[2]))
            # patient <-> epsilon combination
            patEpsComb.append(createEdges(relType[10], provenance, tempPatientId, tempEpsCombId, visit[2]))
            # patient <-> diagnosis
            patDiagn.append(createEdges(relType[3], provenance, tempPatientId, tempDiagn, visit[2]))
            # patient <-> hgnc
            if listHGNCValues != ['']:
                for entry in listHGNCValues:
                    entry = entry.strip("'")
                    patHg.append(createEdges(relType[4], provenance, tempPatientId, entry, visit[2]))
                    # hgnc <-> sourceAll
                    hgSourceAll.append(createEdges(relType[7], provenance, entry, tempProv, visit[2]))
                
            # edge patientNode-[hasValue]->unstructuredNode (visit no)
            patUn.append(createEdges(relType[5], provenance, tempPatientId, tempVisitNumber, visit[2]))
            
            # edge unstructuredNode(visit no)-[hasSourceAll]->sourceAllNode
            unSourceAll.append(createEdges(relType[8], provenance, tempVisitNumber, tempProv, visit[2]))
            
            # edge entityNode-[hasSourceAll]->sourceNode (rg, diagn, epsilon)
            # rg <-> SourceAll
            rgSourceAll.append(createEdges(relType[7], provenance, tempRg, tempProv, visit[2]))
            # diagn <-> SourceAll
            diagnSourceAll.append(createEdges(relType[7], provenance, tempDiagn, tempProv, visit[2]))
            # epsilon combination <-> sourceAll
            epsCombSourceAll.append(createEdges(relType[7], provenance, tempEpsCombId, tempProv, visit[2]))
            
            # patient <-> source
            if avoidDoubleRel == False:
                patSource.append(createEdges(relType[1], provenance, tempPatientId, tempSite, visit[2]))
            
            # sourceAll <-> source
            sASource.append(createEdges(relType[6], provenance, tempProv, tempSite, visit[2]))
            
            

#----------------------------------------------------------------------------------------------------------------------

# functions to create objects for nodes and edges

def createPerson(_id):
    patient = patientNode(_id)
    patientNodes.append(patient)
    return patient.id

def createUnstData(_unstructuredID, _value, _uri):
    uN = unstructuredNode(_unstructuredID, _value, _uri)
    unstructuredNodes.append(uN)
    return uN.unstructuredID

def createSource(_sourceID, _source, _site):
    sourceN = sourceNode(_sourceID, _source, _site)
    sourceNodes.append(sourceN)
    return sourceN.sourceID

def createSourceAll(_ProvID,_source, _site, _provenance):
    sourceAllN = sourceAllNode(_ProvID, _source, _site, _provenance)
    sourceAllNodes.append(sourceAllN)
    return sourceAllN.sourceAllID

def createEdges(_type, _provenance, _start, _end, _time):
    tempEdge = edge(_type, _provenance, _start, _end, _time)
    return tempEdge

def createSex():
    # function to create sexNodes and store them
    # call at beginning
    maleSex = sexNode('male')
    femaleSex = sexNode('female')
    sexNodes.append(maleSex)
    sexNodes.append(femaleSex)
    
            

#----------------------------------------------------------------------------------------------------------------------

# function to determine and create directory for exported csv files

def createPath():
    # create directories
    os.makedirs(pathHeaderNodes)
    os.makedirs(pathHeaderRelations)
    os.makedirs(pathNodes)
    os.makedirs(pathRelations)
   
#----------------------------------------------------------------------------------------------------------------------

# create csv files for nodes

def nodeCreation():
    patientNodesToCSV()
    sexNodesToCSV()
    unstructuredNodesToCSV()
    sourceNodesToCSV()
    sourceAllNodesToCSV()

def patientNodesToCSV():
    os.chdir(pathNodes)
    with open('patients.csv', 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        for element in patientNodes:
            writeCSV.writerow([element.id])

def sexNodesToCSV():
    os.chdir(pathNodes)
    with open('sex.csv', 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        for element in sexNodes:
            writeCSV.writerow([element.sex])

def unstructuredNodesToCSV():
    os.chdir(pathNodes)
    with open('unstructured.csv', 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        for element in unstructuredNodes:
            writeCSV.writerow([element.unstructuredID , element.value])

def sourceNodesToCSV():
    os.chdir(pathNodes)
    with open('source.csv', 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        for element in sourceNodes:
            writeCSV.writerow([element.sourceID, element.source, element.site])
            
def sourceAllNodesToCSV():
    os.chdir(pathNodes)
    with open('sourceAll.csv', 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        for element in sourceAllNodes:
            writeCSV.writerow([element.sourceAllID, element.source, element.site, element.provenance])

#----------------------------------------------------------------------------------------------------------------------

# create csv header files for nodes

def headerNodes():

    patientsHeader()
    sexHeader()
    unstructuredHeader()
    sourceHeader()
    sourceAllHeader()

def patientsHeader():
    os.chdir(pathHeaderNodes)
    with open('patients-header.csv', 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow(['patient:ID(patient-ID)'])

def sexHeader():
    os.chdir(pathHeaderNodes)
    with open('sex-header.csv', 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow(['sex:ID(sex-ID)'])

def unstructuredHeader():
    os.chdir(pathHeaderNodes)
    with open('unstructured-header.csv', 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow(['unstructured:ID(unstructured-ID)', 'value'])

def sourceHeader():
    os.chdir(pathHeaderNodes)
    with open('source-header.csv', 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow(['source:ID(source-ID)', 'source', 'site'])
        
def sourceAllHeader():
    os.chdir(pathHeaderNodes)
    with open('sourceAll-header.csv', 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow(['sourceAll:ID(sourceAll-ID)', 'source', 'site', 'provenance'])

#----------------------------------------------------------------------------------------------------------------------
        
# create csv files for edges

# edges to cover:
# edge patientNode-[hasSex]->sexNode
# edge patientNode-[hasSource]->sourceNode
# edge patientNode<-[hasAffiliationWithEntity]->entityNode (rg, diagn, hg)
# edge patientNode-[hasValue]->unstructuredNode (visit no)
# edge unstructuredNode-[hasSource]->sourceNode
# edge entityNode-[hasSource]->sourceNode (rg, diagn, hg)
def edgeTypeProvToCSV(_relType, _list):
    # patientSex, unstructuredSource
    os.chdir(pathRelations)
    fileName = str(_relType) + '.csv'
    with open(fileName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        for element in _list:
            writeCSV.writerow([element.startNode, element.endNode, element.type, element.provenance])
            
def edgeTypeToCSV(_relType, _list):
    # patientSource, entitySource
    os.chdir(pathRelations)
    fileName = str(_relType) + '.csv'
    with open(fileName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        for element in _list:
            writeCSV.writerow([element.startNode, element.endNode, element.type])
            
def edgeTypeProvTimeToCSV(_relType, _list):
    # patientEntity, patientUnstructured
    os.chdir(pathRelations)
    fileName = str(_relType) + '.csv'
    with open(fileName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        for element in _list:
            writeCSV.writerow([element.startNode, element.endNode, element.type, element.provenance, element.time])

# relType = ['hasSex', 'patientHasSource', 'hasPatient', 'hasDiagnosis', 'hasGeneNomenclature', 'hasValue', 
#           'isSubSource', 'entityHasSourceAll', 'unstructuredHasSourceAll', 'patientHasSourceAll', 
#           'hasEpsCombination' ]
def edgeCreation():
    #hasSourceTogether = patSex + patSourceAll + hgSourceAll + diagnSourceAll + patSource + unSourceAll
    entSourceAllTogether = hgSourceAll + diagnSourceAll #+ rgSourceAll + epsCombSourceAll
    
    edgeTypeToCSV(relType[11], rgSourceAll)
    
    edgeTypeToCSV(relType[12], epsCombSourceAll)
    
    edgeTypeProvToCSV(relType[0], patSex)
    
    edgeTypeToCSV(relType[1], patSource)

    edgeTypeToCSV(relType[7], entSourceAllTogether)
    
    edgeTypeToCSV(relType[8], unSourceAll) 
    
    edgeTypeToCSV(relType[9], patSourceAll)
    
    edgeTypeToCSV(relType[6], sASource)
    
    edgeTypeProvTimeToCSV(relType[2], patRg)
    
    edgeTypeProvTimeToCSV(relType[3], patDiagn)
    
    edgeTypeProvTimeToCSV(relType[4], patHg)
    
    edgeTypeProvTimeToCSV(relType[10], patEpsComb)
    
    edgeTypeProvTimeToCSV(relType[5], patUn)
    

#----------------------------------------------------------------------------------------------------------------------

# create csv header files for edges

# edges to cover:
# edge patientNode-[hasSex]->sexNode
# edge patientNode-[hasSource]->sourceNode
# edge patientNode<-[hasAffiliationWithEntity]->entityNode (rg, diagn, hg)
# edge patientNode-[hasValue]->unstructuredNode (visit no)
# edge unstructuredNode-[hasSource]->sourceNode
# edge entityNode-[hasSource]->sourceNode (rg, diagn, hg)

def headerEdges():

    patientSexHeader()
    patientSourceHeader()
    
    entitySourceAllHeader()
    
    unstructuredSourceAllHeader()
    
    patientSourceAllHeader()
    
    sourceAllSourceHeader()
    
    #entityPatientHeader(relType[2])
    rgHasPatientHeader()
    patientEntityHeader(relType[3])
    patientEntityHeader(relType[4])
    patientEpsilonCombHeader()
    
    patientUnstructuredHeader()
    
    rgSourceAllHeader()
    epsilonCombinationSourceAllHeader()
    
def rgHasPatientHeader():
    os.chdir(pathHeaderRelations)
    headerName = str(relType[2]) + '-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(riskID)', ':END_ID(patient-ID)', 'type', 'provenance', 'time'])
    
def patientEpsilonCombHeader():
    os.chdir(pathHeaderRelations)
    headerName = str(relType[10]) + '-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(patient-ID)', 'epsComb:ID(epsCombID)', 'type', 'provenance', 'time'])
    

def patientSexHeader():
    os.chdir(pathHeaderRelations)
    headerName = str(relType[0]) + '-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)
        # keep provenance only because of changing sex, normaly not helping or necessary 
        writeCSV.writerow([':START_ID(patient-ID)', ':END_ID(sex-ID)', 'type', 'provenance'])

def patientEntityHeader(_relType):
    os.chdir(pathHeaderRelations)
    headerName = str(_relType) + '-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(patient-ID)', ':END_ID(Entity-ID)', 'type', 'provenance', 'time'])

def entityPatientHeader(_relType):
    os.chdir(pathHeaderRelations)
    headerName = str(_relType) + '-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(Entity-ID)', ':END_ID(patient-ID)', 'type', 'provenance', 'time'])

def patientUnstructuredHeader():
    os.chdir(pathHeaderRelations)
    headerName = str(relType[5]) + '-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(patient-ID)', ':END_ID(unstructured-ID)', 'type', 'provenance', 'time'])
        
def sourceAllSourceHeader():
    os.chdir(pathHeaderRelations)
    headerName = str(relType[6]) + '-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(sourceAll-ID)', ':END_ID(source-ID)', 'type'])
        
def patientSourceHeader():
    os.chdir(pathHeaderRelations)
    headerName = str(relType[1]) + '-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(patient-ID)', ':END_ID(source-ID)', 'type'])
        
def patientSourceAllHeader():
    os.chdir(pathHeaderRelations)
    headerName = str(relType[9]) + '-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(patient-ID)', ':END_ID(sourceAll-ID)', 'type'])

def unstructuredSourceAllHeader():
    os.chdir(pathHeaderRelations)
    headerName = str(relType[8]) + '-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(unstructured-ID)', ':END_ID(sourceAll-ID)', 'type', 'provenance'])

def entitySourceAllHeader():
    os.chdir(pathHeaderRelations)
    headerName = str(relType[7]) + '-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(Entity-ID)', ':END_ID(sourceAll-ID)', 'type'])
        
def rgSourceAllHeader():
    os.chdir(pathHeaderRelations)
    headerName = str(relType[11]) + '-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(riskID)', ':END_ID(sourceAll-ID)', 'type'])
        
def epsilonCombinationSourceAllHeader():
    os.chdir(pathHeaderRelations)
    headerName = str(relType[12]) + '-header.csv'
    with open(headerName, 'w') as csvTargetFile:
        writeCSV = csv.writer(csvTargetFile)

        writeCSV.writerow([':START_ID(epsCombID)', ':END_ID(sourceAll-ID)', 'type'])
        



#----------------------------------------------------------------------------------------------------------------------

# start programm

tic = time.time()
        
createPath()

createSex()

impCSVFile('export.CSV')

nodeCreation()

edgeCreation()

headerNodes()

headerEdges()

toc = time.time()
# timer
print("--- %s seconds ---" % (toc - tic))

print('done')







