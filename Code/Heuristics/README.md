# Heuristics
We have used different heuristics/methods for this project. These will be explained down below.

#### depth first
This heuristic removes connections one by one that occur more than once in a lining system. This ensures an improvement of the quality as a result of the total time (Min) being reduced.

#### greedy
This heuristic creates a random lining system and remembers the solution as the best solution and the quality as the best quality. Then it will repeat those steps and checks if the quality is better than the best quality. This heuristic will run a given amount of time.

#### random once
This heuristic creates a random lining system where a connection between two stations can only occur once in a lining system. In other words: a connection between two stations cannot occur two or more times in all pathways from a lining system.

#### random twice
This heuristic creates a random lining system where a connection between two stations can occur twice in a lining system. In other words: a connection between two stations can occur twice in all pathways from a lining system.