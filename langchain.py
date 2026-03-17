from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
from keys import get_api_key

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


def main():
    # print(demosimple1.__doc__)
    # demosimple1()

    # print(demosimple2.__doc__)
    # demosimple2()

    # print(demosimple3.__doc__)
    # demosimple3()

    # print(demosimple4.__doc__)
    # demosimple4()

    print(demosimple5.__doc__)
    demosimple5()


if __name__ == "__main__":
    main()
