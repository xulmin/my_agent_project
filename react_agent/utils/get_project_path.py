import os


# 获取工程所在的目录
def get_project_path():
    """
    获取工程所在的目录
    :return:
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_abs_path(path):
    """
    获取绝对路径
    :param path: 相对路径
    :return:
    """
    return os.path.join(get_project_path(), path)


if __name__ == '__main__':
    print(get_abs_path("config\prompts.yml"))
