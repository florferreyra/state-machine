

class OrderStates:
    CREATED = 'created'
    WAITING_FOR_PAYMENT = 'waiting_for_payment'
    PROCESSING = 'processing'
    SHIPPING = 'shipping'
    COMPLETED = 'completed'
    CANCELED = 'canceled'

    CHOICES = [
        (CREATED, CREATED),
        (WAITING_FOR_PAYMENT, WAITING_FOR_PAYMENT),
        (PROCESSING, PROCESSING),
        (SHIPPING, SHIPPING),
        (COMPLETED, COMPLETED),
        (CANCELED, CANCELED)
    ]
