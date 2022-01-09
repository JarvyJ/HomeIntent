from .base_shopping_list import BaseShoppingList, intents


class ShoppingList(BaseShoppingList):
    a = "(schreibe | packe | setze)"
    b = "(streiche | entferne)"
    c = "(dem Einkaufszettel | der Einkaufsliste)"

    @intents.sentences([f"{a} ($shopping_list_item) auf (den Einkaufszettel | die Einkaufsliste)"])
    def add_item_to_shopping_list(self, shopping_list_item):
        self._add_item_to_shopping_list(shopping_list_item)
        return f"{shopping_list_item} dem Einkaufszettel hinzugefügt."

    @intents.sentences(
        ["Hake ($shopping_list_item) (vom Einkaufszettel | von der Einkaufsliste) ab", f"{b} ($shopping_list_item) (vom Einkaufszettel | von der Einkaufsliste)"]
    )
    def mark_item_complete_on_shopping_list(self, shopping_list_item):
        self._mark_item_complete_on_shopping_list(shopping_list_item)
        return f"{shopping_list_item} auf dem Einkaufszettel abgehakt"

    @intents.sentences(
        [f"{a} ($shopping_list_item) wieder auf (den Einkaufszettel | die Einkaufsliste)",]
    )
    def unmark_item_complete_on_shopping_list(self, shopping_list_item):
        self._unmark_item_complete_on_shopping_list(shopping_list_item)
        return f"{shopping_list_item} wieder auf den Einkaufszettel gesetzt"

    @intents.default_disable("Causes system confustion")
    @intents.sentences(
        [f"Hake alles auf {c} ab", f"Streiche alles auf {c}"]
    )
    def mark_everything_complete_on_shopping_list(self):
        self._mark_everything_complete_on_shopping_list()
        return "Einkaufszettel komplett abgehakt"

    @intents.default_disable("Causes system confustion")
    @intents.sentences(
        ["Setze alles wieder auf (den Einkaufszettel | die Einkaufsliste)",]
    )
    def unmark_everything_complete_on_shopping_list(self):
        self._unmark_everything_complete_on_shopping_list()
        return "Alles wieder auf (den Einkaufszettel | die Einkaufsliste) gesetzt"

    @intents.default_disable("Doesn't actually work...")
    # Not entirely sure how to get the items from the shopping list via the API.
    # Will have to do some discovery around it.
    @intents.sentences(["Sag mir, was auf (dem Einkaufszettel | der Einkaufsliste) steht", "Was steht auf (dem Einkaufszettel | der Einkaufsliste)?"])
    def display_list_items(self):
        return "I can't do that yet..."

    @intents.sentences(["(Lösche | Entferne) die abgehakten Sachen von (der Einkaufsliste | dem Einkaufszettel)"])
    def _delete_marked_items_from_shopping_list(self):
        return "Abgehakte Sachen wurden vom Einkaufszettel entfernt"