## Controller Python Script "mailman_list_update"

##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=HumaineMailman List Update
##
request = container.REQUEST
RESPONSE = request.RESPONSE

list_name = request.get("list", None)
list_password = request.get("password", None)

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

# Return the list of subscribed email addresses.
list_emails = [x[1] for x in context.mailman_tool.get_list_members(list_name)]

# Return a warning message if mailing list is empty.
if not list_emails:
    RESPONSE.setStatus(500)
    return ["Empty mailing list!"]

return "\n".join(list_emails)