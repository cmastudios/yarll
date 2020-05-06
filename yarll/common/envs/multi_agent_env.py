from typing import TypeVar, Dict, Tuple

from gym import Env, Space

Agent = TypeVar('Agent')
Observation = TypeVar('Observation')
Action = TypeVar('Action')

# Inspired by the design and examples of RLLib multi-agent

class MultiAgentEnv(Env):
    """An environment where multiple policies can interact simultaneously.
    Agents may come and go as the environment changes, and each may have their
    own varied action and reward spaces.

    Each of the core API methods step and reset act on and return dictionaries
    indexed by the applicable agent.

    The attributes action_space and observation_space are now dictionaries that
    map agent identifiers to the applicable space. They may initially be empty,
    but MUST be populated for each agent active in the environment at the time
    of returning from reset() or step().
    """
    all_done = '_all_done'

    action_space: Dict[Agent, Space] = {}
    observation_space: Dict[Agent, Space] = {}

    def reset(self) -> Dict[Agent, Observation]:
        """Reset the environment to a clean state and return initial
        observations.

        This method MUST be called at the start of interaction.

        The return value is a dictionary containing an agent-observation pair
        for each agent who should make a move next turn.
        """
        raise NotImplementedError

    def step(self, action_dict: Dict[Agent, Action]) -> Tuple[Dict[Agent, Observation], Dict[Agent, float], Dict[Agent, bool], Dict[Agent, dict]]:
        """This runs one timestep of the environment, using the provided agent
        actions.

        Note that this multi agent model supports agents coming and going as
        they please. Agents that moved in this turn won't necessarily move in
        the next turn. If they are not present in the observation/reward dicts,
        then they are considered "paused" until new observations and rewards
        have been returned for them. However, if they are marked as done at the
        end of this turn, then they should not make any future actions as they
        have been considered to have dropped out.

        This means we can handle turn-based games and simultaneous move games.

        The return value is a tuple of observations, rewards, dones, and infos.
        Agents moving in this step MUST have entries in the done dictionary. If
        any are True, that agent has been considered to have dropped out of the
        environment. Agents that should move in the next step MUST have entries
        in the observation and reward dictionary. 
        """
        raise NotImplementedError


# Examples of multi-agent environments

import gym

class RockPaperScissorsEnv(MultiAgentEnv):
    """Plays the simultaneous move game rock-paper-scissors with two agents.
    """
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    def __init__(self):
        # You get to choose rock, paper, or scissors
        self.action_space = {
                'agent1': gym.spaces.Discrete(3),
                'agent2': gym.spaces.Discrete(3),
                }
        # You get to see the opponent's last move
        self.observation_space = {
                'agent1': gym.spaces.Discrete(3),
                'agent2': gym.spaces.Discrete(3),
                }

    def reset(self):
        self.steps = 0
        return {'agent1': 0, 'agent2': 0}

    def step(self, action_dict):
        a1a, a2a = action_dict['agent1'], action_dict['agent2']
        reward = {}
        if ((a1a == self.ROCK and a2a == self.PAPER)
            or (a1a == self.PAPER and a2a == self.ROCK)
            or (a1a == self.SCISSORS and a2a == self.PAPER)):
            reward = {'agent1': 1, 'agent2': -1}
        elif ((a2a == self.ROCK and a1a == self.PAPER)
            or (a2a == self.PAPER and a1a == self.ROCK)
            or (a2a == self.SCISSORS and a1a == self.PAPER)):
            reward = {'agent1': -1, 'agent2': 1}
        else:
            reward = {'agent1': 0, 'agent2': 0}
        observation = {'agent1': a2a, 'agent2': a1a}
        self.steps += 1
        if self.steps >= 3:
            done = {'agent1': True, 'agent2': True, self.all_done: True}
        else:
            done = {'agent1': False, 'agent2': False}

        return observation, reward, done, {}


class PokemonBattle(MultiAgentEnv):
    """Plays a (simplified) turn-based Pokemon battle between two agents.
    """
    CHARMANDER = 0
    BULBASAUR = 1

    def __init__(self):
        # TODO
        pass



