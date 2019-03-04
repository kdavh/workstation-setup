class EventStream():
    def __init__(self, *listeners):
        self._listeners = listeners

    def push(self, event_name: str, data: any):
        for listener in self._listeners:
            listener.handle(event_name, data)


INSTALL_STARTED = 'INSTALL_STARTED'
INSTALL_SUCCEEDED = 'INSTALL_SUCCEEDED'
INSTALL_FAILED = 'INSTALL_FAILED'
INSTALL_ALREADY_DONE = 'INSTALL_ALREADY_DONE'
INSTALL_FORCED = 'INSTALL_FORCED'

EXPORT_STARTED = 'EXPORT_STARTED'
EXPORT_SUCCEEDED = 'EXPORT_SUCCEEDED'
EXPORT_FAILED = 'EXPORT_FAILED'
EXPORT_ALREADY_DONE = 'EXPORT_ALREADY_DONE'

PULLING_PACKAGE_REPO = 'PULLING_PACKAGE_REPO'
