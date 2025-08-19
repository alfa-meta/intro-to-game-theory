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


Exercise 14.1:
	Players: A, B
	Actions: {Work Hard, Goof off}
	Preferences: Work Hard only when the other Works Hard.
	Preference A: (WH, WH) > {GO, WH} > {GO, GO} > {WH, GO}

| Game      | Work Hard | Goof Off |
| --------- | --------- | -------- |
| Work Hard | (3,3)     | (0,2)    |
| Goof off  | (2,0)     | (1,1)    |

#### 2.2.2 Duopoly
Exercise 16.1:
	Players: FishA, FishB
	Actions: {H, L}
	Preferences: {P,P} > {P, N}, {N, P} > {N, N}

| Game      | Preferred | Other |
| --------- | --------- | ----- |
| Preferred | (3,3)     | (0,2) |
| Other     | (2,0)     | (1,1) |
![[Pasted image 20250819001500.png]]

### 2.3 Example: Bach or Stravinsky

A situation where two people want to cooperate but disagree what to cooperate with such as:

| Game       | Bach  | Stravinsky |
| ---------- | ----- | ---------- |
| Bach       | (2,1) | (0,0)      |
| Stravinsky | (0,0) | (1, 2)     |
This is best exemplified when two merging companies have two different Computer Technologies. Linux vs Windows, where both companies want to use their own technology as not to start learning something new, however they want to cooperate with the other company.

Exercise 17.2:
	Players: A, B
	Actions: {P, N}
	Preferences: {P, N}, {N, P} > {N, N}, {P, P}

| Game - Tennis | Left  | Right  |
| ------------- | ----- | ------ |
| Left          | (0,0) | (2,2)  |
| Right         | (2,2) | (0, 0) |

Arms Race:
![[Pasted image 20250819004706.png]]