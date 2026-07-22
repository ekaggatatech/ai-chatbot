from.chatbot import run_chatbot
print("Hourmaker Bot. Type 'exit' to quit")
while True:
    q=input("\nAsk:")
    if q.lower()=='exit':break
    res=run_chatbot(q)
    print("\n",res["answer"])