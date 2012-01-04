from Products.LinguaPlone import patches

_enabled = []


def AlreadyApplied(patch):
    if patch in _enabled:
        return True
    _enabled.append(patch)
    return False


def QueryAllLanguagesForAuthenticatedCatalog():
    # Patches the catalog tool to filter languages
    if AlreadyApplied('QueryAllLanguagesForAuthenticatedCatalog'):
        return

    from Products.CMFPlone.CatalogTool import CatalogTool
    
    def searchResults(self, REQUEST=None, **kw):
        """ This version returns the results for all languages if
            the user is authenticated.
        """

        if hasattr(self, 'REQUEST'):
            langtool = self.REQUEST.get('LANGUAGE_TOOL', None)
            if langtool is not None:
                if not langtool.tool.isAnonymousUser():
                    if REQUEST is not None and not REQUEST.has_key('Language'):
                        REQUEST['Language'] = 'all'
                    elif REQUEST is None and not kw.has_key('Language'):
                        kw['Language'] = 'all'

        return self.__valentine_old_searchResults(REQUEST, **kw)

    CatalogTool.__valentine_old_searchResults = CatalogTool.searchResults
    CatalogTool.searchResults = searchResults
    CatalogTool.__call__ = searchResults

QueryAllLanguagesForAuthenticatedCatalog()
