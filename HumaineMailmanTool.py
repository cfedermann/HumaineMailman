# pylint: disable-msg=F0401
"""
Project: HumaineMailman
 Author: Christian Federmann <cfedermann@gmail.com>

This work has been supported by the EC Project HUMAINE (IST-507422);
See http://emotion-research.net/ for more information.
"""
from xml.dom.minidom import getDOMImplementation

from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.permissions import View, ManagePortal
from Products.CMFCore.utils import UniqueObject, getToolByName

try:
    from App.class_init import InitializeClass

except ImportError:
    from Globals import InitializeClass

from Products.HumaineMailman.config import PKG_NAME, UNIQUE_ID, ICON


# pylint: disable-msg=C0103,E1101
class HumaineMailmanTool(UniqueObject, SimpleItem):
    """
    Plone tool that allows to connect Mailman mailing lists to Plone.
    """
    id = UNIQUE_ID
    meta_type = "{0} Tool".format(PKG_NAME)
    toolicon = ICON
    security = ClassSecurityInfo()
    plone_tool = 1
    
    _cache = {"general": "", "success": "", "already": "", "unknown": ""}
    
    def _format_cache_info(self, success, already, unknown, verb="subscribe"):
        """
        Formats _cache information s.t. it can be printed to the user.
        
        Possible verbs are: "subscribe", "unsubscribe".
        
        """
        self._cache["general"] += "{0} successfully {1}d, {2} " \
          "already {1}d, {3} unknown emails\n\n".format(success, verb,
          already, unknown)
        
        if success > 0:
            self._cache["success"] = "\n{0}".format(self._cache["success"])
        
        else:
            self._cache["success"] = ""
        
        if already > 0:
            self._cache["already"] = "\n{0}".format(self._cache["already"])
        
        else:
            self._cache["already"] = ""
        
        if unknown > 0:
            self._cache["unknown"] = "\n{0}".format(self._cache["unknown"])
        
        else:
            self._cache["unknown"] = ""
    
    security.declareProtected(ManagePortal, "export_content")
    def export_content(self):
        """
        Exports mailing lists and member subscriptions to XML.
        """
        DOM = getDOMImplementation()
        doc = DOM.createDocument(None, "object", None)
        
        mailing_lists = doc.createElement("mailing_lists")
        member_mailing_lists = doc.createElement("member_mailing_lists")
        
        properties = getToolByName(self, "portal_properties")
        lists = list(properties.mailman_properties.getProperty("lists", []))
        for _list in lists:
            item = doc.createElement("element")
            item.setAttribute('value', _list)
            mailing_lists.appendChild(item)
        doc.firstChild.appendChild(mailing_lists)
        
        membership = getToolByName(self, "portal_membership")
        members = membership.listMembers()
        for member in members:
            member_lists = list(member.getProperty("mailman_lists", []))
            member_node = doc.createElement(member.getId())
            for member_list in member_lists:
                item = doc.createElement("element")
                item.setAttribute('value', member_list)
                member_node.appendChild(item)
            member_mailing_lists.appendChild(member_node)
            
        doc.firstChild.appendChild(member_mailing_lists)
        return doc.toprettyxml()
    
    security.declareProtected(ManagePortal, "get_subscriptions_cache")
    def get_subscriptions_cache(self):
        """
        Returns the subscriptions cache for this tool instance.
        """
        return self._cache
    
    security.declareProtected(ManagePortal, "subscribe_list")
    def subscribe_list(self, address, emails):
        """
        Adds all portal members specified by their email addresses to the
        given mailing list and updates the subscriptions cache.
        """
        # Perform a basic sanity check.
        if not address or not emails:
            return
        
        # Reset subscriptions cache.
        self._cache["general"] = "{0} subscribe stats:\n" .format(address)
        self._cache["success"] = "successfully subscribed:\n"
        self._cache["already"] = "already subscribed:\n"
        self._cache["unknown"] = "unknown emails:\n"
        
        # We collect success information for the subscriptions cache log.
        success = 0
        already = 0
        unknown = 0
        
        # Browse through the list of members and check if their email is
        # already subscribed to the given list.  If not, update the member's
        # 'mailman_lists' property accordingly.
        membership = getToolByName(self, "portal_membership")
        members = membership.listMembers()
        for member in members:
            email = member.getProperty("email", None)
            
            if email in emails:
                emails.remove(email)
                member_lists = list(member.getProperty("mailman_lists", []))

                # Subscribe emails iff they are not yet subscribed.
                if not address in member_lists:
                    member_lists.append(address)
                    member_property = {"mailman_lists": tuple(member_lists)}
                    member.setMemberProperties(member_property)
                    self._cache["success"] += "{0}: successfully subscribed" \
                      " to {1}\n".format(email, address)
                    success += 1
                
                # Otherwise log already subscribed emails in the _cache.
                else:
                    self._cache["already"] += "{0}: already subscribed to" \
                      " {1}\n".format(email, address)
                    already += 1
        
        # Log unknown emails in the _cache.
        for unknown_email in emails:
            self._cache["unknown"] += "{0}: not a registered member " \
              "email\n".format(unknown_email)
            unknown += 1
        
        # Format the _cache information.
        self._format_cache_info(success, already, unknown)
    
    security.declareProtected(ManagePortal, "unsubscribe_list")
    def unsubscribe_list(self, address, emails):
        """
        Removes all portal members specified by their email addresses from the
        given mailing list and updates the subscriptions cache.
        """
        # Perform a basic sanity check.
        if not address or not emails:
            return

        # Reset subscriptions cache.
        self._cache["general"] = "{0} unsubscribe stats:\n" .format(address)
        self._cache["success"] = "successfully unsubscribed:\n"
        self._cache["already"] = "already unsubscribed:\n"
        self._cache["unknown"] = "unknown emails:\n"
        
        # We collect success information for the subscriptions cache log.
        success = 0
        already = 0
        unknown = 0
        
        # Browse through the list of members and check if their email is
        # already unsubscribed from the given list.  If not, update the
        # member's 'mailman_lists' property accordingly.
        membership = getToolByName(self, "portal_membership")
        members = membership.listMembers()
        for member in members:
            email = member.getProperty("email", None)
            
            if email in emails:
                emails.remove(email)
                member_lists = list(member.getProperty("mailman_lists", []))
                
                # Unsubscribe emails iff they are already subscribed.
                if address in member_lists:
                    member_lists.remove(address)
                    member_property = {"mailman_lists": tuple(member_lists)}
                    member.setMemberProperties(member_property)
                    self._cache["success"] += "{0}: successfully unsubscrib" \
                      "ed from {1}\n".format(email, address)
                    success += 1
                
                # Otherwise log already unsubscribed emails in the _cache.
                else:
                    self._cache["already"] += "{0}: already unsubscribed " \
                      "from {1}\n".format(email, address)
                    already += 1
        
        # Log unknown emails in the _cache.
        for unknown_email in list(emails):
            self._cache["unknown"] += "{0}: not a registered member " \
              "email\n".format(unknown_email)
            unknown += 1
        
        # Format the _cache information.
        self._format_cache_info(success, already, unknown, verb="unsubscribe")
    
    security.declareProtected(ManagePortal, "get_members")
    def get_members(self, prefix):
        """
        Returns the list of all Plone members whose member name matches
        the given prefix.
        """
        result = []
        
        # Verify that the given prefix is valid, i.e. a non-empty string.
        if not len(prefix):
            return []
        
        try:
            membership = getToolByName(self, "portal_membership")
            members = membership.listMemberIds()
            
            # Browse through the list of members and check member name.
            for member in members:
                if prefix.lower() == member[0:len(prefix)].lower():
                    result.append(member)
        except:
            result = [self.plone_utils.exceptionString()]
        
        return result
    
    security.declareProtected(ManagePortal, "get_list_members")
    def get_list_members(self, address):
        """
        Returns the list of all Plone members who are subscribed to the list
        defined by the given list address.
        """
        result = []
        
        try:
            membership = getToolByName(self, "portal_membership")
            members = membership.listMembers()
            
            # Browse through the list of members and check list status.
            for member in members:
                member_lists = list(member.getProperty("mailman_lists", []))
                member_email = member.getProperty("email", None)
                
                # Iff the member is subscribed to the list, add corresponding
                # id and email to the result list.
                if address in member_lists:
                    result.append({0: member.getId(), 1: member_email})
        except:
            result = [self.plone_utils.exceptionString()]
        
        return result
    
    security.declareProtected(ManagePortal, "get_auto_lists")
    def get_auto_lists(self):
        """
        Returns the list of all auto lists.
        """
        result = []
        
        try:
            properties = getToolByName(self, "portal_properties")
            lists = properties.mailman_properties.getProperty("lists", [])
            lists = list(lists)
            
            # Browse through all mailing lists.
            for mailing_list in lists:
                list_data = mailing_list.split(":")
                
                # Verify that this is a correct list definition.
                if len(list_data) < 4:
                    continue
                
                # Verify that this is an auto list.
                if list_data[0] == "auto":
                    result.append(list_data[1])
        except:
            result = [self.plone_utils.exceptionString()]
        
        return result
    
    security.declareProtected(ManagePortal, "get_mailing_lists")
    def get_mailing_lists(self):
        """
        Returns the list of all non-auto lists, i.e. open and role lists.
        """
        result = []
        
        try:
            properties = getToolByName(self, "portal_properties")
            lists = properties.mailman_properties.getProperty("lists", [])
            lists = list(lists)
            
            # Browse through all mailing lists.
            for mailing_list in lists:
                list_data = mailing_list.split(":")
                
                # Verify that this is a correct list definition.
                if len(list_data) < 4:
                    continue

                # Nerify that this is NOT an auto list.
                if list_data[0] != "auto":
                    result.append(list_data[1])
        except:
            result = [self.plone_utils.exceptionString()]
        
        return result
    
    # Use security.declarePublic("get_member_lists") to allow anonymous users
    # to call this method without the need to login.  This allows to use wget
    # synchronisation with mailman_{autolist|list}_update.py.
    security.declareProtected(View, "get_member_lists")
    def get_member_lists(self, member):
        """
        Returns the lists a given portal member is subscribed to.
        """
        result = []
        
        # Verify that the given member object is valid.
        if not member:
            return []
        
        try:
            properties = getToolByName(self, "portal_properties")
            lists = list(properties.mailman_properties.lists)
            member_lists = list(member.getProperty("mailman_lists", []))
            
            # Browse through all mailing lists.
            for mailing_list in lists:
                list_data = mailing_list.split(":")
                
                # Verify that this is a correct list definition
                if len(list_data) < 4:
                    continue
                
                # Add all open lists to the result list.
                if list_data[0] == "open":
                    result.append((list_data[1], \
                                   list_data[1] in member_lists, \
                                   list_data[2]))
                
                # Also add all role lists iff the current user has the
                # appropriate role.
                elif list_data[0] == "role":
                    if member.has_role(list_data[4]):
                        result.append((list_data[1], \
                                       list_data[1] in member_lists, \
                                       list_data[2]))
                
                # Never add auto lists as they will be handled differently.
                else:
                    pass
        except:
            result = [self.plone_utils.exceptionString()]
        
        return result
    
    # Use security.declarePublic("get_list_password") to allow anonymous users
    # to call this method without the need to login.  This allows to use wget
    # synchronisation with mailman_{autolist|list}_update.py.
    security.declareProtected(ManagePortal, "get_list_password")
    def get_list_password(self, address):
        """
        Returns the admin password for the list defined by address.
        """
        try:
            properties = getToolByName(self, "portal_properties")
            all_lists = properties.mailman_properties.lists
            
            # Browse through the list definitions.
            for mailing_list in all_lists:
                list_data = mailing_list.split(":")
                
                # Verify that this is a correct list definition.
                if len(list_data) < 4:
                    continue
                
                # Iff the list address matches, return the admin password.
                if address == list_data[1]:
                    return list_data[3]
        except:
            return self.plone_utils.exceptionString()
    
    security.declareProtected(ManagePortal, "update_member")
    def update_member(self, member, properties):
        """
        Allows to set Plone member properties for a given member.
        """
        member.setMemberProperties(properties)

InitializeClass(HumaineMailmanTool)
