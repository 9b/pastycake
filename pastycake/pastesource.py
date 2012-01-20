import abc


class PasteSource:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def new_urls(self, dbcon):
        '''
        must be implemented as generator yielding new, unvisited URLs
        as pairs of (self, path)

        IMPORTANT: requests to db.already_visited_url MUST be made with
        the full url (base_url + path) in order to avoid random
        inter-domain collisions.
        '''
        raise NotImplemented()

    def get_paste(self, path):
        '''
        must return a pair containing (http_status_code, paste_data)
        '''
        raise NotImplemented()

    def full_url(self, path):
        '''
        must return the full uri (base_url + path) for the given path
        '''
        raise NotImplemented()
