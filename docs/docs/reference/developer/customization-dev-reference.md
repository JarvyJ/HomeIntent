# Customization (Dev Reference)

## Intent modifications (sentence addition/removal and aliasing)
Intent modifications will verify the intent names defined in the customization file are associated with the component during the `register` method.

Sentence additions/removals are then modified in the associated intent sentences. From there the normal handling of sentences occurs (so slot verification will still happen).

Aliases are setup as a custom method dynamically added to the class. They can technically support slots and partially filled values, but we'll see how that goes when I get to adding it in.

## Slot modifications
Similar to intent modifications, slot group names are verified during the `register` call and will raise an error if the slot group name is not in the associated component.

Slots themselves are modified later after being retrieved from the component. If there is a slot value for removal that isn't in the slot list of values, a `warning` is logged, but the program will continue to execute.