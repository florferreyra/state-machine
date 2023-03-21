"""Module for define mixins"""
from app.fsm import FiniteStateMachineMixin
from order.states.states import OrderStates as st


class OrderFSMMixin(FiniteStateMachineMixin):
    """Abstract class to manage the Order state machine.

    Define the TRANSITIONS state machine.

    Define the field state name as `FIELD_NAME`

    And remember always to use `change_state` instead of simply assigning it
    """
    TERMINAL_STATE = []
    FIELD_NAME = "state"

    TRANSITIONS = {
        st.CREATED: [st.WAITING_FOR_PAYMENT, st.CANCELED],
        st.WAITING_FOR_PAYMENT: [st.PROCESSING, st.CANCELED],
        st.PROCESSING: [st.SHIPPING, st.CANCELED],
        st.SHIPPING: [st.COMPLETED],
        st.CANCELED: TERMINAL_STATE,
        st.COMPLETED:   TERMINAL_STATE,
    }

    def current_state(self) -> str:
        """Returns the current state in the FSM."""
        return getattr(self, self.FIELD_NAME)

    def set_state(self, state: str) -> None:
        """Update the internal state field.
        :param state: the new state to set.
        """
        setattr(self, self.FIELD_NAME, state)
