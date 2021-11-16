from home_intent import Intents

intents = Intents(__name__)


class BaseShoppingList:
    def __init__(self, home_assistant, home_intent):
        self.ha = home_assistant
        self.home_intent = home_intent

    @intents.slots
    def shopping_item(self):
        item_file = self.home_intent.get_file("home_assistant/shopping_items.txt")
        return item_file.read_text().strip().split("\n")

    def _add_item_to_shopping_list(self, shopping_item):
        self.ha.api.call_service("shopping_list", "add_item", {"name": shopping_item})

    def _mark_item_complete_on_shopping_list(self, shopping_item):
        self.ha.api.call_service("shopping_list", "complete_item", {"name": shopping_item})

    def _unmark_item_complete_on_shopping_list(self, shopping_item):
        self.ha.api.call_service("shopping_list", "incomplete_item", {"name": shopping_item})

    def _mark_everything_complete_on_shopping_list(self):
        self.ha.api.call_service("shopping_list", "complete_all")

    def _unmark_everything_complete_on_shopping_list(self):
        self.ha.api.call_service("shopping_list", "incomplete_all")
