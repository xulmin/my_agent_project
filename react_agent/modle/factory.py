from abc import ABC, abstractmethod
from typing import Optional, Union

from langchain_community.chat_models.tongyi import BaseChatModel
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.embeddings import Embeddings

from utils.config_handler import rag_config


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
        return ChatTongyi(model=rag_config["chat_model_name"])


class EmbeddingModelFactory(BaseModelFactory):
    """
    嵌入工厂类
    """

    def create_model(self) -> Optional[Union[Embeddings, BaseChatModel]]:
        return DashScopeEmbeddings(model=rag_config["embedding_model_name"])



chart_model = ChatModelFactory().create_model()
embedding_model = EmbeddingModelFactory().create_model()

