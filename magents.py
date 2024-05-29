from openai import OpenAI
import os
import json

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class Agent:
    def __init__(self, role, goal, backstory, tools=None, memory=True, verbose=False, max_rpm=None, max_iter=25):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []
        self.memory = memory
        self.verbose = verbose
        self.max_rpm = max_rpm
        self.max_iter = max_iter
        self.context = []

    def log(self, message):
        if self.verbose:
            print(message)

    def add_to_context(self, message):
        if self.memory:
            self.context.append(message)

    def generate_prompt(self, task):
        context_str = "\n".join(self.context) if self.memory else ""
        prompt = f"Role: {self.role}\nGoal: {self.goal}\nBackstory: {self.backstory}\nContext: {context_str}\nTask: {task}"
        return prompt

    def call_gpt4(self, prompt):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            self.log(f"Error calling GPT-4 API: {e}")
            return None

    def execute_task(self, task):
        prompt = self.generate_prompt(task)
        response = self.call_gpt4(prompt)
        if response:
            self.log(f"AI Response: {response}")
            self.add_to_context(response)
            return response
        else:
            self.log("Failed to generate a response.")
            return None


# Example Tools
class SearchTool:
    def search(self, query):
        return f"Searching for: {query}"


class SummarizeTool:
    def summarize(self, text):
        return f"Summarizing: {text[:100]}..."


def create_technical_agents():
    search_tool = SearchTool()
    summarize_tool = SummarizeTool()

    agents = [
        Agent(
            role="Project Manager",
            goal="Manage project timelines and deliverables",
            backstory="A project manager with a track record of successful project delivery.",
            tools=[search_tool],
            verbose=True
        ),
        Agent(
            role="Developer/Software Engineer",
            goal="Develop and implement technical solutions",
            backstory="A skilled developer who excels in coding and implementation.",
            tools=[summarize_tool],
            verbose=True
        ),
        Agent(
            role="Cloud Engineer",
            goal="Design and manage cloud infrastructure",
            backstory="An expert in cloud architecture and management.",
            tools=[search_tool, summarize_tool],
            verbose=True
        ),
        Agent(
            role="Platform Engineer",
            goal="Ensure platform stability and performance",
            backstory="A specialist in platform engineering and optimization.",
            tools=[summarize_tool],
            verbose=True
        ),
        Agent(
            role="Site Reliability Engineer (SRE)",
            goal="Maintain and improve service reliability",
            backstory="Focused on ensuring system reliability and uptime.",
            tools=[search_tool],
            verbose=True
        ),
        Agent(
            role="DevOps Engineer",
            goal="Streamline development and operations",
            backstory="Bridges the gap between development and operations for efficient workflows.",
            tools=[summarize_tool],
            verbose=True
        ),
        Agent(
            role="SecOps Engineer",
            goal="Ensure security operations and compliance",
            backstory="Specializes in securing systems and ensuring compliance.",
            tools=[search_tool],
            verbose=True
        ),
        Agent(
            role="QA Engineer",
            goal="Test and ensure the quality of the product",
            backstory="Ensures the product meets quality standards through rigorous testing.",
            tools=[summarize_tool],
            verbose=True
        )
    ]

    # Adding a CTO agent for validation
    cto_agent = Agent(
        role="CTO",
        goal="Validate project plans and deliverables",
        backstory="Chief Technology Officer overseeing technical strategies.",
        tools=[summarize_tool],
        verbose=True
    )

    return agents, cto_agent


def ask_user_questions():
    print("Welcome to the AI Agent Framework!")
    agent_class = input("What class of agents do you need (Technical/Leadership)? ")
    task = input("What task would you like the AI agent to accomplish? ")
    additional_info = input("Please provide any additional information to help with the task: ")
    return agent_class, task, additional_info


def main():
    agent_class, task, additional_info = ask_user_questions()

    if agent_class.lower() == "technical":
        agents, cto_agent = create_technical_agents()
    else:
        print(f"Invalid agent class: {agent_class}. Please choose 'Technical'.")
        return

    project_manager = agents[0]
    project_manager.log(f"Task received: {task}\nAdditional info: {additional_info}")
    response = project_manager.execute_task(task)

    if response:
        project_manager.log(f"Reporting to CTO: {response}")
        cto_response = cto_agent.execute_task(response)
        if cto_response:
            project_manager.log(f"CTO Validation: {cto_response}")
            for agent in agents[1:]:
                agent.log(f"Executing task: {response}")
                agent_response = agent.execute_task(response)
                if agent_response:
                    project_manager.log(f"Response from {agent.role}: {agent_response}")
        else:
            print("CTO failed to validate the project plan.")
    else:
        print("Project Manager failed to produce a result.")


if __name__ == "__main__":
    main()
