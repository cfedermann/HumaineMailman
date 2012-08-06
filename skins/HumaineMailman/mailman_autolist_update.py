## Controller Python Script "mailman_autolist_update"

##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=list=None,password=None
##title=HumaineMailman Autolist Update
##
request = container.REQUEST
RESPONSE = request.RESPONSE

list_name = request.get("list", list)
list_password = request.get("password", password)

# Verify that list address and password have been given.
if not list_name or not list_password:
    RESPONSE.setStatus(500)
    return ["Incomplete request!"]

list_emails = []
check_password = context.mailman_tool.get_list_password(list_name)

# Verify that the access to the list data is allowed.
if not list_password == check_password:
    RESPONSE.setStatus(500)
    return ["Unauthorized access!"]

# Place your autolist code here...
#
#if list_name == "some-list@some-host":
#    list_emails = ["some", "entries", "are", "now", "inside", "this", "list"]
#
# The following example code returns all current Plone site members
# for an autolist called 'all@your-host'.
#
#if list_name == "all@your-host":
#    members = context.portal_membership.listMembers()
#    list_emails = [member.getProperty("email") for member in members]
#
#else:
#    list_emails = ["warning: unknown list '{0}'".format(list_name)]

return "\n".join(list_emails)
