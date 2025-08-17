Strategic game is a model of interacting decision-makers.

Decision-makers - players
Each player has a set of possible actions.
The model captures interaction between the players by allowing each player to be affected by the actions of all players, not only her own action.

Strategic game with ordinal preferences consists of:
- a set of `players`
- for each player, a set of `actions`
- for each player, `preferences` over the set of action profiles.

Time is absent form the models.
Games without time are considered simultaneous move games.


### 2.2 Prisoner's Dilemma

Example 12.1:
	Players: Suspect 1, Suspect 2
	Actions: {Quiet, Fink}

	Player 1's preferences: {Fink, Quiet} - Free, {Quiet, Quiet} - 1 year, {Fink, Fink} - 3 years, {Quiet, Fink} - 4 years.
	Suspect 2's ordering is: {Quiet, Fink}, {Quiet, Quiet}, {Fink, Fink}, {Fink, Quiet}.

	Payoff function:
		u1(Fink, Quiet) > u1{Quiet, Quiet} > u1{Fink, Fink} > u1{Quiet, Fink}