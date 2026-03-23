from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.messages import SystemMessage
from langchain.tools import tool
from langchain.agents import create_agent


from dotenv import load_dotenv
from keys import get_api_key
import json
import yfinance as yf
import warnings
import urllib3
import os
import ssl


load_dotenv()




def demosimple1():
    """Function for demonstrating use of Langchain to combine prompt,LLM call to get the desired output"""

    # user-question
    question = "which is the most popular game in india"

    # Create a prompt template with a embedded variable
    template = """Question: {question}
    
    Answer: """

    prompt = PromptTemplate(template=template, input_variables=["question"])

    # Create the language model object
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=get_api_key())

    # Invoke the LLM Chain
    chain = prompt | llm

    response = chain.invoke({"question": question})
    print(response.content)


def demosimple2():
    """Function for demonstrating use of Langchain expression language to combine prompt,LLM call to get the desired output"""

    prompt = PromptTemplate.from_template(
        """Act as a senior good teacher. I am fifth grader trying to know what recent trends are. explain me what {topic} is. do not include technical jargon"""
    )

    # Create the language model object
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=get_api_key())

    chain = prompt | llm  # Langchain expression language

    response = chain.invoke({"topic": "Model Agnostic"})
    print(response.content)


def demosimple3():
    """Function for demonstrating use of prompt template format  to get the desired output"""

    prompt = PromptTemplate.from_template(
        """Act as a senior good teacher. I am fifth grader trying to know what recent trends are. explain me what {topic} is. do not include technical jargon"""
    )

    prompt = prompt.format(topic="Cosine Similiarity")

    # Create the language model object
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", google_api_key=get_api_key(), temperature=2
    )

    response = llm.invoke(prompt)
    print(response.content)


def demosimple4():
    """Function for demonstrating use of chat prompt template to get the desired output"""

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Your name is {name} and act as a senior good teacher. I am fifth grader trying to know what recent trends are. do not include technical jargon",
            ),
            ("human", "Hello, how are you doing?"),
            ("ai", "I am doing well, thanks!"),
            ("human", "{user_input}"),
        ]
    )
    prompt = prompt.format_messages(
        name="Riyaz", user_input="Introduce you and explain me what is tesseract!"
    )

    # Create the language model object
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=get_api_key())

    response = llm.invoke(prompt)
    print(response.content)


def demosimple5():
    """Function for demonstrating use of system message, HumanPrompt template to get the desired output"""

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="Act as a senior good teacher. I am fifth grader trying to know what recent trends are. do not include technical jargon"
            ),
            HumanMessagePromptTemplate.from_template(
                "Your name is {name} and {user_input}"
            ),
        ]
    )
    prompt = prompt.format_messages(
        name="Riyaz", user_input="Introduce you and explain me what is epstein files!"
    )

    # Create the language model object
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=get_api_key())

    response = llm.invoke(prompt)
    print(response.content)

def demo_langchain_agents_tools():
    """Function for demonstrating use of Langchain agents and tools"""
    
    @tool(description="Evaluate a mathematical expression.")
    def calculator(expression: str) -> str:
        print(expression)
        return str(eval(expression))
    

    # Create the language model object
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=get_api_key(),temperature=0)

    agent = create_agent(
    tools=[calculator],
    model=llm,
    system_prompt="You are a helpful assistant",
)
    #result=agent.invoke({"messages": [{"role": "user", "content": "What is 25 * 17?"}]})
    result=agent.invoke({"messages": [{"role": "user", "content": "You are building a house. there are two bedrooms of 5 metres by 5 metres each and drawing cum open kitchen is 7 metres by 6 metres and balcony of 3 metres by 2 metres. what is the total area of the house?"}]})
    print(result["messages"][-1].content)

    for msg in result["messages"]:
        # Tool calls are stored here
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            print("Tool was called:", msg.tool_calls)

def demo_langchain_agents_multiple_tools():
    """Function for demonstrating use of Langchain agents and multiple tools"""

    # ---- OPTIONAL: disable SSL (only if needed in your env) ----
    ssl._create_default_https_context = ssl._create_unverified_context
    os.environ["CURL_CA_BUNDLE"] = ""
    os.environ["SSL_CERT_FILE"] = ""
    os.environ["REQUESTS_CA_BUNDLE"] = ""
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")

    

    @tool
    def search_tool(query: str) -> str:
        """Get Microsoft stock price (USD) and USD/INR exchange rate."""
        print("search_tool called")

        msft = yf.Ticker("MSFT")
        usd_inr = yf.Ticker("USDINR=X")

        msft_usd = msft.fast_info.get("lastPrice")
        fx_rate = usd_inr.fast_info.get("lastPrice")

        if msft_usd is None or fx_rate is None:
            raise ValueError("Failed to fetch market data")

        return json.dumps({
            "msft_usd": float(msft_usd),
            "usd_inr": float(fx_rate)
        })

    @tool
    def calculator(expression: str) -> str:
        """Evaluate arithmetic expression safely."""
        print("calculator called with:", expression)

        allowed = set("0123456789+-*/(). ")
        if not set(expression) <= allowed:
            raise ValueError("Unsafe expression")

        return str(eval(expression, {"__builtins__": {}}, {}))

    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=get_api_key(),
        temperature=0,
    )

    agent = create_agent(
        model=model,
        tools=[search_tool, calculator],
        system_prompt=(
            "You are a finance assistant. "
            "For Microsoft stock price requests, first call search_tool. "
            "Then call calculator to convert the USD stock price to INR using the USD/INR rate. "
            "Return both USD and INR and mention the Google Finance pages used."
        ),
    )

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Find Microsoft stock on Google Finance and show the price in USD "
                        "and INR using the calculator tool."
                    ),
                }
            ]
        }
    )

    print("\nFinal Answer:")
    print(result["messages"][-1].content)

    print("\nTool Calls:")
    for msg in result["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            print("Tool was called:", msg.tool_calls)

    ssl._create_default_https_context=ssl._create_default_https_context
     

def main():
    # print(demosimple1.__doc__)
    # demosimple1()

    # print(demosimple2.__doc__)
    # demosimple2()

    # print(demosimple3.__doc__)
    # demosimple3()

    # print(demosimple4.__doc__)
    # demosimple4()

    #print(demosimple5.__doc__)
    #demosimple5()

    #print(demo_langchain_agents_tools.__doc__)
    #demo_langchain_agents_tools()

    print(demo_langchain_agents_multiple_tools.__doc__)
    demo_langchain_agents_multiple_tools()


if __name__ == "__main__":
    main()
