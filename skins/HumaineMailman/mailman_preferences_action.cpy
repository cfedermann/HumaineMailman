## Controller Python Script "mailman_preferences_action"

##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=HumaineMailman Preferences Action
##
request = container.REQUEST
RESPONSE = request.RESPONSE

try:
    updated_lists = request.get("lists")
    context.portal_properties.mailman_properties.manage_changeProperties(
      {"lists": updated_lists}
    )
    state.set(
      portal_status_message="Successfully updated global preferences."
    )

except:
    state.set(status="failure")
    state.set(
      portal_status_message="An error occured when updating global " \
        "preferences."
    )

RESPONSE.setCookie("panel", "global")
return state
