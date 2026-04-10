from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

from langchain_ollama import OllamaLLM

# llm = OllamaLLM(model="llama3.1")
llm = OllamaLLM(model="deepseek-r1")

# llm = OllamaLLM(model="ministral-3")
# file_path = "chat_history.txt"

# chat_history = []
# chat_log = FileChatMessageHistory(file_path)

chat_log = ChatMessageHistory()

# To clear the history in the file
# chat_history.clear()

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI named John, answer what you been asked.",
            # "You are an AI named Mike, you answer questions with simple answers and no funny stuff.",
        ),
        # MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

chain = prompt_template | llm


def start_app():
    
    counter = 0
    round = 0

    while True:
        question = input("You: ")
        if question == "done":
            loaded_messages = chat_log.messages
            if len(loaded_messages) == 0:
                print("Nothing to write.")
                return
            
            file_path_output = "chat_history_output" + "_" + str(round) + ".txt"
            
            with open(file_path_output, "w", encoding="utf-8") as f:
                for line in loaded_messages:
                    f.write(f"{line.type.capitalize()}: {line.content}" + "\n")
            
            f.close()
            chat_log.clear()

            return
        
        # response = chain.invoke({"input": question, "chat_history": chat_history})
        response = chain.invoke({"input": question})
        # chat_history.append(HumanMessage(content=question))
        # chat_history.append(AIMessage(content=response))
        chat_log.add_user_message(message=HumanMessage(content=question))
        chat_log.add_ai_message(message=AIMessage(content=response))

        print("AI:" + response)
        counter += 1

        if counter == 10:
            file_path_output = "chat_history_output" + "_" + str(round) + ".txt"
            loaded_messages = chat_log.messages
            with open(file_path_output, "w", encoding="utf-8") as f:
                for line in loaded_messages:
                    f.write(f"{line.type.capitalize()}: {line.content}" + "\n")
            f.close()
            # chat_history.clear()
            chat_log.clear()
            counter = 0
            round += 1
    
 
    # loaded_messages = chat_log.messages
    
    # print(f"Loaded messages from '{file_path}':")
    
    # for message in loaded_messages:
    #     print(f"{message.type.capitalize()}: {message.content}")

    # file_path_output = "chat_history_output" + "_" + str(round) + ".txt"
    # with open(file_path_output, "w", encoding="utf-8") as f:
    #     for line in loaded_messages:
    #         f.write(f"{line.type.capitalize()}: {line.content}" + "\n")

    # print(f"Chat history saved to {file_path}")

if __name__ == "__main__":
    start_app()

#     ########################
#     from langchain_community.chat_message_histories import FileChatMessageHistory
# from langchain_core.messages import HumanMessage, AIMessage

# # Initialize FileChatMessageHistory with the path to your text file
# file_path = "chat_history.txt"
# chat_history = FileChatMessageHistory(file_path)

# # Add messages to the history
# chat_history.add_user_message("Hello, how are you?")
# chat_history.add_ai_message("I'm doing well, thank you for asking!")
# chat_history.add_user_message("Can you tell me more about LangChain?")

# # You can also add messages as a list
# messages_to_add = [
#     AIMessage(content="LangChain is a framework designed to simplify the creation of applications using large language models."),
#     HumanMessage(content="That's interesting! What are its main features?")
# ]
# chat_history.add_messages(messages_to_add)

# # The messages are automatically saved to the 'chat_history.txt' file as they are added.
# # You can retrieve the messages as a list of BaseMessage objects
# loaded_messages = chat_history.get_messages()

# print(f"Loaded messages from '{file_path}':")
# for message in loaded_messages:
#     print(f"{message.type.capitalize()}: {message.content}")

# # To clear the history in the file
# # chat_history.clear()