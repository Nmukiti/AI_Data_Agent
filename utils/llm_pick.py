from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

def pick_llm(level: str):
    """
    Picks the appropriate LLM (Language Model) based on the specified level.

    Args:
        level (str): The level of the LLM to pick. It can be "low", "medium", or "high".

    Returns:
        str: The name of the selected LLM.
    """
    if level.lower() == "low":
        llm = ChatOpenAI(model_name="gpt-5.6-luna", temperature=0, model_kwargs={"reasoning_effort": "none"})
    elif level.lower() == "medium":
        llm = ChatOpenAI(model_name="gpt-5.6-terra", temperature=0, model_kwargs={"reasoning_effort": "none"})
    elif level.lower() == "high":
        llm = ChatOpenAI(model_name="gpt-5.6-sol", temperature=0, model_kwargs={"reasoning_effort": "none"})
    else:
        raise ValueError(f"Unsupported level: {level}")

    return llm

if __name__ == "__main__":
    llm_obj = pick_llm("low")
    print(llm_obj.invoke("What is the capital of France?"))