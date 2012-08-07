## Controller Python Script "mailman_export_content"

##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=HumaineMailman Exporter
##
request = container.REQUEST
RESPONSE = request.RESPONSE

RESPONSE.setHeader("Content-type", "text/xml")
return context.mailman_tool.export_content()