"""
Project: HumaineMailman
 Author: Christian Federmann <cfedermann@dfki.de>

This work has been supported by the EC Project HUMAINE (IST-507422);
See http://emotion-research.net/ for more information.
"""
from Products.CMFCore.utils import ToolInit
from Products.CMFCore.DirectoryView import registerDirectory

from Products.HumaineMailman.config import PKG_NAME, GLOBALS, SKINS_DIR, ICON
from Products.HumaineMailman.HumaineMailmanTool import HumaineMailmanTool

def initialize(context):
    registerDirectory(SKINS_DIR, GLOBALS)
    
    ToolInit("{0} Tool".format(PKG_NAME),
      tools = (HumaineMailmanTool,),
      icon = ICON
    ).initialize(context)
