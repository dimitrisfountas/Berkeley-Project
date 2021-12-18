# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        ghostPositions = successorGameState.getGhostPositions()
        cost=0
        foodList = newFood.asList()
        if foodList:
            closeFoodDist = min([manhattanDistance(newPos, food) for food in foodList])
        ghosts=[]
        for ghost in ghostPositions:
            if manhattanDistance(newPos, ghost)== 0: return float('-inf')
            ghosts.append(manhattanDistance(newPos,ghost))
        gostDist=min(ghosts)
        numFood = currentGameState.getNumFood()
        newNumFood = successorGameState.getNumFood()
        if newNumFood < numFood: return 999999
        if action == Directions.STOP:
            return -9999999
        if len(foodList) == 0:
            return float('inf')
        return -closeFoodDist+gostDist/250+currentGameState.getScore()



def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        def minimax(gameState,agent,depth):
            if agent==gameState.getNumAgents():
                agent=0
                depth+=1
            if agent==0:
                return max_value(gameState,depth)
            else:
                return min_value(gameState,agent,depth)


        def max_value(gameState,depth):
            Actions=gameState.getLegalActions(0)
            if len(Actions)==0 or  depth==self.depth:
                return[self.evaluationFunction(gameState),None]
            max=float("-inf")
            best_action=None
            successors=[(gameState.generateSuccessor(0,action),action) for action in gameState.getLegalActions(0)]
            for successor,action in successors:
                value=minimax(successor,1,depth)
                if value[0]>max:
                    max =value[0]
                    best_action=action
            return[max,best_action]

        def min_value(gameState,agent,depth):
            Actions=gameState.getLegalActions(agent)
            if len(Actions) == 0:
                return[self.evaluationFunction(gameState),None]
            min=float("inf")
            best_action=None
            for action in Actions:
                value=minimax(gameState.generateSuccessor(agent,action),agent+1,depth)
                value=value[0]
                if(value<min):
                    min,best_action=value,action
            return[min,best_action]
        max_value=max_value(gameState,0)[1]
        return max_value
        util.raiseNotDefined()































class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def minimax(gameState,agent,depth,a,b):
            if agent==gameState.getNumAgents():
                agent=0
                depth+=1
            if agent==0:
                return max_value(gameState,depth,a,b)
            else:
                return min_value(gameState,agent,depth,a,b)

        def max_value(gameState,depth,a,b):
            Actions = gameState.getLegalActions(0)
            if len(Actions)==0 or gameState.isWin() or gameState.isLose() or depth==self.depth:
                return (self.evaluationFunction(gameState), None)
            w=-(float("inf"))
            best_action=None
            for action in Actions:
                value=min_value(gameState.generateSuccessor(0,action),1,depth,a,b)
                value=value[0]
                if w<value:
                    w,best_action=value,action
                if w>b:
                    return (w,best_action)
                a=max(a,w)
            return (w,best_action)

        def min_value(gameState,agent,depth,a,b):
            " Cases checking "
            Actions=gameState.getLegalActions(agent)
            if len(Actions) == 0:
                return (self.evaluationFunction(gameState),None)
            l = float("inf")
            best_action = None
            for action in Actions:
                value = minimax(gameState.generateSuccessor(agent,action),agent + 1,depth,a,b)
                value=value[0]
                if (value<l):
                    l,best_action=value,action
                if (l<a):
                    return (l,best_action)
                b=min(b,l)
            return(l,best_action)

        a=-(float("inf"))
        b=float("inf")
        max_value=max_value(gameState,0,a,b)[1]
        return max_value
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def minimax(gameState,agent,depth):
            if agent==gameState.getNumAgents():
                agent=0
                depth+=1
            if agent==0:
                return max_value(gameState,depth)
            else:
                return exp_value(gameState,agent,depth)
        def max_value(gameState,depth):
            Actions=gameState.getLegalActions(0)
            if len(Actions)==0 or  depth==self.depth:
                return[self.evaluationFunction(gameState),None]
            max=float("-inf")
            best_action=None
            successors=[(gameState.generateSuccessor(0,action),action) for action in gameState.getLegalActions(0)]
            for successor,action in successors:
                value=minimax(successor,1,depth)
                if value[0]>max:
                    max =value[0]
                    best_action=action
            return[max,best_action]




        def exp_value(gameState,agent,depth):
            Actions=gameState.getLegalActions(agent)
            if len(Actions) == 0:
                return[self.evaluationFunction(gameState),None]
            average=0
            best_action=None
            for action in Actions:
                value=minimax(gameState.generateSuccessor(agent,action),agent+1,depth)
                value=value[0]
                prob=value/len(Actions)
                average+=prob
            return[average,best_action]
        max_value=max_value(gameState,0)[1]
        return max_value
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    position=currentGameState.getPacmanPosition()
    food=currentGameState.getFood().asList()
    capsules=currentGameState.getCapsules()
    cost=0
    dist=[]
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")
    eat=[]
    for apple in food:
        eat+=[manhattanDistance(position,apple)]
    if len(eat)!=0:
        cost-=min(eat)
    else:
        return(float("inf"))
    for i in range(currentGameState.getNumAgents() - 1):
        dist+=[manhattanDistance(position,currentGameState.getGhostPosition(i+1))]
    if len(dist)!=0:
        cost+=min(dist)
    superfood=[]
    for capsule in capsules:
        superfood+=[manhattanDistance(position,capsule)]
    if len(superfood)!=0:
        cost-=min(superfood)
    if len(superfood)>=2:
        cost-=max(superfood)
    return cost+2*currentGameState.getScore()









    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
