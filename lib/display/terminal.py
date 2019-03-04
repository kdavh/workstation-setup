from termcolor import colored
from types import SimpleNamespace

from events import (
    INSTALL_STARTED, INSTALL_SUCCEEDED, INSTALL_FAILED, INSTALL_ALREADY_DONE,
    EXPORT_STARTED, EXPORT_SUCCEEDED, EXPORT_FAILED, EXPORT_ALREADY_DONE,
    PULLING_PACKAGE_REPO,
)


mood = SimpleNamespace(
    highlight=lambda s: colored(s, 'yellow'),
    success=lambda s: colored(s, 'green'),
    failed=lambda s: colored(s, 'red'),
    subtle=lambda s: colored(s, 'blue'),
    notable=lambda s: colored(s, 'blue'),
)


class TerminalDisplay():
    INDENT = '  '

    def __init__(self):
        self._pending = []
        self._current_event = None
        self._previous_message = ('', ('__INIT__', None))

    def handle(self, event_name: str, data):
        self._current_event = (event_name, data)

        if event_name == INSTALL_STARTED:
            self._add_pending(data.full)

        elif event_name == INSTALL_SUCCEEDED:
            self._pop_pending()
            self.info(
                self._with_pending_display(mood.success(data.full + ' -- Installed ✓✓✓'))
            )

        elif event_name == INSTALL_FAILED:
            self._pop_pending()
            self.warn(
                self._with_pending_display(mood.failed(data.full + ' -- Install Failed'))
            )

        elif event_name == INSTALL_ALREADY_DONE:
            self._pop_pending()
            self.info(
                self._with_pending_display(mood.subtle(data.full + ' -- already installed, skipping'))
            )


        elif event_name == EXPORT_STARTED:
            self._add_pending(data.full)

        elif event_name == EXPORT_SUCCEEDED:
            self._pop_pending()
            self.info(
                self._with_pending_display(mood.success(data.full + ' -- Exported ✓✓✓'))
            )

        elif event_name == EXPORT_FAILED:
            self._pop_pending()
            self.warn(
                self._with_pending_display(mood.failed(data.full + ' -- Export Failed'))
            )

        elif event_name == EXPORT_ALREADY_DONE:
            self._pop_pending()
            self.info(
                self._with_pending_display(mood.subtle(data.full + ' -- no export needed'))
            )

        elif event_name == PULLING_PACKAGE_REPO:
            if self._previous_message[1][0] != event_name or self._previous_message[1][1] != data:
                self.info(mood.subtle('Updating package definitions for ' + data))

    def _with_pending_display(self, message) -> str:
        if self._pending:
            return mood.subtle(
                'Dependency for (' + ' > '.join(self._pending or self._pending) + ') '
            ) + message
        else:
            return message

    def _pop_pending(self):
        self._pending = self._pending[0:-1]

    def _add_pending(self, item):
        self._pending.append(item)

    def _indent(self, length: int) -> str:
        return self.INDENT * length

    def info(self, s, *args, **kwargs):
        print(s, *args, **kwargs)
        self._previous_message = (s, self._current_event)

    def warn(self, s, *args, **kwargs):
        print(s, *args, **kwargs)
        self._previous_message = (s, self._current_event)
