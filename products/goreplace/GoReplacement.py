# -*- coding: utf-8 -*-
#
# File: GoReplacement.py
#
# Copyright (c) 2014 by unknown <unknown>
# Generator: ArchGenXML Version 2.6
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """unknown <unknown>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from products.goreplace.config import *

# code-section module-header #fill in your manual code here
import re
# /code-section module-header

schema = Schema((

    TextField(
        name='find',
        default="""(?is)<a(.*?)href=['"](.*?)['"](.*?)>""",
        mimetype="text/html",
        widget=TextAreaWidget(
            label='Find',
            label_msgid='GoReplace_label_find',
            i18n_domain='GoReplace',
        ),
        default_output_type="text/html",
    ),
    TextField(
        name='replace',
        default="""<a\\1href="http://gogo.bluedynamics.com"\\3> <!-- was: "\\2" -->""",
        mimetype="text/html",
        widget=TextAreaWidget(
            label='Replace',
            label_msgid='GoReplace_label_replace',
            i18n_domain='GoReplace',
        ),
        default_output_type="text/html",
    ),
    BooleanField(
        name='regex',
        default=1,
        widget=BooleanField._properties['widget'](
            label='Regex',
            label_msgid='GoReplace_label_regex',
            i18n_domain='GoReplace',
        ),
    ),
    BooleanField(
        name='repr',
        default=0,
        widget=BooleanField._properties['widget'](
            label='Repr',
            label_msgid='GoReplace_label_repr',
            i18n_domain='GoReplace',
        ),
    ),
    LinesField(
        name='fields',
        default=["title", "description", "text"],
        widget=LinesField._properties['widget'](
            label='Fields',
            label_msgid='GoReplace_label_fields',
            i18n_domain='GoReplace',
        ),
    ),
    StringField(
        name='catalog_search',
        widget=StringField._properties['widget'](
            maxlen=4096,
            size=150,
            label='Catalog_search',
            label_msgid='GoReplace_label_catalog_search',
            i18n_domain='GoReplace',
        ),
    ),

),
)

# code-section after-local-schema #fill in your manual code here
# /code-section after-local-schema

GoReplacement_schema = BaseSchema.copy() + \
    schema.copy()

# code-section after-schema #fill in your manual code here
# /code-section after-schema


class GoReplacement(BaseContent, BrowserDefaultMixin):

    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IGoReplacement)

    meta_type = 'GoReplacement'
    _at_rename_after_creation = True

    schema = GoReplacement_schema

    # code-section class-header #fill in your manual code here
    # /code-section class-header

    # Methods

    security.declarePublic('wet_run')

    def wet_run(self):
        """
        """
        self.REQUEST.set('replacements', self.do_run(change=True))
        return self.run()

    security.declarePublic('dry_run')

    def dry_run(self):
        """
        """
        replacements = self.do_run(change=False)
        self.REQUEST.set('replacements', replacements)
        return replacements

    # Manually created methods

    security.declarePublic('getValue')

    def getValue(self, o, name):
        """
        """
        f = o.getField(name)
        if f:
            a = f.edit_accessor
            return o[a]()
        else:
            summary = "Replace failed"
            message = "Can not read from field %s @ %s" % (repr(name), repr(o))
            logger.log(logging.WARNING, '%s \n%s', summary, message)

    security.declareProtected("Manage Portal", 'setValue')

    def setValue(self, o, name, value):
        """
        """
        f = o.getField(name)
        if f:
            c = f.getContentType(o)
            m = f.mutator
            o[m](value)
            if f.getContentType(o) != c:
                # Workaround to fix content type change bug
                f.setContentType(o, c)
        else:
            summary = "Replace failed"
            message = "Can not write to field %s @ %s" % (repr(name), repr(o))
            logger.log(logging.WARNING, '%s \n%s', summary, message)

    security.declareProtected("Manage Portal", 'replaceValue')

    def replaceValue(self, o, name):
        """
        """
        val = self.getValue(o, name)
        find = self.getFind()
        replace = self.getReplace()

        if not val:
            return val
        if self.getRegex():
            if not getattr(self, '_reg', False):
                self._reg = re.compile(find)
            #import pdb;pdb.set_trace()
            rep = self._reg.sub(replace, val)
        else:
            rep = val.replace(find, replace)
        return rep

    def do_run(self, change=False):
        # brains = self.getTopics().queryCatalog()
        brains = eval("self.portal_catalog.searchResults(%s)" %
                      self.getCatalog_search())
        res = {'objectchangecount': 0,
               'fieldchangecount': 0,
               'itemcount': len(brains),
               'replacements': [], }
        i = 0
        for brain in brains:
            i = i + 1
            print "%d/%d [%s] %s" % (i, len(brains), brain.meta_type, brain.getURL()),
            o = brain.getObject()
            fres = []
            ores = {}
            ores['changed'] = False
            ores['uid'] = o.UID()
            ores['meta_type'] = o.meta_type
            ores['icon'] = o.getIcon()
            for field in self.getFields():
                if not o.getField(field):
                    continue
                o_val = self.getValue(o, field)
                r_val = self.replaceValue(o, field)
                changed = (o_val != r_val)
                fres.append(
                    {'name': field,
                        'old': o_val,
                        'new': r_val,
                        'changed': changed, })
                if changed:
                    res['fieldchangecount'] += 1
                    ores['changed'] = True
                    if change:
                        self.setValue(o, field, r_val)
            if ores['changed']:
                res['objectchangecount'] += 1
                o.reindexObject()
                print "*"
            else:
                print
            ores['fields'] = fres
            ores['id'] = o.id
            res['replacements'].append(ores)
        return res

    def at_post_edit_script(self):
        self._reg = None


registerType(GoReplacement, PROJECTNAME)
# end of class GoReplacement

# code-section module-footer #fill in your manual code here
# /code-section module-footer
