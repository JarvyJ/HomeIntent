from .sample_light import intents, SampleLight


def test_registered_slots():
    assert len(intents.all_slots) == 2


def test_registered_sentences():
    assert len(intents.all_sentences) == 5


def test_disabled_sentences():
    print(intents.all_sentences)
    assert len({k: v for (k, v) in intents.all_sentences.items() if v.disabled is True}) == 2
