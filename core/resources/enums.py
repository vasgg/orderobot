from enum import Enum


class OrderStatus(Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    WIP = 'wip'
    DELETED = 'deleted'
    DONE = 'done'


class UserType(Enum):
    CUSTOMER = 'customer'
    FREELANCER = 'freelancer'
