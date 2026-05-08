from utils.config_handler import prompts_config
from utils.logger_handler import logger
from utils.get_project_path import get_abs_path


def load_system_prompt() -> str:
    """
    加载系统提示词
    :return:
    """
    try:
        prompt_path = get_abs_path(prompts_config["main_prompt_path"])
        with open(prompt_path, encoding='utf-8') as f:
            return f.read()
    except KeyError as key_error:
        logger.error(f'[load_system_prompt]在yml文件配置中没有main_prompt_path配置项')
        raise key_error
    except Exception as e:
        logger.error(f'[load_system_prompt]加载系统提示错误: {e}')
        raise  e


def load_rag_prompt() -> str:
    """
    加载系统提示词
    :return:
    """
    try:
        rag_prompt = get_abs_path(prompts_config["rag_summerize_prompt_path"])
        with open(rag_prompt, encoding='utf-8') as f:
            return f.read()
    except KeyError as key_error:
        logger.error(f'[load_rag_prompt]在yml文件配置中没有rag_summerize_prompt_path配置项')
        raise key_error
    except Exception as e:
        logger.error(f'[load_rag_prompt]加载系统提示错误: {e}')
        raise  e


def load_report_prompt() -> str:
    """
    加载系统提示词
    :return:
    """
    try:
        report_path = get_abs_path(prompts_config["report_prompt_path"])
        with open(report_path, encoding='utf-8') as f:
            return f.read()
    except KeyError as key_error:
        logger.error(f'[load_report_prompt]在yml文件配置中没有report_prompt_path配置项')
        raise key_error
    except Exception as e:
        logger.error(f'[load_report_prompt]加载系统提示错误: {e}')
        raise  e


if __name__ == '__main__':
    print(load_system_prompt())
    print(load_rag_prompt())
    print(load_report_prompt())