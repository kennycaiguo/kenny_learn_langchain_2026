

def create_qwen3_instance():
    from langchain_openai import ChatOpenAI
    # 创建模型实例
    model = ChatOpenAI(
        model="qwen3-vl:latest",
        api_key="sk12345",
        base_url="http://localhost:11434/v1",
        temperature=0.1
    )    

    return model

def create_gemma4_instance():
    from langchain_openai import ChatOpenAI
    # 创建模型实例
    model = ChatOpenAI(
        model="gemma4:latest",
        api_key="ollama",
        base_url="http://localhost:11434/v1",
        temperature=0.1
    )    

    return model