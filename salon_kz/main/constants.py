CLIENT = 'client'
MASTER = 'master'
PARTNER = 'partner'
ADMIN = 'admin'


USER_TYPES = (
    (CLIENT, CLIENT),
    (MASTER, MASTER),
    (PARTNER, PARTNER),
    (ADMIN, ADMIN),
)

NEW_ORDER = 'new_order'
CANCELED_ORDER = 'canceled_order'
SERVICE_RENDERED = 'service_rendered'
SERVICE_PAID = 'service_paid'

ORDER_FLAGS =(
    (NEW_ORDER, NEW_ORDER),
    (CANCELED_ORDER, CANCELED_ORDER),
    (SERVICE_RENDERED, SERVICE_RENDERED),
    (SERVICE_PAID, SERVICE_PAID)
)

t9 = True
t10 = True
t11 = True
t12 = True
t13 = True
t14 = True
t15 = True
t16 = True
t17 = True

# TIMES = (
#     ('9:00', True),
#     ('10:00', True),
#     ('11:00', True),
#     ('12:00', True),
#     ('13:00', True),
#     ('14:00', True),
#     ('15:00', True),
#     ('16:00', True),
#     ('17:00', True),
# )

TIMES = [
    t9, t10, t11, t12, t13, t14, t15, t16, t17
]

