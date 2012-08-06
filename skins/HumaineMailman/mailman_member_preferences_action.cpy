## Controller Python Script "mailman_member_preferences_action"

##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=HumaineMailman Member Preferences Action
##
request = container.REQUEST
RESPONSE = request.RESPONSE

try:
    # Get member object from the given id
    member_object = context.portal_membership.getAuthenticatedMember()
    
    # Get mailing list information.
    mailing_lists = int(request.get("checkboxes"))
    member_lists = []
    
    # Browse through all mailing lists.
    for index in range(mailing_lists):
        checked = request.get("checkbox_{0}".format(index), False)
        address = request.get("address_{0}".format(index), None)
        
        # Update member_lists iff the current mailing list was checked.
        if checked and address:
            member_lists.append(address)
    
    # Update the mailing list subscriptions for the given member.
    member_object.setProperties(mailman_lists=tuple(member_lists))
    state.set(
      portal_status_message="Successfully updated mailing list subscriptions."
    )

except:
    state.set(status="failure")
    state.set(
      portal_status_message="An error occured when updating mailing list " \
        "subscriptions.  Exception: '{0}'".format(
        context.plone_utils.exceptionString())
    )

return state