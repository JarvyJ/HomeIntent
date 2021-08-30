import pytest
from pathlib import PosixPath


@pytest.fixture
def colors():
    from .sample_light import intents, SampleLight

    # load up the light/customization
    sample_light = SampleLight()
    intents.handle_customization(
        PosixPath("./tests/various_slot_customizations.yaml"), sample_light
    )

    return sample_light.color()


@pytest.fixture
def lights():
    from .sample_light import intents, SampleLight

    sample_light = SampleLight()
    intents.handle_customization(
        PosixPath("./tests/various_slot_customizations.yaml"), sample_light
    )

    return sample_light.light()


@pytest.fixture
def intents():
    from .sample_light import intents, SampleLight

    sample_light = SampleLight()
    intents.handle_customization(
        PosixPath("./tests/various_slot_customizations.yaml"), sample_light
    )

    return intents


@pytest.fixture
def no_intents():
    from .sample_light import intents, SampleLight

    sample_light = SampleLight()
    intents.handle_customization(PosixPath("./tests/disable_all.yaml"), sample_light)

    return intents


def test_slot(lights):
    assert "kitchen{light}" in lights
    assert "attic{light}" in lights


def test_slot_addition(lights):
    assert "bathroom{light}" in lights
    assert "laundry{light:basement}" in lights


def test_slot_removal(lights):
    assert "bedroom{light}" not in lights


def test_dictionary_slot(colors):
    assert "yellow{color:yellow}" in colors
    assert "red{color:red}" in colors


def test_dictionary_slot_addition(colors):
    assert "green{color}" in colors
    assert "lime green{color:limegreen}" in colors


def test_dictionary_slot_removal(colors):
    assert "blue{color:blue}" not in colors
    assert "light blue{color:blue}" not in colors


def test_registered_sentences(intents):
    assert len(intents.all_sentences) == 5
    assert len({k: v for (k, v) in intents.all_sentences.items() if v.disabled is True}) == 0


def test_disable_all(no_intents):
    assert len(no_intents.all_sentences) == 0
    assert len({k: v for (k, v) in no_intents.all_sentences.items() if v.disabled is True}) == 0
