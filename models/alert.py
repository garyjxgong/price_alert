import uuid
from dataclasses import dataclass, field
from models.item import Item
from models.user import User
from models.model import Model
from libs.mailgun import Mailgun


@dataclass(eq=False)
class Alert(Model):
    collection: str = field(init=False, default="alerts")
    name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> dict:
        return {
            "_id": self._id,
            "name": self.name,
            "item_id": self.item_id,
            "price_limit": self.price_limit,
            "user_email": self.user_email
        }

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self) -> None:
        if self.item.price < self.price_limit:
            print(f"Item {self.item} has reached a price under {self.price_limit}. "
                  f"Latest price: {self.item.price}.")
            Mailgun.send_mail(
                [self.user_email],
                f'Notification for {self.name}',
                f'Your alert {self.name} has reached a price under{self.price_limit}.'
                f'The latest price is {self.item.price}.'
                f'Go to this address to check your item: {self.item.url}',
                f'<p>Your alert {self.name} has reached a price under{self.price_limit}.</p>'
                f'<p>The latest price is {self.item.price}.</p>'
                f'<p>Click <a href="{self.item.url}">here</a> to check your item.</p>'
            )
