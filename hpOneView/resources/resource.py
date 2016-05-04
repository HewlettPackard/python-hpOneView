from hpOneView.activity import activity


class Resource(object):
    def __init__(self, connection):
        self._connection = connection
        self._activity = activity(connection)
