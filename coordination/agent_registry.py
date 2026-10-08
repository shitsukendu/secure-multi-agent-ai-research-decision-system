class AgentRegistry:

    def __init__(self):
        self.agents = {}

    def register(
        self,
        agent_name,
        role,
        description="",
        active=True
    ):

        self.agents[agent_name] = {
            "agent_name": agent_name,
            "role": role,
            "description": description,
            "active": active
        }

    def unregister(self, agent_name):

        if agent_name in self.agents:
            del self.agents[agent_name]
            return True

        return False

    def get_agent(self, agent_name):

        return self.agents.get(agent_name)

    def get_active_agents(self):

        return [
            agent
            for agent in self.agents.values()
            if agent["active"]
        ]

    def exists(self, agent_name):

        return agent_name in self.agents