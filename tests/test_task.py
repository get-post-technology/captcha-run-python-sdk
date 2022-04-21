import pytest

from captcharun.task import *


def test_construct_ReCaptchaV2_task():
    task = ReCaptchaV2Task("a", "b", False, True)

    assert task.data == {
        "captchaType": "ReCaptchaV2",
        "siteKey": "a",
        "siteReferer": "b",
        "useCache": False,
        "isInvisible": True,
    }


def test_construct_ReCaptchaV3_task():
    task = ReCaptchaV3Task("a", "b", "c")

    assert task.data == {
        "captchaType": "ReCaptchaV3",
        "siteKey": "a",
        "siteReferer": "b",
        "siteAction": "c",
    }


def test_construct_ReCaptchaV2Classification_task():
    with pytest.raises(AssertionError):
        ReCaptchaV2ClassificationTask("a", "b")
    with pytest.raises(AssertionError):
        ReCaptchaV2ClassificationTask("a", "/m/b", 2)

    task = ReCaptchaV2ClassificationTask("a", "/m/b")
    assert task.data == {
        "captchaType": "ReCaptchaV2Classification",
        "image": "a",
        "question": "/m/b",
        "resize": 0,
    }

    task0 = ReCaptchaV2ClassificationTask(b"a", "/m/b")
    assert task0.data == {**task.data, "image": "YQ=="}


def test_construct_HCaptcha_task():
    task = HCaptchaTask("a", "b", False)

    assert task.data == {
        "captchaType": "HCaptcha",
        "siteKey": "a",
        "siteReferer": "b",
        "useCache": False,
    }


def test_construct_HCaptchaClassification_task():
    task = HCaptchaClassificationTask("test", [], [])

    assert task.data == {
        "captchaType": "HCaptchaClassification",
        "question": "test",
        "queries": [],
        "anchors": [],
    }


def test_construct_TextCaptcha_task():
    task = TextCaptchaTask("test")

    assert task.data == {
        "captchaType": "TextCaptcha",
        "image": "test",
    }
