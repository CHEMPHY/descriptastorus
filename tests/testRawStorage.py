from __future__ import print_function
import unittest
from descriptastorus import raw
from descriptastorus.descriptors import rdDescriptors
from descriptastorus.descriptors import MakeGenerator
import contextlib, sys

import numpy, os, shutil

class TestCase(unittest.TestCase):
    def test_raw(self):
        try:
            directory = "test-store"
            if os.path.exists(directory):
                shutil.rmtree(directory)

            descriptors = MakeGenerator("Morgan3Counts,RDKit2D".split(","))
            N=10
            with contextlib.closing(raw.MakeStore(descriptors.GetColumns(), N, directory)) as r:
                smiles = ["C"]
                data = []
                for i in range(N):
                    row = descriptors.process( "".join(smiles) )
                    data.append(row)
                    r.putRow( i, row )
                    smiles.append("C")

                try:
                    r.putRow( i+1, descriptors.process( "".join(smiles) ) )
                    self.assertFalse("Shouldn't be able to write past the end of the db")

                except:
                    pass

                for i, row in enumerate(data):
                    self.assertEqual(tuple(row), r.get(i))
        finally:
            if os.path.exists(directory):
                shutil.rmtree(directory)

    def testStringStore(self):
        try:
            directory = "test-store"
            if os.path.exists(directory):
                shutil.rmtree(directory)
                
            with contextlib.closing(raw.MakeStore([('name', numpy.dtype("S80"))],
                                                  10, directory)) as r:
                print("*"*44, file=sys.stderr)
                print(r.pack_format, file=sys.stderr)
                print("*"*44, file=sys.stderr)
                for i in range(10):
                    r.putRow(i, str(i))

                for i in range(10):
                    self.assertEqual(r.get(i), (str(i),))
            
        finally:
            if os.path.exists(directory):
                shutil.rmtree(directory)
    
                      
if __name__ == '__main__':
    unittest.main()
