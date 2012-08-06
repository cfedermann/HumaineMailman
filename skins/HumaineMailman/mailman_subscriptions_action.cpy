## Controller Python Script "mailman_subscriptions_action"

##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=HumaineMailman Subscriptions Action
##
request = container.REQUEST
RESPONSE = request.RESPONSE

try:
    action = request.get("action", None)
    emails = str(request.get("emails", ""))
    address = request.get("mailinglist_select", None)
    RESPONSE.setCookie("emails", emails)
    RESPONSE.setCookie("mailinglist_select", address)
    
    if action == "subscribe":
        emails = emails.replace("\r\n", "\n")
        emails = emails.split("\n")
        context.mailman_tool.subscribe_list(address, emails)
        state.set(portal_status_message="Successfully updated subscriptions.")
    
    elif action == "unsubscribe":
        emails = emails.replace("\r\n", "\n")
        emails = emails.split("\n")
        context.mailman_tool.unsubscribe_list(address, emails)
        state.set(
          portal_status_message="Successfully updated subscriptions."
        )

except:
    state.set(status="failure")
    state.set(
      portal_status_message="An error occured when updating subscriptions."
    )

return state
