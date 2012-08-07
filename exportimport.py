"""
Project: HumaineMailman
 Author: Christian Federmann <cfedermann@dfki.de>

This work has been supported by the EC Project HUMAINE (IST-507422);
See http://emotion-research.net/ for more information.
"""
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import XMLAdapterBase

from Products.HumaineMailman.HumaineMailmanTool import HumaineMailmanTool


class HumaineMailmanToolXMLAdapter(XMLAdapterBase):
    """
    Implements export/import behaviour for the HumaineMailmanTool.
    """
    __used_for__ = HumaineMailmanTool
    
    _LOGGER_ID = 'mailman_tool'
    
    name = 'mailman_tool'
    
    def _exportNode(self):
        """
        Export the object as a DOM node.
        """
        self._encoding = self.context.getProperty('default_charset', 'utf-8')
        
        node = self._doc.createElement('object')
        
        mailing_lists = self._doc.createElement('mailing_lists')
        member_mailing_lists = self._doc.createElement('member_mailing_lists')
        
        properties = getToolByName(self.context, "portal_properties")
        lists = list(properties.mailman_properties.getProperty("lists", []))
        
        for item in lists:
            element = self._doc.createElement('element')
            element.setAttribute('value', item)
            mailing_lists.appendChild(element)
        node.appendChild(mailing_lists)
        
        membership = getToolByName(self.context, "portal_membership")
        members = membership.listMembers()
        
        for member in members:
            member_child = self._doc.createElement(member.getId())
            member_lists = list(member.getProperty('mailing_lists', []))
            
            for item in member_lists:
                element = self._doc.createElement('element')
                element.setAttribute('value', item)
                member_child.appendChild(element)
            member_mailing_lists.appendChild(member_child)
        node.appendChild(member_mailing_lists)
        
        self._logger.info('HumaineMailman Tool exported.')
        return node
    
    def _importNode(self, node):
        """
        Import the object from the given DOM node.
        """
        self._encoding = self.context.getProperty('default_charset', 'utf-8')
        
        for child in node.childNodes:
            if child.nodeName == 'mailing_lists':
                properties = getToolByName(self.context, "portal_properties")
                lists = list(properties.mailman_properties.getProperty(
                  "lists", []))
                
                if self.environ.shouldPurge():
                    lists = []
                
                for element in child.childNodes:
                    if element.nodeName == 'element':
                        item = element.getAttribute('value')
                        if item:
                            lists.append(item)
                
                properties.mailman_properties.lists = lists
            
            # cfedermann: import of member subscriptions not yet ready.
            elif child.nodeName == 'member_mailing_lists':
                pass
        
        self._logger.info('HumaineMailman Tool imported.')

def importHumaineMailmanTool(context):
    """
    Imports HumaineMailmanTool lists and subscriptions from an XML file.
    """
    site = context.getSite()
    tool = getToolByName(site, 'mailman_tool', None)
    if tool is None:
        logger = context.getLogger('mailman_tool')
        logger.warning('Nothing to import.')
        return
    
    importObjects(tool, '', context)

def exportHumaineMailmanTool(context):
    """
    Exports HumaineMailmanTool lists and subscriptions to an XML file.
    """
    site = context.getSite()
    tool = getToolByName(site, 'mailman_tool', None)
    if tool is None:
        logger = context.getLogger('mailman_tool')
        logger.warning('Nothing to export.')
        return
    
    exportObjects(tool, '', context)
