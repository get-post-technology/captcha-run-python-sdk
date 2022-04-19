from uuid import uuid4

import pytest
from httpx import HTTPStatusError

from captcharun import Client, GetBalance, GetTask
from captcharun.request import CreateTask
from captcharun.task import ReCaptchaV2Task

client = Client()


def check_balance_response(result):
    assert "_id" in result
    assert "share" in result
    assert "balance" in result
    assert "credit" in result
    assert "cumulativeShare" in result
    assert "cumulativeRecharge" in result

    assert type(result["balance"]) is str


def test_get_balance_sync():
    result = client.invoke(GetBalance())
    check_balance_response(result)


def test_get_balance_not_exists():
    with pytest.raises(HTTPStatusError) as excinfo:
        client.invoke(GetBalance(str(uuid4())))

    resp = excinfo.value.response
    json = resp.json()

    assert json["statusCode"] == resp.status_code == 401


@pytest.mark.asyncio
async def test_get_balance_async():
    result = await client.invoke_async(GetBalance())
    check_balance_response(result)

    async_client = Client(use_async=True)
    result = await async_client.invoke(GetBalance())
    check_balance_response(result)


def test_get_task_not_exists():
    with pytest.raises(HTTPStatusError) as excinfo:
        client.invoke(GetTask(str(uuid4())))

    resp = excinfo.value.response
    json = resp.json()

    assert json["statusCode"] == resp.status_code == 404


def test_task_pipeline():
    developer = "b9056f79-bfcf-42d7-8d85-bd2b1b1c9876"
    task = ReCaptchaV2Task(
        "6LfW6wATAAAAAHLqO2pb8bDBahxlMxNdo9g947u9",
        "https://recaptcha-demo.appspot.com/recaptcha-v2-checkbox.php",
    )

    result = client.invoke(
        CreateTask(
            task,
            developer,
        ),
    )

    assert "taskId" in result
    task_id = result["taskId"]

    result = client.invoke(GetTask(task_id))

    assert result["_id"] == task_id
    assert result["developer"] == developer
    assert task.data.items() <= result["request"].items()
