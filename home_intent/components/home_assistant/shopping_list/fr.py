from .base_shopping_list import BaseShoppingList, intents


class ShoppingList(BaseShoppingList):
    @intents.sentences(["ajouter ($shopping_list_item) à la liste [de course]"])
    def add_item_to_shopping_list(self, shopping_list_item):
        self._add_item_to_shopping_list(shopping_list_item)
        return f"Ajout de {shopping_list_item} dans votre liste de course"

    @intents.sentences(
        ["(cocher | remettre) ($shopping_list_item) dans la liste [de course]",]
    )
    def mark_item_complete_on_shopping_list(self, shopping_list_item):
        self._mark_item_complete_on_shopping_list(shopping_list_item)
        return f"cocher {shopping_list_item} dans votre liste de course"

    @intents.sentences(
        ["(décocher | enlever) ($shopping_list_item) dans la liste [de course]",]
    )
    def unmark_item_complete_on_shopping_list(self, shopping_list_item):
        self._unmark_item_complete_on_shopping_list(shopping_list_item)
        return f"décocher {shopping_list_item} dans votre liste de courset"

    @intents.default_disable("Causes system confustion")
    @intents.sentences(
        ["Tout (cocher | enlever) dans la liste [de course]",]
    )
    def mark_everything_complete_on_shopping_list(self):
        self._mark_everything_complete_on_shopping_list()
        return "Tout enelver dans la liste de course"

    @intents.default_disable("Causes system confustion")
    @intents.sentences(
        ["Tout (décocher | remettre) dans la liste [de course]",]
    )
    def unmark_everything_complete_on_shopping_list(self):
        self._unmark_everything_complete_on_shopping_list()
        return "Tout remettre dans la liste de course"

    @intents.default_disable("Doesn't actually work...")
    # Not entirely sure how to get the items from the shopping list via the API.
    # Will have to do some discovery around it.
    @intents.sentences(["[Dis moi] qu'est ce qu'il y a dans la liste [de course]"])
    def display_list_items(self):
        return "Je ne peux pour l'instant pas te le dire"
