import logging
from typing import Any

from app.exceptions import InvalidTransition, AbortTransition

logger = logging.getLogger(__name__)


class FiniteStateMachineMixin:
    """
    Base Mixin to add a state_machine behavior.
    Inspired from https://github.com/woile/pyfsm/
    Represents the state machine for the object.
    The states and transitions should be specified in the following way:
    .. code-block:: python
        TRANSITIONS = {
           'some_state': '__all__'
           'another_state': ('some_state', 'one_more_state')
           'one_more_state': None
        }
    Requires the implementation of :code:`current_state` and :code:`set_state`
    """

    TRANSITIONS = None

    def set_state(self, state: str or int) -> Any:
        """Update the internal state field.
        :param state: type depends on the definition of the states.
        """
        raise NotImplementedError()

    def current_state(self) -> str or int:
        """Returns the current state in the FSM."""
        raise NotImplementedError()

    def can_change(self, next_state: str or int) -> bool:
        """Validates if the next_state can be executed or not.

        It uses the state_machine attribute in the class.
        """
        valid_transitions = self.get_valid_transitions()

        if not valid_transitions:
            return False

        return next_state in valid_transitions

    def get_valid_transitions(self) -> tuple or list:
        """Return possible states to whom a product can transition.

        :returns: valid transitions
        """
        current = self.current_state()
        valid_transitions = self.TRANSITIONS[current]

        if valid_transitions == "__all__":
            return self.TRANSITIONS.keys()

        return self.TRANSITIONS[current]

    def on_before_change_state(self, previous_state: str or int, next_state: str or int, **kwargs) -> Any:
        """Called before a state changes.

        :param previous_state: type depends on the definition of the states.
        :param next_state: type depends on the definition of the states.
        """
        pass

    def on_change_state(self, previous_state: str or int, next_state: str or int, **kwargs) -> Any:
        """Called after a state changes.

        :param previous_state: type depends on the definition of the states.
        :param next_state: type depends on the definition of the states.
        """
        pass

    def on_manage_error(self, next_state: str or int, error: Exception, **kwargs) -> Any:
        """Call this if an error needs to be managed on a specific way.
        You must implement this method on the Child class.

        :param next_state: type depends on the definition of the states.
        :param error: the error to manage
        """
        pass

    def change_state(self, next_state: str or int, manage_error: bool = False, **kwargs) -> str or int:
        """Performs a transition from current state to the given next state if
        possible.

        Callbacks will be executed before an after changing the state.
        Specific state callbacks will also be called if they are implemented
        in the subclass.

        :param next_state: where the state must go
        :param manage_error: for use in case that an error needs to be managed on a specific way.
        :returns: new state.
        :raises InvalidTransition: If transitioning is not possible
        :raises AbortTransition: If transitioning not meet a validation
        """
        previous_state = self.current_state()

        if not self.can_change(next_state):
            msg = f"The transition from {previous_state} to {next_state} is not valid"
            logger.info(msg)
            raise InvalidTransition(msg)

        name = f"on_before_{next_state.lower()}_callback"
        callback = getattr(self, name, None)
        if callback:
            try:
                callback(**kwargs)
            except AbortTransition:
                name = f"on_aborted_{next_state}_callback"
                aborted_callback = getattr(self, name, None)
                logger.exception(f'Transition to {next_state} was not completed')
                if manage_error:
                    return aborted_callback(**kwargs) if aborted_callback else None
                raise AbortTransition
            except Exception as e:
                logger.exception(f"An error occurred while trying to call callback: {e}")
                if manage_error:
                    return self.on_manage_error(next_state, e, **kwargs)
                raise e

        self.on_before_change_state(previous_state, next_state, **kwargs)

        self.set_state(next_state)

        name = f"on_{next_state}_callback"
        callback = getattr(self, name, None)
        if callback:
            callback(**kwargs)

        self.on_change_state(previous_state, next_state, **kwargs)
        return next_state
