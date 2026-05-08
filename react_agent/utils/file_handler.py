import hashlib
import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

from utils.logger_handler import logger


def get_file_md5(file_path):
    """
    获取文件的md5
    :param file_path: 文件路径
    :return:
    """
    if not os.path.exists(file_path):
        logger.error(f'[md5计算]文件不存在: {file_path}')
        return None

    if not os.path.isfile(file_path):
        logger.error(f'[md5计算]不是文件: {file_path}')
        return None
    md5 = hashlib.md5()
    chunk_size = 4096
    try:
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                md5.update(data)
            return md5.hexdigest()

    except Exception as e:
        logger.error(f'[md5计算]文件读取错误: {file_path}, {e}')
        return None


def listdir_with_allowed_types(path, allowed_types):
    """
    列出指定目录下的文件，并筛选出指定类型的文件
    :param path: 目录路径
    :param allowed_types: 允许的文件类型列表
    :return:
    """
    if not os.path.isdir(path):
        logger.error(f'[listdir_with_allowed_types]不是文件夹: {path}')
        return allowed_types

    # if not os.path.exists(path):
    #     logger.error(f'[listdir_with_allowed_types]目录不存在: {path}')
    #     return allowed_types

    file_list = []

    for file in os.listdir(path):
        if file.endswith(allowed_types):
            file_list.append(os.path.join(path, file))
            logger.info(f'[listdir_with_allowed_types]文件: {file}')

    return file_list


def pdf_loader(file_path, password) -> list[Document]:
    """
    pdf文件加载
    :param file_path:
    :param password:
    :return:
    """
    return PyPDFLoader(file_path, password).load()


def txt_loader(file_path) -> list[Document]:
    """
    txt文件加载
    :param file_path:
    :return:
    """
    return TextLoader(file_path).load()
