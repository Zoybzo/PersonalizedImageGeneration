from config.configurator import Config

# config_file_list = ["props/overall.yaml"]
gpt_config = Config(config_file_list=["props/gpt.yaml", "props/overall.yaml"])
prompt_config = Config(config_file_list=["props/prompt.yaml", "props/overall.yaml"])
server_config = Config(config_file_list=["props/server.yaml", "props/overall.yaml"])
txt2img_config = Config(config_file_list=["props/txt2img.yaml", "props/overall.yaml"])
