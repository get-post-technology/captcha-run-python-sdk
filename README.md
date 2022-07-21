<div align="center">

<h1>CaptchaRun Python SDK</h1>

<p>
<a href="https://github.com/get-post-technology/captcha-run-python-sdk/actions?query=workflow%3ACI">
<img src="https://github.com/get-post-technology/captcha-run-python-sdk/workflows/CI/badge.svg" alt="Github Action Test" />
</a>

<a href="https://app.codecov.io/gh/get-post-technology/captcha-run-python-sdk">
<img alt="Codecov" src="https://codecov.io/gh/get-post-technology/captcha-run-python-sdk/branch/main/graph/badge.svg?token=NUIJJ4BK8H">
</a>
</p>

<a href="https://pypi.org/project/captcharun/">
<img src="https://img.shields.io/pypi/v/captcharun" alt="PyPI" />
</a>

</p>

<a href="https://captcha.run">CapthcaRun</a> 官方 Python 客户端

</div>

---

# 例子

## 查询余额
```python
from captcharun import Client, GetBalance, CreateTask
client = Client("你的 TOKEN")
result = client.invoke(GetBalance())

print(result)
# {'cumulativeRecharge': '1100', 'share': '0.0960', 'balance': '103.508', 'credit': '0', 'cumulativeShare': '0.0960'}

```

## 创建任务 & 获取状态
```python
from captcharun import Client, GetBalance, GetTask, CreateTask
from captcharun.task import ReCaptchaV2Task

client = Client("你的 TOKEN")

# 创建任务
result = client.invoke(
    CreateTask(
        ReCaptchaV2Task(
            "SITE KEY",
            "SITE REFERER",
        ),
        developer="开发者 ID"
    ),
)
print(result) 
# {'taskId': '492ca979-7559-4012-ac31-3134b9ce63f8'}

# 获取任务状态 (异步返回)
result = client.invoke(GetTask(result['taskId']))
print(result)

```


## 完整创建任务 + 等待 + 重试例子
```python
import time
from captcharun import Client, GetTask, CreateTask
from captcharun.task import ReCaptchaV2Task


# 你可以手动指定 token
# client = Client("xxxxxxxxxxxxxxxxxxx")
# 不然会自动从环境变量 CAPTCHARUN_TOKEN 获取 
client = Client()


# 简单获取 token
def get_token(timeout = 180):
    result = client.invoke(
        CreateTask(
            ReCaptchaV2Task(
                "xxxxxxxxxxxxxxxxxxx",
                "https://example.com",
            ),
            developer="开发者 ID"
        ),
    )

    task_id = result.get("taskId")
    if task_id is None:
        print("创建任务失败")
        return
    
    start_time = time.time()
    result = client.invoke(GetTask(task_id))

    while result["status"] == "Working" and time.time() - start_time < timeout:
        time.sleep(3)
        result = client.invoke(GetTask(task_id))
    
    return result['response']['gRecaptchaResponse']


# 失败自动重试
def get_token_with_retry(retry_times=3, timeout=180):
    for _ in range(retry_times):
        try:
            token = get_token(timeout)
            if token is not None:
                return token
        except Exception as e:
            print(e)

    return None


if __name__ == '__main__':
    print(get_token_with_retry())
```
