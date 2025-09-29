#decoupling


from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

# from crewai_tools import SerperDevTool, ScrapeWebsiteTool, DirectoryReadTool, FileWriterTool, FileReadTool

from dotenv import load_dotenv
load_dotenv()

@CrewBase
class BlogCrew():
    """"My Blog writing crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/taks.yaml"

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['research_agent'],
            # tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer_agent'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent = self.researcher()
        )

    @task
    def blog_task(self) -> Task:
        return Task(
            config=self.tasks_config['blog_task'],
            agent = self.writer()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.researcher(), self.writer()],
            tasks=[self.research_task(), self.blog_task()]
        )

if __name__ == "__main__":
    blog_crew = BlogCrew()
    blog_crew.crew().kickoff(inputs={"topic": "The future of AI"})