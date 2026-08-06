from.chatbot import run_chatbot
history=[]
print("Hourmaker Bot. Type 'exit' to quit")
while True:
    q=input("\nAsk:")
    if q.lower()=='exit':break
    res=run_chatbot(q, history)
    print("\n",res["answer"])    
    # Save the history
    history.append({"role":"user","content":q})
    history.append({"role":"assistant","content":res["answer"]}) 

print("\nHistory:")
for msg in history:
    print(msg)