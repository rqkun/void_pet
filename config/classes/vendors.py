
import millify
from components import cards
from config.constants import Warframe
from utils import data_manage, tools


from datetime import datetime


class Vendor:
    """Base class representing a generic vendor in Warframe.

    Attributes:
        json_data (dict): Raw data for the vendor.
        type (Enum or None): Type of the vendor.
        currency (list): List of supported currency types.
        inventory (list): Complete list of vendor items.
        filtered_inventory (list): Filtered subset of the inventory.
    """
    def __init__(self, json_data: dict):
        """Initialize a Vendor with given JSON data."""
        self.json_data = json_data
        self.type = None
        self.currency = []
        self.inventory = []
        self.filtered_inventory = []

    def is_active(self) -> bool:
        """Check if the vendor is currently active.

        Returns:
            bool: True if the vendor is active, False otherwise.
        """
        return self.json_data.get("active", False)

    def get(self, key: str, default=None):
        """Retrieve a value from the vendor's data.

        Args:
            key (str): The key to retrieve from the JSON data.
            default (any, optional): Default value if the key is not found.

        Returns:
            any: The value associated with the key or the default value.
        """
        return self.json_data.get(key, default)

    def _format_time(self, key: str) -> str:
        """Internal method to format time from vendor data.

        Args:
            key (str): The key to retrieve the timestamp.

        Returns:
            str: Human-readable time duration.
        """
        date = datetime.strptime(self.json_data.get(key, datetime.today().isoformat()), "%Y-%m-%dT%H:%M:%S.%fZ") - datetime.today()
        return tools.format_timedelta(date)

    def arrive_time(self) -> str:
        """Get the time until the vendor arrives.

        Returns:
            str: Formatted time until activation.
        """
        return self._format_time("activation")

    def leave_time(self) -> str:
        """Get the time until the vendor leaves.

        Returns:
            str: Formatted time until expiry.
        """
        return self._format_time("expiry")

    def preload(self) -> None:
        """Preload the vendor's inventory if the vendor is active."""
        if self.is_active():
            self.inventory = data_manage.preload_data(self.json_data.get("inventory", []))

    def filter(self, filters: list) -> list:
        """Filter the inventory based on provided criteria.

        Args:
            filters (list): List of filter conditions.

        Returns:
            list: Filtered inventory.
        """
        self.filtered_inventory = tools.filter_data(self.inventory["items"], filters)

    def check(self) -> dict:
        """Check the vendor's status and generate an alert message.

        Returns:
            dict: Contains the active status and a formatted message.
        """
        time_string = self.leave_time() if self.is_active() else self.arrive_time()
        action_string = "leave" if self.is_active() else "arrive"
        alert_message = f"{self.type['name']} will {action_string} in {time_string}"
        return {
            "active": self.is_active(),
            "message": alert_message
        }

    def parse_items(self, start_idx: int, end_idx: int) -> list:
        """Parse and format inventory items for display.

        Args:
            start_idx (int): Start index for item parsing.
            end_idx (int): End index for item parsing.

        Returns:
            list: List of filtered items between start and end index.
        """
        for item in self.filtered_inventory[start_idx:end_idx]:
            item["image"] = data_manage.get_image_url(item["uniqueName"])

            currency_type, amount = (self.currency[0], item["ducats"]) if item["ducats"] > 0 else (self.currency[1], item["credits"])

            item["html"] = cards.generic(
                package=item,
                image_url=item["image"],
                price_info={
                    "type": currency_type,
                    "amount": millify.millify(amount, precision=2)
                }
            )
        return self.filtered_inventory[start_idx:end_idx]


class VoidTraider(Vendor):
    """Represents Baro Ki'Teer in Warframe."""
    def __init__(self):
        """Initialize the VoidTrader with specific attributes."""
        super().__init__(data_manage.get_baro())
        self.type = Warframe.BARO.value
        self.currency = [Warframe.DUCAT.value, Warframe.CREDITS.value]


class VaultTraider(Vendor):
    """Represents Varzia in Warframe."""
    def __init__(self):
        """Initialize the VaultTrader with specific attributes."""
        super().__init__(data_manage.get_variza())
        self.type = Warframe.VARZIA.value
        self.currency = [Warframe.REGAL_AYA.value, Warframe.AYA.value]
