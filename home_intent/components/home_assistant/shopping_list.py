from pathlib import Path

from home_intent import Intents

intents = Intents(__name__)


class ShoppingList:
    def __init__(self, home_assistant):
        self.ha = home_assistant

    @intents.slots
    def shopping_item(self):
        item_file = Path("home_intent/components/home_assistant/shopping_items.txt")
        return item_file.read_text().strip().split("\n")

    @intents.sentences(["add ($shopping_item) to the [shopping] list"])
    def add_item_to_shopping_list(self, shopping_item):
        self.ha.api.call_service("shopping_list", "add_item", {"name": shopping_item})
        return f"Adding {shopping_item} to the shopping list."

    @intents.sentences(
        ["(mark|check) ($shopping_item) off the [shopping] list",]
    )
    def mark_item_complete_on_shopping_list(self, shopping_item):
        self.ha.api.call_service("shopping_list", "complete_item", {"name": shopping_item})
        return f"Checking off {shopping_item} from the shopping list."

    @intents.sentences(
        ["(unmark | uncheck) ($shopping_item) from the [shopping] list",]
    )
    def unmark_item_complete_on_shopping_list(self, shopping_item):
        self.ha.api.call_service("shopping_list", "incomplete_item", {"name": shopping_item})
        return f"Adding item {shopping_item} to list!"

    @intents.sentences(
        ["(mark | check) everything off the [shopping] list",]
    )
    def mark_everything_complete_on_shopping_list(self):
        self.ha.api.call_service("shopping_list", "complete_all")
        return "Everything has been checked off the shopping list."

    @intents.sentences(
        ["(unmark | uncheck) everything from the [shopping] list",]
    )
    def unmark_everything_complete_on_shopping_list(self):
        self.ha.api.call_service("shopping_list", "incomplete_all")
        return "Everything has been unchecked from the shopping list."

    @intents.sentences(["[tell me] what is on the [shopping] list"])
    def display_list_items(self):
        return "I can't do that yet..."
