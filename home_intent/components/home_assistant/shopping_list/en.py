from .base_shopping_list import intents, BaseShoppingList


class ShoppingList(BaseShoppingList):
    def __init__(self, home_assistant, language):
        self.ha = home_assistant
        self.language = language

    @intents.sentences(["add ($shopping_item) to the [shopping] list"])
    def add_item_to_shopping_list(self, shopping_item):
        self._add_item_to_shopping_list(shopping_item)
        return f"Adding {shopping_item} to your shopping list"

    @intents.sentences(
        ["(mark|check) ($shopping_item) off the [shopping] list",]
    )
    def mark_item_complete_on_shopping_list(self, shopping_item):
        self._mark_item_complete_on_shopping_list(shopping_item)
        return f"Checking off {shopping_item} from your shopping list"

    @intents.sentences(
        ["(unmark | uncheck) ($shopping_item) from the [shopping] list",]
    )
    def unmark_item_complete_on_shopping_list(self, shopping_item):
        self._unmark_item_complete_on_shopping_list(shopping_item)
        return f"Unchecking {shopping_item} from your shopping list"

    @intents.default_disable("Causes system confustion")
    @intents.sentences(
        ["(mark | check) everything off the [shopping] list",]
    )
    def mark_everything_complete_on_shopping_list(self):
        self._mark_everything_complete_on_shopping_list()
        return "Checking everything off of your shopping list"

    @intents.default_disable("Causes system confustion")
    @intents.sentences(
        ["(unmark | uncheck) everything from the [shopping] list",]
    )
    def unmark_everything_complete_on_shopping_list(self):
        self._unmark_everything_complete_on_shopping_list()
        return "Unchecking everything from your shopping list."

    @intents.default_disable("Doesn't actually work...")
    # Not entirely sure how to get the items from the shopping list via the API.
    # Will have to do some discovery around it.
    @intents.sentences(["[tell me] what is on the [shopping] list"])
    def display_list_items(self):
        return "I can't do that yet..."
