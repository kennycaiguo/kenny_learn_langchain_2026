from langchain_core.prompts import ChatPromptTemplate

class ReusablePromptTemplate:
    """可复用提示模板"""
    TRANSLATOR = ChatPromptTemplate([
        ("system","你是专业翻译，精通{src_lang}和{target_lang}"),
        ("user","翻译一下文本\n{text}"),
    ])
    CODE_REVIEWER = ChatPromptTemplate([
        ("system","你是{language}代码审查专家，重点关注{focus}"),
        ("human","审查代码：\n'''{language}\n{code}\n'''"),
    ])
    SUMMARIZOR = ChatPromptTemplate([
        ("system","你是内容摘要专家"),
        ("user","将以下内容总结为{n}个要点{content}"),
    ])
    TUTOR = ChatPromptTemplate([
        ("system","你是{subject}导师，学生水平{level}"),
        ("user","{question}"),
    ])
