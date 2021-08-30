import pytest
from pathlib import PosixPath


@pytest.fixture
def intents():
    from .sample_light import intents, SampleLight

    sample_light = SampleLight()
    intents.handle_customization(
        PosixPath("./tests/various_sentence_customizations.yaml"), sample_light
    )

    return intents


def test_registered_sentences(intents):
    assert len(intents.all_sentences) == 5
    assert len({k: v for (k, v) in intents.all_sentences.items() if v.disabled is True}) == 2
    assert intents.all_sentences["toggle_light"].disabled == True
    assert intents.all_sentences["change_color_temperature"].disabled == False
