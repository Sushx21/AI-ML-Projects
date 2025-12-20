from dotenv import load_dotenv
load_dotenv()

from langchain.globals import set_verbose, set_debug
from langchain_groq.chat_models import ChatGroq

from langgraph.constants import END
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent
set_verbose(True)
set_debug(True)
llm = ChatGroq(model="moonshotai/kimi-k2-instruct-0905") #Better parameters model  might have token limit so need to switch to api key
#
# response=llm.invoke("whats mint chocolate icecream")
#
# print(response.content)   # testing


from prompts import *
from states import *
from tools import *



def planner_agent(state: dict) -> dict:     #dict as input and dict as output
    """Converts user prompt into a structured Plan."""
    users_prompt = state["user_prompt"]
    resp = llm.with_structured_output(Plan).invoke(planner_prompt(user_prompt))

    return {"plan": resp}

    if resp is None:
        raise ValueError("Planner did not return a valid response.")#Throw exception if none     return {"plan": resp}




def architect_agent(state: dict) -> dict:
    """Creates TaskPlan from Plan."""
    plan = state["plan"]
    resp = llm.with_structured_output(TaskPlan).invoke(
        architect_prompt(plan))

    if resp is None:
        raise ValueError("Architect did not return a valid response.")

    resp.plan=plan  #Appending input and output to maintain better context                #This is coming from config dict allow from states



    return {"task_plan": resp}


def coder_agent(state: dict) -> dict:
    """LangGraph tool-using coder agent."""
    coder_state: CoderState = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state, "status": "DONE"} #will help exit graph
    current_task=steps[coder_state.current_step_idx]


    existing_content = read_file.run(current_task.filepath)
    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content:\n{existing_content}\n"
        "Use write_file(path, content) to save your changes."
    )

    system_prompt = coder_system_prompt()


    coder_tools = [read_file, write_file, list_files, get_current_directory]
    react_agent = create_react_agent(llm, coder_tools)

    react_agent.invoke({"messages": [{"role": "system", "content": system_prompt},
                                     {"role": "user", "content": user_prompt}]})

    #system,user,assistant write code in susnat generated

    coder_state.current_step_idx += 1

    return {"coder_state": coder_state}




graph = StateGraph(dict)# structure of state dictinor
graph.add_node("planner", planner_agent)

graph.add_node("architect", architect_agent)

graph.add_node("coder",coder_agent)
graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")

graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
                          {"END": END, "coder": "coder"}
                            )



graph.set_entry_point("planner")
agent=graph.compile()


#Planner( tech stack,features( feature description), Files{path:description})
#Architect ( Files) {path:Task description},will further guide it like a real word setup




if __name__ == "__main__":
    user_prompt="Build a todo list in mint turquoise color  give header Susnata  and give add functionalaity so that its use ready and delete functionality too "
    result=agent.invoke({"user_prompt": user_prompt},
                        {"recursion_limit":100})

    print(result)