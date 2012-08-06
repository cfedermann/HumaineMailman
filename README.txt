HumaineMailman
==============

Plone 4 compatible release of the HumaineMailman product.

1. Overview
-----------

This product allows Plone portal users to ``subscribe`` or ``unsubscribe`` to Mailman mailing lists and, thus, to embed Mailman mailing lists into a Plone portal.

The portal manager can set up open or role-based mailing lists as well as so-called "auto lists", i.e.m mailing lists that get populated using a Python script.  In order to allow easy integration into the Plone portal, there exists an auto list "sandbox" which allows to preview the effects of the script code before actually using it.

Portal users get an additional preferences panel that allows to subscribe to all lists the user may access.  The user data can be synced using a shell script (that should be called regularly by a cronjob).

The product code has been developed in 2007 and is actively used to this day on the `HUMAINE portal <http://emotion-research.net>`_. It has been released to the so that others can use it as well, hoping that some may find it useful.

The code has recently been upgraded to version 1.1, adding support for Plone 4, and moved to GitHub.

2. Install HumaineMailman
-------------------------

Copy the downloaded ``HumaineMailman`` folder into your Plone instance's ``products`` folder. Make sure that the folder is named ``HumaineMailman`` as this is required for properly importing it!

This product can be installed using the Plone ``portal_quickinstaller`` tool in the Zope Management Interface.  The product will install:

 1. a tool named ``mailman_tool`` into your Plone instance's root folder;
 2. a configlet named ``mailman_preferences`` and corresponding ``HumaineMailmanPreferences`` entry inside ``portal_controlpanel``;
 3. a portal action named ``mailman_member_preferences``;
 4. a custom Javascript file named ``mailman_preferences.js``;
 5. a member property named ``mailing_lists``;
 6. a property sheet named ``mailman_properties``.

**IMPORTANT:** before you can actually use HumaineMailman, you will have to prepare one or several Mailman mailing lists. Please also read the documentation inside ``docs`` before using HumaineMailman.

3. Uninstall HumaineMailman
---------------------------

To remove the product from your Plone instance, just select "Uninstall" in the ``portal_quickinstaller`` tool.  This will remove:

 1. the tool ``mailman_tool``;
 2. the portal action ``mailman_member_preferences``;
 3. the custom Javascript file ``mailman_preferences.js``.

Member properties inside ``mailing_lists`` and anything inside ``mailman_properties`` will **NOT** be deleted so your mailing list settings will remain available. Sadly, Plone's GenericSetup mechanism will **OVERWRITE** any pre-existing settings on re-install, so it is a good idea to make a backup of your list settings regularly!

**NOTE:** for some reason, the QuickInstaller will not remove the ``HumaineMailmanPreferences`` entry inside ``portal_controlpanel``. You have to delete it manually when uninstalling this product.

3. Credits
----------

Developed by `Christian Federmann <http://www.dfki.de/~cfedermann/>`_, note that this software is not actively maintained due to lack of funding.

This work has been supported by the `EC Project HUMAINE (IST-507422) <http://emotion-research.net/>`_.

4. Changelog
------------

 - 2012-08-06 1.1 "Hordaland"
 - 2007-11-22 1.0 "Narvik"
 - 2007-05-14 0.3 "Hammerfest"
 - 2007-04-12 0.2 "Bjoergvin"
 - 2007-03-27 0.1 "Kobenhavn"