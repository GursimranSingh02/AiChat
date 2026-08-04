from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "You are a helpful, context-aware chat assistant.\n"
                "Use the conversation history when it is relevant.\n"
                "If the user asks a follow-up, resolve it using prior messages.\n"
                "Keep answers clear and concise unless the user asks for detail.\n"
                "If the request is ambiguous, ask a focused clarifying question."
            ),
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)
