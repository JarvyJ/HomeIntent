import pytest
from home_intent.intents import IntentException


def test_broken_arg_fails():
    with pytest.raises(IntentException) as exception:
        from .sample_light_broken_arg import SampleLight, intents


def test_broken_sentence_fails():
    with pytest.raises(IntentException) as exception:
        from .sample_light_broken_sentence import SampleLight, intents


# def test_broken_sentence_fails2():
#     with pytest.raises(IntentException) as exception:
#         from .sample_light_broken_sentence2 import SampleLight, intents
