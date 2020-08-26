import torch
import aitools
from game.utils import save_model, load_model

from game import Game, VisualGame


if __name__ == "__main__":
    env = Game(10, 10)

    policy_net = None

    if False:
        policy_net = (
            aitools.nn.NetworkFF.Builder(env.get_size_obs())
            .add_layer(200, torch.nn.functional.relu)
            .add_layer(200, torch.nn.functional.relu)
            .add_layer(env.get_size_action(), torch.nn.functional.softmax)
            .build()
        )
    else:
        policy_net = load_model()

    agent = aitools.rl.AgentExploring(policy_net=policy_net)
    trainer = aitools.rl.train.VPGTrainer(
        agent=agent,
        optimizer=policy_net.build_optimizer(torch.optim.Adam, lr=0.0005),
        y=0.99,
    )

    value_net = (
        aitools.nn.NetworkFF.Builder(env.get_size_obs())
        .add_layer(120, torch.nn.functional.relu)
        .add_layer(120, torch.nn.functional.relu)
        .add_layer(1)
        .build()
    )
    value_estimator = aitools.rl.value.ValueEstimator(
        value_net,
        value_net.build_optimizer(torch.optim.Adam, lr=0.02),
        loss_f=torch.nn.functional.mse_loss,
    )

    aitools.rl.train.TrainingProcess(trainer).set_env(env).set_baseline_provider(
        value_estimator
    ).plot().train(30, 10000)

    save_model(policy_net)
