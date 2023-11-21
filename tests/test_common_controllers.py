from unittest import IsolatedAsyncioTestCase

from core.controllers.common_controllers import change_order_status
from core.database.db import db
from core.database.models import Order
from core.resources.enums import OrderStatus


class Test(IsolatedAsyncioTestCase):
    async def test_change_entity_status(self):
        order = Order(customer_id=1)
        async with db.session_factory.begin() as session:
            session.add(order)
            await session.commit()
        self.assertEqual(order.status, OrderStatus.DRAFT)
        async with db.session_factory.begin() as session:
            await change_order_status(order, entity_id=1, status=OrderStatus.WIP, session=session)
            await session.commit()

        # self.fail()
        await db.engine.dispose()
