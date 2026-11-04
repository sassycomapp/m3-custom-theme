"""M3 Snackbar: a brief message at the bottom of the screen.
See docs/components/Snackbar.md in the project library.

A Snackbar is not placed in a form. It is created in code and shown with show().
Only one Snackbar is on screen at a time; the others wait in a queue and appear
one after another.
"""
from anvil.js import window

DURATIONS = {"short": 4000, "long": 10000, "indefinite": None}

# The time the leaving animation needs before the element is removed (ms). It
# matches --m3x-motion-duration-short3 in tokens.css.
_EXIT_MS = 150

_queue = []
_current = None
_host = None


def _get_host():
    """The fixed area at the bottom of the page that holds the Snackbar."""
    global _host
    if _host is None:
        _host = window.document.createElement("div")
        _host.className = "m3x-snackbar-host"
        window.document.body.appendChild(_host)
    return _host


def _show_next():
    global _current
    _current = _queue.pop(0) if _queue else None
    if _current is not None:
        _current._open()


class Snackbar:
    """A brief message with an optional action and close button.

    text         the message (one or two lines).
    action_text  the label of the action button, or None for no action.
    on_action    a function called with no arguments when the action is clicked.
    on_dismiss   a function called with no arguments when the Snackbar leaves the
                 screen for any reason.
    show_close   if True, a close button is shown.
    duration     "short" (4 s), "long" (10 s), "indefinite" (until closed or an
                 action is clicked), or a number of seconds.
    """

    def __init__(self, text, action_text=None, on_action=None, on_dismiss=None,
                 show_close=False, duration="short"):
        if duration not in DURATIONS and not isinstance(duration, (int, float)):
            raise ValueError(
                f"Unknown duration {duration!r}. Use 'short', 'long', "
                "'indefinite' or a number of seconds."
            )
        if duration == "indefinite" and not (action_text or show_close):
            show_close = True  # An indefinite Snackbar must offer a way to close it.
        self.text = text
        self.action_text = action_text
        self.on_action = on_action
        self.on_dismiss = on_dismiss
        self.show_close = show_close
        self.duration = duration
        self._node = None
        self._timer = None

    def show(self):
        """Show the Snackbar, after any Snackbar already on screen."""
        _queue.append(self)
        if _current is None:
            _show_next()

    def dismiss(self):
        """Remove the Snackbar from the screen, or from the queue."""
        if self in _queue:
            _queue.remove(self)
            return
        if self is not _current or self._node is None:
            return
        if self._timer is not None:
            window.clearTimeout(self._timer)
            self._timer = None
        node, self._node = self._node, None
        node.classList.remove("m3x-snackbar-shown")
        window.setTimeout(lambda: node.remove(), _EXIT_MS)
        if self.on_dismiss is not None:
            self.on_dismiss()
        window.setTimeout(_show_next, _EXIT_MS)

    def _open(self):
        doc = window.document
        node = doc.createElement("div")
        node.className = "m3x-snackbar"
        node.setAttribute("role", "status")
        node.setAttribute("aria-live", "polite")
        text = doc.createElement("div")
        text.className = "m3x-snackbar-text"
        text.innerText = self.text
        node.appendChild(text)
        if self.action_text:
            action = doc.createElement("button")
            action.className = "m3x-snackbar-action"
            action.type = "button"
            action.innerText = self.action_text
            action.addEventListener("click", self._on_action_click)
            node.appendChild(action)
        if self.show_close:
            close = doc.createElement("button")
            close.className = "m3x-snackbar-close"
            close.type = "button"
            close.setAttribute("aria-label", "Close")
            icon = doc.createElement("i")
            icon.className = "material-symbols-outlined"
            icon.setAttribute("aria-hidden", "true")
            icon.innerText = "close"
            close.appendChild(icon)
            close.addEventListener("click", lambda event: self.dismiss())
            node.appendChild(close)
        _get_host().appendChild(node)
        self._node = node
        # Add the class one frame later, so the entering animation runs.
        window.requestAnimationFrame(
            lambda t: node.classList.add("m3x-snackbar-shown")
        )
        ms = DURATIONS.get(self.duration, None)
        if isinstance(self.duration, (int, float)):
            ms = int(self.duration * 1000)
        if ms is not None:
            self._timer = window.setTimeout(self.dismiss, ms)

    def _on_action_click(self, event):
        if self.on_action is not None:
            self.on_action()
        self.dismiss()
