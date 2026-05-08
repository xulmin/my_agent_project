from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from modle.factory import chart_model
from rag.vector_store import VectorStoreService
from utils.prompt_loader import load_rag_prompt

def print_prompt(prompt):
    """
    打印参数
    :param prompt:
    :return:
    """
    print("=" * 50)
    print(prompt.to_string())
    print("=" * 50)
    return  prompt


class RagSummarizeService(object):
    """
    让模型根据参考资料总结
    """

    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompt()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chart_model
        self.chain = self.__init_chain()

    def __init_chain(self):
        return self.prompt_template | print_prompt | self.model | StrOutputParser()

    def retriever_doc(self, query: str):
        """
        检索
        :param query:
        :return:
        """
        docs = self.retriever.invoke(query)
        return docs

    def rag_summarize(self, query: str):
        """
        让模型根据参考资料总结
        :param query:
        :return:
        """
        docs = self.retriever_doc(query)
        context = ""
        counter = 0
        for doc in docs:
            counter += 1
            context += f"【参考资料{counter}】：参考资料内容：{doc.page_content}\n | 参考元数据：{doc.metadata}\n"

        return self.chain.invoke({"input": query, "context": context})


if __name__ == '__main__':
    rag_summarize = RagSummarizeService()
    print(rag_summarize.rag_summarize("小户型适合那些扫地机器人"))