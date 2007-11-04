import unittest

from plone.folder.ordered import OrderedBTreeFolder

from OFS.CopySupport import CopySource


class DummyObject(CopySource):
    
    def __init__(self, id, meta_type):
        self.id = id
        self.meta_type = meta_type
        
    def cb_isMoveable(self):
        return 1
        
    def manage_afterAdd(self, item, container):
        return
        
    def manage_beforeDelete(self, item, container):
        return
        
    manage_afterAdd.__five_method__ = True
    manage_beforeDelete.__five_method__ = True
    
    def wl_isLocked(self):
        return 0


class TestCase(unittest.TestCase):
    """ tests borrowed from OFS.tests.testOrderSupport """
        
    def create(self):
        folder = OrderedBTreeFolder("f1")
        
        folder._setOb('o1', DummyObject('o1', 'mt1'))
        folder._setOb('o2', DummyObject('o2', 'mt1'))
        folder._setOb('o3', DummyObject('o3', 'mt1'))
        folder._setOb('o4', DummyObject('o4', 'mt1'))
        
        return folder
        
    # Test for ordering of basic methods
    
    def test_objectIdsOrdered(self):
        pass
    
    def test_objectValuesOrdered(self):
        pass
        
    def test_objectItemsOrdered(self):
        pass
        
    def test_contentIdsOrdered(self):
        pass
        
    def test_contentValuesOrdered(self):
        pass
        
    def test_contentItemsOrdered(self):
        pass
        
    # Tests borrowed from OFS.tests.testsOrderSupport
        
    def _doCanonTest(self, methodname, table):
        for args, order, rval in table:
            f = self.create()
            method = getattr(f, methodname)
            if rval == 'ValueError':
                self.failUnlessRaises( ValueError, method, *args )
            else:
                self.failUnlessEqual( method(*args), rval )
            self.failUnlessEqual( list(f.objectIds()), order )

    def test_moveObjectsUp(self):
        self._doCanonTest( 'moveObjectsUp',
              ( ( ( 'o4', 1 ),         ['o1', 'o2', 'o4', 'o3'], 1 )
              , ( ( 'o4', 2 ),         ['o1', 'o4', 'o2', 'o3'], 1 )
              , ( ( ('o1', 'o3'), 1 ), ['o1', 'o3', 'o2', 'o4'], 1 )
              , ( ( ('o1', 'o3'), 9 ), ['o1', 'o3', 'o2', 'o4'], 1 )
              , ( ( ('o2', 'o3'), 1 ), ['o2', 'o3', 'o1', 'o4'], 2 )
              , ( ( ('o2', 'o3'), 1, ('o1', 'o2', 'o3', 'o4') ),
                                       ['o2', 'o3', 'o1', 'o4'], 2 )
              , ( ( ('o2', 'o3'), 1, ('o2', 'o3', 'o4') ),
                                       ['o1', 'o2', 'o3', 'o4'], 0 )
              , ( ( ('n2', 'o3'), 1 ), ['o1', 'o2', 'o3', 'o4'], 'ValueError')
              , ( ( ('o3', 'o1'), 1 ), ['o1', 'o3', 'o2', 'o4'], 1 )
              )
            )

    def test_moveObjectsDown(self):
        self._doCanonTest( 'moveObjectsDown',
              ( ( ( 'o1', 1 ),         ['o2', 'o1', 'o3', 'o4'], 1 )
              , ( ( 'o1', 2 ),         ['o2', 'o3', 'o1', 'o4'], 1 )
              , ( ( ('o2', 'o4'), 1 ), ['o1', 'o3', 'o2', 'o4'], 1 )
              , ( ( ('o2', 'o4'), 9 ), ['o1', 'o3', 'o2', 'o4'], 1 )
              , ( ( ('o2', 'o3'), 1 ), ['o1', 'o4', 'o2', 'o3'], 2 )
              , ( ( ('o2', 'o3'), 1, ('o1', 'o2', 'o3', 'o4') ),
                                       ['o1', 'o4', 'o2', 'o3'], 2 )
              , ( ( ('o2', 'o3'), 1, ('o1', 'o2', 'o3') ),
                                       ['o1', 'o2', 'o3', 'o4'], 0 )
              , ( ( ('n2', 'o3'), 1 ), ['o1', 'o2', 'o3', 'o4'], 'ValueError')
              , ( ( ('o4', 'o2'), 1 ), ['o1', 'o3', 'o2', 'o4'], 1 )
              )
            )

    def test_moveObjectsToTop(self):
        self._doCanonTest( 'moveObjectsToTop',
              ( ( ( 'o4', ),         ['o4', 'o1', 'o2', 'o3'], 1 )
              , ( ( ('o1', 'o3'), ), ['o1', 'o3', 'o2', 'o4'], 1 )
              , ( ( ('o2', 'o3'), ), ['o2', 'o3', 'o1', 'o4'], 2 )
              , ( ( ('o2', 'o3'), ('o1', 'o2', 'o3', 'o4') ),
                                     ['o2', 'o3', 'o1', 'o4'], 2 )
              , ( ( ('o2', 'o3'), ('o2', 'o3', 'o4') ),
                                     ['o1', 'o2', 'o3', 'o4'], 0 )
              , ( ( ('n2', 'o3'), ), ['o1', 'o2', 'o3', 'o4'], 'ValueError')
              , ( ( ('o3', 'o1'), ), ['o3', 'o1', 'o2', 'o4'], 1 )
              )
            )

    def test_moveObjectsToBottom(self):
        self._doCanonTest( 'moveObjectsToBottom',
              ( ( ( 'o1', ),         ['o2', 'o3', 'o4', 'o1'], 1 )
              , ( ( ('o2', 'o4'), ), ['o1', 'o3', 'o2', 'o4'], 1 )
              , ( ( ('o2', 'o3'), ), ['o1', 'o4', 'o2', 'o3'], 2 )
              , ( ( ('o2', 'o3'), ('o1', 'o2', 'o3', 'o4') ),
                                     ['o1', 'o4', 'o2', 'o3'], 2 )
              , ( ( ('o2', 'o3'), ('o1', 'o2', 'o3') ),
                                     ['o1', 'o2', 'o3', 'o4'], 0 )
              , ( ( ('n2', 'o3'), ), ['o1', 'o2', 'o3', 'o4'], 'ValueError')
              , ( ( ('o4', 'o2'), ), ['o1', 'o3', 'o4', 'o2'], 1 )
              )
            )

    def test_orderObjects(self):
        self._doCanonTest( 'orderObjects',
              ( ( ( 'id', 'id' ),       ['o4', 'o3', 'o2', 'o1'], 4)
              , ( ( 'meta_type', '' ),  ['o1', 'o3', 'o2', 'o4'], 1)
              , ( ( 'meta_type', 'n' ), ['o4', 'o2', 'o3', 'o1'], 3)
              , ( ( 'position', 0 ),    ['o1', 'o2', 'o3', 'o4'], 0)
              , ( ( 'position', 1 ),    ['o4', 'o3', 'o2', 'o1'], 3)
              )
            )

    def test_getObjectPosition(self):
        self._doCanonTest( 'getObjectPosition',
              ( ( ( 'o2', ), ['o1', 'o2', 'o3', 'o4'], 1)
              , ( ( 'o4', ), ['o1', 'o2', 'o3', 'o4'], 3)
              , ( ( 'n2', ), ['o1', 'o2', 'o3', 'o4'], 'ValueError')
              )
            )

    def test_moveObjectToPosition(self):
        self._doCanonTest( 'moveObjectToPosition',
              ( ( ( 'o2', 2 ), ['o1', 'o3', 'o2', 'o4'], 1)
              , ( ( 'o4', 2 ), ['o1', 'o2', 'o4', 'o3'], 1)
              , ( ( 'n2', 2 ), ['o1', 'o2', 'o3', 'o4'], 'ValueError')
              )
            )


