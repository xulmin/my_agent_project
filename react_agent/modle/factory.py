import os
from abc import ABC, abstractmethod
from typing import Optional, Union

from dotenv import load_dotenv
from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_openai import ChatOpenAI

from utils.config_handler import rag_config

# 加载环境变量
load_dotenv()


class BaseModelFactory(ABC):
    """
    模型工厂抽象类
    """

    @abstractmethod
    def create_model(self) -> Optional[Union[Embeddings, BaseChatModel]]:
        """
        生成器
        """


class ChatModelFactory(BaseModelFactory):
    """
    聊天工厂类
    """

    def create_model(self) -> Optional[Union[Embeddings, BaseChatModel]]:
        return ChatOpenAI(
            model=rag_config["chat_model_name"],
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url=os.getenv("ALI_BASE_URL"),
            temperature=0.7
        )


class EmbeddingModelFactory(BaseModelFactory):
    """
    嵌入工厂类
    """

    def create_model(self) -> Optional[Union[Embeddings, BaseChatModel]]:
        return DashScopeEmbeddings(
            model=rag_config["embedding_model_name"],
            dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
        )


chart_model = ChatModelFactory().create_model()
embedding_model = EmbeddingModelFactory().create_model()
