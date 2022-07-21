# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['captcharun']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'captcharun',
    'version': '0.2.3',
    'description': 'CaptchaRun Official Python SDK',
    'long_description': '<div align="center">\n\n<h1>CaptchaRun Python SDK</h1>\n\n<p>\n<a href="https://github.com/get-post-technology/captcha-run-python-sdk/actions?query=workflow%3ACI">\n<img src="https://github.com/get-post-technology/captcha-run-python-sdk/workflows/CI/badge.svg" alt="Github Action Test" />\n</a>\n\n<a href="https://app.codecov.io/gh/get-post-technology/captcha-run-python-sdk">\n<img alt="Codecov" src="https://codecov.io/gh/get-post-technology/captcha-run-python-sdk/branch/main/graph/badge.svg?token=NUIJJ4BK8H">\n</a>\n</p>\n\n<a href="https://pypi.org/project/captcharun/">\n<img src="https://img.shields.io/pypi/v/captcharun" alt="PyPI" />\n</a>\n\n</p>\n\n<a href="https://captcha.run">CapthcaRun</a> 官方 Python 客户端\n\n</div>\n\n---\n\n# 例子\n\n## 查询余额\n```python\nfrom captcharun import Client, GetBalance, CreateTask\nclient = Client("你的 TOKEN")\nresult = client.invoke(GetBalance())\n\nprint(result)\n# {\'cumulativeRecharge\': \'1100\', \'share\': \'0.0960\', \'balance\': \'103.508\', \'credit\': \'0\', \'cumulativeShare\': \'0.0960\'}\n\n```\n\n## 创建任务 & 获取状态\n```python\nfrom captcharun import Client, GetBalance, GetTask, CreateTask\nfrom captcharun.task import ReCaptchaV2Task\n\nclient = Client("你的 TOKEN")\n\n# 创建任务\nresult = client.invoke(\n    CreateTask(\n        ReCaptchaV2Task(\n            "SITE KEY",\n            "SITE REFERER",\n        ),\n        developer="开发者 ID"\n    ),\n)\nprint(result) \n# {\'taskId\': \'492ca979-7559-4012-ac31-3134b9ce63f8\'}\n\n# 获取任务状态 (异步返回)\nresult = client.invoke(GetTask(result[\'taskId\']))\nprint(result)\n\n```\n\n\n## 完整创建任务 + 等待 + 重试例子\n```python\nimport time\nfrom captcharun import Client, GetTask, CreateTask\nfrom captcharun.task import ReCaptchaV2Task\n\n\n# 你可以手动指定 token\n# client = Client("xxxxxxxxxxxxxxxxxxx")\n# 不然会自动从环境变量 CAPTCHARUN_TOKEN 获取 \nclient = Client()\n\n\n# 简单获取 token\ndef get_token(timeout = 180):\n    result = client.invoke(\n        CreateTask(\n            ReCaptchaV2Task(\n                "xxxxxxxxxxxxxxxxxxx",\n                "https://example.com",\n            ),\n            developer="开发者 ID"\n        ),\n    )\n\n    task_id = result.get("taskId")\n    if task_id is None:\n        print("创建任务失败")\n        return\n    \n    start_time = time.time()\n    result = client.invoke(GetTask(task_id))\n\n    while result["status"] == "Working" and time.time() - start_time < timeout:\n        time.sleep(3)\n        result = client.invoke(GetTask(task_id))\n    \n    return result[\'response\'][\'gRecaptchaResponse\']\n\n\n# 失败自动重试\ndef get_token_with_retry(retry_times=3, timeout=180):\n    for _ in range(retry_times):\n        try:\n            token = get_token(timeout)\n            if token is not None:\n                return token\n        except Exception as e:\n            print(e)\n\n    return None\n\n\nif __name__ == \'__main__\':\n    print(get_token_with_retry())\n```\n',
    'author': 'CaptchaRun',
    'author_email': 'admin@captcha.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://captcha.run',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

