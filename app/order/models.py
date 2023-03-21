from django.db import models

from order.states.state_machine import OrderFSMMixin
from order.states.states import OrderStates


class Order(models.Model, OrderFSMMixin):
    details = models.CharField(max_length=200)
    client_id = models.CharField(max_length=10)
    state = models.CharField(max_length=50, choices=OrderStates.CHOICES, default=OrderStates.CREATED)