class TestOrderSupport(unittest.TestCase):
    """ tests borrowed from Products.CMFPlone.tests.testOrderSupport """

    def setUp(self):
        self.folder = OrderedBTreeFolder("f1")
        self.folder._setOb('foo', DummyObject('foo', 'mt1'))
        self.folder._setOb('bar', DummyObject('bar', 'mt1'))
        self.folder._setOb('baz', DummyObject('baz', 'mt1'))

    def testGetObjectPosition(self):
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('bar'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def testMoveObject(self):
        self.folder.moveObjectToPosition('foo', 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def testMoveObjectToSamePos(self):
        self.folder.moveObjectToPosition('bar', 1)
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('bar'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def testMoveObjectToFirstPos(self):
        self.folder.moveObjectToPosition('bar', 0)
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def testMoveObjectToLastPos(self):
        self.folder.moveObjectToPosition('bar', 2)
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 2)

    def testMoveObjectOutLowerBounds(self):
        # Pos will be normalized to 0
        self.folder.moveObjectToPosition('bar', -1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def testMoveObjectOutUpperBounds(self):
        # Pos will be normalized to 2
        self.folder.moveObjectToPosition('bar', 3)
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 2)

    def testMoveObjectsUp(self):
        self.folder.moveObjectsUp(['bar'])
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def testMoveObjectsDown(self):
        self.folder.moveObjectsDown(['bar'])
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 2)

    def testMoveObjectsToTop(self):
        self.folder.moveObjectsToTop(['bar'])
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)

    def testMoveObjectsToBottom(self):
        self.folder.moveObjectsToBottom(['bar'])
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 2)

    def testMoveTwoObjectsUp(self):
        self.folder.moveObjectsUp(['bar', 'baz'])
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('foo'), 2)

    def testMoveTwoObjectsDown(self):
        self.folder.moveObjectsDown(['foo', 'bar'])
        self.assertEqual(self.folder.getObjectPosition('baz'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 2)

    def testMoveTwoObjectsToTop(self):
        self.folder.moveObjectsToTop(['bar', 'baz'])
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('foo'), 2)

    def testMoveTwoObjectsToBottom(self):
        self.folder.moveObjectsToBottom(['foo', 'bar'])
        self.assertEqual(self.folder.getObjectPosition('baz'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 2)

    def testOrderObjects(self):
        self.folder.orderObjects('id')
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('foo'), 2)

    def testSubsetIds(self):
        self.folder.moveObjectsByDelta(['baz'], -1, ['foo', 'bar', 'baz'])
        self.assertEqual(self.folder.getObjectPosition('foo'), 0)
        self.assertEqual(self.folder.getObjectPosition('baz'), 1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 2)

    def testSkipObjectsNotInSubsetIds(self):
        self.folder.moveObjectsByDelta(['baz'], -1, ['foo', 'baz'])
        self.assertEqual(self.folder.getObjectPosition('baz'), 0)
        self.assertEqual(self.folder.getObjectPosition('bar'), 1) # Did not move
        self.assertEqual(self.folder.getObjectPosition('foo'), 2)

    def testIgnoreNonObjects(self):
        #Fix for (http://dev.plone.org/plone/ticket/3959) non contentish objects
        #cause errors, we should just ignore them
        self.folder.moveObjectsByDelta(['bar','blah'], -1)
        self.assertEqual(self.folder.getObjectPosition('bar'), 0)
        self.assertEqual(self.folder.getObjectPosition('foo'), 1)
        self.assertEqual(self.folder.getObjectPosition('baz'), 2)


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(TestCase),
        unittest.makeSuite(TestOrderSupport)
    ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')