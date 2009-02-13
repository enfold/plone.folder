from unittest import defaultTestLoader
from zope.interface import classImplements
from Products.ATContentTypes.content.document import ATDocument
from plone.folder.interfaces import IOrderable
from plone.folder.tests.base import IntegrationTestCase, PloneFolderLayer
from plone.folder.tests.layer import PloneFolderPartialOrderingLayer


class Layer(PloneFolderPartialOrderingLayer, PloneFolderLayer):
    """ test layer for partial ordering support """


class PartialOrderingTests(IntegrationTestCase):
    """ tests regarding order-support for only items marked orderable """

    layer = Layer

    def afterSetUp(self):
        classImplements(ATDocument, IOrderable)

    def testGetObjectPositionForNonOrderableContent(self):
        oid = self.folder.invokeFactory('Event', id='foo')
        obj = self.folder._getOb(oid)
        # a non-orderable object should return "no position"
        self.failIf(IOrderable.providedBy(obj), 'orderable events?')
        self.assertEqual(self.folder.getObjectPosition(oid), None)
        # a non-existant object should raise an error, though
        self.assertRaises(ValueError, self.folder.getObjectPosition, 'bar')

    def testRemoveNonOrderableContent(self):
        self.setRoles(('Manager',))
        oid = self.folder.invokeFactory('Event', id='foo')
        self.folder.manage_delObjects('foo')
        self.failIf(self.folder.hasObject('foo'), 'foo?')

    def testCreateOrderableContent(self):
        self.setRoles(('Manager',))
        # create orderable content
        oid = self.folder.invokeFactory('Document', id='foo')
        self.assertEqual(oid, 'foo')
        self.failUnless(self.folder.hasObject('foo'), 'foo?')
        self.assertEqual(self.folder.getObjectPosition(oid), 0)
        # and some more...
        self.folder.invokeFactory('Document', id='bar')
        self.assertEqual(self.folder.getObjectPosition('bar'), 1)
        self.folder.invokeFactory('Event', id='party')
        self.assertEqual(self.folder.getObjectPosition('party'), None)


def test_suite():
    return defaultTestLoader.loadTestsFromName(__name__)

