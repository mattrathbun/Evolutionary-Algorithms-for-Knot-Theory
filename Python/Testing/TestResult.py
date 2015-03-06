import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from datetime import datetime
import ADT, ADTOp, ADTOpList

K = ADT.ADT([-4, -18, -22, -14, -6, -20, -8, -10, -2, -12, -16], [1, 1, 1, -1, 1, -1, -1, 1, 1, -1, 1])


#['CC(@13)', '2U(pos=1, side=R, target=[5, 4])', '2D(pos=8)', '2D(pos=4)', 
#'1U(pos=1, side=R, sign=1)', '1D(pos=2)', '1U(pos=1, side=L, sign=-1)', 'CC(@2)']

ol = []
ol.append(ADTOp.ADTCC({'arc':13}))
ol.append(ADTOp.ADTMove(2, 'U', {'pos':1, 'side':'R', 'target':[5,4]}))
ol.append(ADTOp.ADTMove(2, 'D', {'pos':8}))
ol.append(ADTOp.ADTMove(2, 'D', {'pos':4}))
ol.append(ADTOp.ADTMove(1, 'U', {'pos':1, 'side':'R', 'sign':1}))
ol.append(ADTOp.ADTMove(1, 'D', {'pos':2}))
ol.append(ADTOp.ADTMove(1, 'U', {'pos':1, 'side':'L', 'sign':-1}))
ol.append(ADTOp.ADTCC({'arc':2}))

for op in ol:
    print op.toString()
#    K = op.apply(K)
#    print K.to_string()