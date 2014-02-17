import unittest,getopt,sys,os
import matplotlib as mpl
if mpl.get_backend() != 'agg':
    mpl.use('agg')

## parse inputs                                                                                                                      
try:
    optlist, args = getopt.getopt(sys.argv[1:],'v')
except getopt.GetoptError:
    print getopt.GetoptError
    print sys.argv[0] + "-a"
    print "      projName (-v) verbose flag (default is False)"
    sys.exit()

VERBOSE = False
RUNALL = False

for o, a in optlist:
    if o == '-v':
        VERBOSE = True

### tests
from ControllerTest import *
ControllerTestSuite = unittest.TestLoader().loadTestsFromTestCase(ControllerTest)
controllerSuite = unittest.TestSuite([ControllerTestSuite])

from BasicTemplates import *
BasicTestSuite = unittest.TestLoader().loadTestsFromTestCase(BasicTemplates)
basicSuite = unittest.TestSuite([BasicTestSuite])


#from FishersExactTest import *
#FishersExactTestSuite = unittest.TestLoader().loadTestsFromTestCase(FishersExactTest)
#FishersExactSuite = unittest.TestSuite([FishersExactTestSuite])
