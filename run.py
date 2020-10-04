import aitools

from game import VisualGame
from game.utils import load_model

if __name__ == "__main__":
    policy_net = load_model("model")
    agent = aitools.rl.AgentProd(policy_net)

    env = VisualGame(10, 10)

    while True:
        agent(env)
