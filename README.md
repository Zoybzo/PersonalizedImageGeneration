# 用途
根据用户的文字描述, 针对不同的用户生成个性化的图片.

框架有两种生成方式: 
1. 通过输入用户的历史交互物品序列, 根据GPT等大语言模型生成用户的个性化描述,
然后与用户的文字描述结合, 生成个性化的图片.
2. 通过用户的文字描述与用户ID, 利用文生图模型与用户Embedding生成个性化的图片.

# 使用方法

框架提供两种使用方式:
1. API模式
2. 直接调用模式

模型使用`Python 3.8`版本, 在使用之前需要安装相关的依赖
```shell
pip install -r requirements.txt
```

为了避免`Module Not Found`问题, 可以在运行之前使用`export PYTHONPATH="${PYTHONPATH}:/path/to/your/project/"`.

## API模式
API模式下, 通过启动不同的服务器, 用户可以通过HTTP请求的方式调用生成图片的接口.
1. 启动GPT服务器
   ```shell
   python gpt/server.py
   ```
2. 启动Prompt服务器
    ```shell
    python prompt/server.py
    ```
3. 启动t2i服务器
    ```shell
    python txt2img/server.py
    ```
4. 启动主服务器
    ```shell
    python main.py
    ```
5. 启动前端
    ```shell
    python gradio_demo.py
    ```
6. 使用API模式生成图片

## 直接调用模式
直接调用模式下, 用户可以通过直接调用模型的方式生成图片. 服务器的启动方式与API模式相同.
1. 启动GPT服务器
2. 启动主服务器
3. 启动前端
4. 使用直接调用模式生成图片

# 可能的问题以及解决方法
1. 'Module Not Found' error.
   在运行之前使用`export PYTHONPATH="${PYTHONPATH}:/path/to/your/project/"`.
