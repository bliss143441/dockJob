from TestHelperSuperClass import testHelperSuperClass
import unittest
from APIBackendWithSwaggerAppObj import APIBackendWithSwaggerAppObj
import json
from sortedcontainers import SortedDict

class mockAppObj():
  pagesizemax = 200

class mockRequestArgs():
  vals = {}
  def __init__(self, vals):
    self.vals = vals
  def get(self, str):
    if str not in self.vals:
      return None
    return self.vals[str]

class mockRequest():
  args = None
  def __init__(self, vals):
    self.args = mockRequestArgs(vals)

testArray =  SortedDict()
testArray[0] = {'id': '123ab1', 'K2': 'V9', 'K3': True, 'K4': False, 'K5': 1}
testArray[1] = {'id': '123ab2', 'K2': 'V8', 'K3': False, 'K4': False, 'K5': 2}
testArray[2] = {'id': '123ab3', 'K2': 'V7', 'K3': True, 'K4': False, 'K5': 3}
testArray[3] = {'id': '123ab4', 'K2': 'V6', 'K3': False, 'K4': False, 'K5': 4}
testArray[4] = {'id': '123ab5', 'K2': 'V5', 'K3': True, 'K4': False, 'K5': 5}
testArray[5] = {'id': '123ab6', 'K2': 'V4', 'K3': False, 'K4': False, 'K5': 6}
testArrayOddOnly =  SortedDict()
testArrayOddOnly[0] = testArray[0]
testArrayOddOnly[1] = testArray[2]
testArrayOddOnly[2] = testArray[4]
testArrayReversed =  SortedDict()
testArrayReversed[0] = testArray[5]
testArrayReversed[1] = testArray[4]
testArrayReversed[2] = testArray[3]
testArrayReversed[3] = testArray[2]
testArrayReversed[4] = testArray[1]
testArrayReversed[5] = testArray[0]
testArrayTwoKey =  SortedDict() #1,3,5,2,4,6
testArrayTwoKey[0] = testArray[1]
testArrayTwoKey[1] = testArray[3]
testArrayTwoKey[2] = testArray[5]
testArrayTwoKey[3] = testArray[0]
testArrayTwoKey[4] = testArray[2]
testArrayTwoKey[5] = testArray[4]

def dictToArr(dict):
  ret = []
  for cur in dict:
    ret.append(dict[cur])
  return ret

class test_APIBackendWithSwaggerAppObj(testHelperSuperClass):

  def assertGetPaginatedResult(self, requestVals, outputFN, filterFN, expOutput, inpData=testArray):
    def filterFNInt(item, whereClauseText):
      return True
    if filterFN is None:
      filterFN = filterFNInt
    def outputFNInt(item):
      return item
    if outputFN is None:
      outputFN = outputFNInt
    request = mockRequest(requestVals)
    res = APIBackendWithSwaggerAppObj.getPaginatedResult(
      mockAppObj,
      inpData, 
      outputFN, 
      request,
      filterFN
    )
    expRes = {
      'pagination': {
        'offset': 0,
        'pagesize': 100,
        'total': len(expOutput)
      },
      'result': dictToArr(expOutput)
    }
    self.assertJSONStringsEqual(res,expRes)

#************ Tests below (helpers above) *****************************

  def test_getPaginatedResult_simple(self):
    self.assertGetPaginatedResult({},None,None,testArray)

  def test_getPaginatedResult_filterOnlyOdd(self):
    def filterFN(item, whereClauseText):
      return ((item['K5'] % 2) == 1)
    self.assertGetPaginatedResult({ 'query': 'AAA'},None,filterFN,testArrayOddOnly)

  def test_getPaginatedResult_sortIntKeyDesc(self):
    self.assertGetPaginatedResult({ 'sort': 'K5:desc'},None,None,testArrayReversed)
  def test_getPaginatedResult_sortIntKeyAsc(self):
    self.assertGetPaginatedResult({ 'sort': 'K5:asc'},None,None,testArray)
  def test_getPaginatedResult_sortIntKey(self):
    self.assertGetPaginatedResult({ 'sort': 'K5'},None,None,testArray)
  def test_getPaginatedResult_sortStringKey2Desc(self):
    self.assertGetPaginatedResult({ 'sort': 'K2:desc'},None,None,testArray)
  def test_getPaginatedResult_sortStringKey2Asc(self):
    self.assertGetPaginatedResult({ 'sort': 'K2:asc'},None,None,testArrayReversed)
  def test_getPaginatedResult_sortStringKey2(self):
    self.assertGetPaginatedResult({ 'sort': 'K2'},None,None,testArrayReversed)

  def test_getPaginatedResult_MultiKeySort(self):
    self.assertGetPaginatedResult({ 'sort': 'K3,K5'},None,None,testArrayTwoKey)

  def test_getPaginatedResult_functionAccess(self):
    obj = SortedDict()
    num = 0
    def outputFN(item):
      return testArray[item]

    for curKey in testArray:
      obj[num]=curKey
      num = num + 1
    self.assertGetPaginatedResult({'sort': 'K5:desc'},outputFN,None,testArrayReversed,inpData=obj)