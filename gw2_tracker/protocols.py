"""
Module containing protocols used for typechecking

This module also provide a sort of specification
"""
from __future__ import annotations

from typing import Any, Callable, Protocol

import outcome

from gw2_tracker import models


class TrioHostProto(Protocol):
    """
    Protocol for running trio in a host event loop using trio guest mode.

    An object implementing this protocol is used by the controller to run
    network code in parallel with the UI event loop. The object should be
    implemented by the view to run trio whithin the UI event loop.
    """

    def run_sync_soon_threadsafe(self, func: Callable[[], Any]):
        """
        Must schedule execution of func and be threadsafe.

        See also:
            `trio.lowlevel.start_guest_run`
        """
        ...

    def run_sync_soon_not_threadsafe(self, func: Callable[[], Any]):
        """
        Must schedule execution of func. Need not be threadsafe.

        If a more efficient implementation of ``run_sync_soon`` is available
        if not thread safety is required, this is useful for performances
        """
        ...

    def done_callback(self, trio_outcome: outcome.Outcome):
        """
        Called when the trio event loop has finished. This should terminate
        the host loop.

        When running trio in guest mode, it is best to terminate both the host
        event loop and trio's event loop at the same time. The host loop should
        implement this function to terminate itself, and stop the whole program
        by stopping trio's event loop. This way, both loops start and end at the
        same time.
        """
        ...


class ControllerProto(Protocol):
    """
    Protocol implemented by controllers

    The view will call this protocol upon UI interaction
    """

    def __init__(self, model: models.Model, view: ViewProto):
        ...

    def start_trio_guest(self, host: TrioHostProto):
        """Starts trio in guest mode"""
        ...


class ViewProto(Protocol):
    """
    Protocol for View objects used by the app

    View objects are responsible for handling the display and the main UI event
    loop of the app.
    """

    def get_trio_host(self) -> TrioHostProto:
        """Provide a host that a controller can use to run trio"""
        ...

    def set_controller(self, controller: ControllerProto):
        ...

    def start_ui(self):
        """Start the UI event loop"""
        ...
