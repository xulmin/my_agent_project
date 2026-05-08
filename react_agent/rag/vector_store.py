import hashlib
import os

from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from modle.factory import embedding_model
from utils.config_handler import chroma_config
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_types
from utils.get_project_path import get_abs_path
from utils.logger_handler import logger


class VectorStoreService:
    """
    向量数据库
    """

    def __init__(self):
        # 初始化向量数据库
        self.vector_store = Chroma(
            collection_name=chroma_config["collection_name"],
            embedding_function=embedding_model,
            persist_directory=chroma_config["persist_directory"]
        )
        # 初始化分词器
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_config["chunk_size"],
            chunk_overlap=chroma_config["chunk_overlap"],
            separators=chroma_config["separators"],
            length_function=len
        )

    def get_retriever(self):
        """
        获取向量数据库的检索器
        :return:
        """
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_config["k"]})


def load_documents(self):
    """
     加载文档
    :param self:
    :return:
    """
    global documents

    def check_md5(md5_str):
        """
        校验md5
        :param md5_str:
        :return:
        """
        if not os.path.exists(get_abs_path(chroma_config["md5_path"])):
            # 不存在则创建
            open(get_abs_path(chroma_config["md5_path"]), 'w', encoding='utf-8').close()
            return False
        else:
            for line in open(get_abs_path(chroma_config["md5_path"]), encoding='utf-8').readlines():
                line = line.strip()
                if line == md5_str:
                    return True

            return False

    # 保存md5
    def save_md5(md5_str):
        """
        #保存md5
        :param md5_str:
        :return:
        """
        with open(get_abs_path(chroma_config["md5_path"]), 'a', encoding='utf-8') as f:
            f.write(md5_str + '\n')

        print("保存md5,保存成功")

    # 获取md5
    def get_md5(input_str, encoding='utf-8'):
        """
        获取md5
        :param input_str:
        :param encoding:
        :return:
        """
        # 将字符串转换字节数组
        bytes_data = input_str.encode(encoding)
        # 计算md5
        md5 = hashlib.md5()
        md5.update(bytes_data)
        return md5.hexdigest()

    def get_file_documents(file_path):
        """
         获取文档
        :param file_path:
        :return:
        """
        if file_path.endswith(".pdf"):
            return pdf_loader(file_path, chroma_config["pdf_password"])

        if file_path.endswith(".txt"):
            return txt_loader(file_path)

        return []

    file_list = listdir_with_allowed_types(chroma_config["data_path"],
                                           tuple(chroma_config["allow_knowledge_file_type"]))

    for file_path in file_list:
        try:
            md5_str = get_md5(file_path)
            if check_md5(md5_str):
                logger.info(f'[load_documents]文件已存在: {file_path}')
                continue
            documents = get_file_documents(file_path)
            if not documents:
                logger.info(f'[load_documents]文件不存在: {file_path}')
                continue

            spliter_documents = self.spliter.split_documents(documents)
            if not spliter_documents:
                logger.info(f'[load_documents]文件不存在: {file_path}')
                continue

            self.vector_store.add_documents(spliter_documents)
            save_md5(md5_str)
            logger.info(f'[load_documents]文件保存成功: {file_path}')

        except Exception as e:
            logger.error(f'[load_documents]文件保存失败: {file_path}, {e}')
