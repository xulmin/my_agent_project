import yaml

from utils.get_project_path import get_abs_path


def get_rag_config(config_path: str = get_abs_path('config/rag.yml'), encoding='utf-8'):
    """
    获取rag配置
    :return:
    """
    with open(config_path, encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def get_chroma_config(config_path: str = get_abs_path('config/chroma.yml'), encoding='utf-8'):
    """
    获取chroma配置
    :return:
    """
    with open(config_path, encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def get_prompts_config(config_path: str = get_abs_path('config/prompts.yml'), encoding='utf-8'):
    """
    获取prompts配置
    :return:
    """
    with open(config_path, encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def get_agent_config(config_path: str = get_abs_path('config/agent.yml'), encoding='utf-8'):
    """
    获取agent配置
    :return:
    """
    with open(config_path, encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


rag_config = get_rag_config()
chroma_config = get_chroma_config()
prompts_config = get_prompts_config()
agent_config = get_agent_config()
