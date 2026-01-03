from langgraph.graph import END, MessageGraph, StateGraph
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from typing import List, Sequence, Annotated, TypedDict
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from IPython.display import Image, display
import openai

load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")
llm_modle = "gpt-3.5-turbo"

llm = ChatOpenAI(temperature=0.7, model=llm_modle)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a professional LinkedIn content writer for software engineers.

                Rules (MANDATORY):
                - Use the provided topic explicitly and concretely.
                - Do NOT use placeholders like [topic], [example], or brackets.
                - Do NOT use emojis or symbols.
                - Do NOT use hype phrases like “excited”, “thrilled”, “delighted”.
                - Do NOT include meta commentary or calls like “Let’s discuss”.
                - Output ONLY the final LinkedIn post text.
                - Keep a calm, technical, recruiter-friendly tone.
                - 2–3 short paragraphs max.
                - End with up to 5 relevant hashtags.
                CRITICAL RULES:
                - NEVER use placeholders such as [example], [specific topic], [mention X], or brackets of any kind.
                - If specific details are missing, make reasonable assumptions based on the topic.
                - Always produce a fully finalized post ready for publishing.

            """
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)



reflection_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a professional LinkedIn content strategist and thought leadership expert. Your task is to critically evaluate the given LinkedIn post and provide a comprehensive critique. Follow these guidelines:

        1. Assess the post’s overall quality, professionalism, and alignment with LinkedIn best practices.
        2. Evaluate the structure, tone, clarity, and readability of the post.
        3. Analyze the post’s potential for engagement (likes, comments, shares) and its effectiveness in building professional credibility.
        4. Consider the post’s relevance to the author’s industry, audience, or current trends.
        5. Examine the use of formatting (e.g., line breaks, bullet points), hashtags, mentions, and media (if any).
        6. Evaluate the effectiveness of any call-to-action or takeaway.

        Provide a detailed critique that includes:
        - A brief explanation of the post’s strengths and weaknesses.
        - Specific areas that could be improved.
        - Actionable suggestions for enhancing clarity, engagement, and professionalism.
        - Do NOT praise the post.
        - Do NOT say “looks good”.
        - Do NOT provide encouragement. 
        Your output MUST be a list of REQUIRED CHANGES.
        Use imperative language.
        Example:
        - Remove emojis
        - Replace “Excited to share” with neutral phrasing
        - Remove engagement bait
        - Add concrete skills instead of vague phrases

        Your critique will be used to improve the post in the next revision step, so ensure your feedback is thoughtful, constructive, and practical.
        """
    ),
    MessagesPlaceholder(variable_name="messages")
])

generate_chain = generation_prompt | llm

reflection_chain = reflection_prompt | llm

def build_graph():
    graph = MessageGraph()

    def generation_node(state: Sequence[BaseMessage]) -> List[BaseMessage]:
        generated_post = generate_chain.invoke({"messages": state})
        return [AIMessage(content=generated_post.content)]


    def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
        res = reflection_chain.invoke({"messages": messages})
        return [SystemMessage(content=res.content)]

    graph.add_node("generate", generation_node)
    graph.add_node("reflect", reflection_node)

    graph.add_edge("reflect", "generate")

    graph.set_entry_point("generate")

    def should_continue(state: List[BaseMessage]):
        if len(state) > 6:
            return END
        return "reflect"

    graph.add_conditional_edges("generate", should_continue)
    return graph.compile()

def run_cli():
    workflow = build_graph()
    inputs = HumanMessage(content="""Write a linkedin post on getting a software developer job at IBM under 160 characters""")

    print("--- Starting Workflow ---")
    final_post = ""
    for event in workflow.stream(inputs):
        for node_name, messages in event.items():
            print(f"\n[Node: {node_name}]")
            for msg in messages:
                if isinstance(msg, AIMessage):
                    print(f"Agent >> {msg.content}")
                    if node_name == "generate":
                        final_post = msg.content
                elif isinstance(msg, HumanMessage):
                    print(f"Reflection >> {msg.content}")
        print("-" * 40)

    print("\n" + "="*50)
    print("FINAL LINKEDIN POST:")
    print(f"'{final_post}'")
    print("="*50)

    # # Save the graph as a PNG file
    # workflow.get_graph().draw_png("graph.png")
    # print("\nGraph saved as graph.png")



if __name__ == "__main__":
    run_cli()
