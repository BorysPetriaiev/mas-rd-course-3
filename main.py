import uuid
from agent import agent_executor
from dotenv import load_dotenv

load_dotenv()

def run_chat():
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    print("🤖 Агент-дослідник готовий! (exit для виходу)")
    
    while True:
        user_input = input("\nВи: ")
        if user_input.lower() in ["exit", "quit", "вихід"]:
            break
            
        for event in agent_executor.stream(
            {"messages": [("user", user_input)]},
            config={"configurable": {"thread_id": "1"}, "recursion_limit": 10},
            stream_mode="updates"
        ):
            for node, data in event.items():
                if node == "agent":
                    message = data["messages"][-1]
                    if message.tool_calls:
                        for tool in message.tool_calls:
                            print(f"\n🤔 [Thought]: Вирішив використати інструмент: **{tool['name']}**")
                            print(f"   Аргументи: {tool['args']}")
                    elif message.content:
                        print(f"\n📝 [Final Answer]: {message.content}")
                
                elif node == "tools":
                    print(f"✅ [Tool Result]: Інструменти завершили роботу")

if __name__ == "__main__":
    run_chat()