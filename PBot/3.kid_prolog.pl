/* Initialize kidLike, kidDidntLike and kidAsked */
kidLike(nothing).
kidDidntLike(nothing).
kidAsked(nothing).


/*Declare dynamic procedures*/
:- dynamic kidLike/1.
:- dynamic kidDidntLike/1.
:- dynamic kidAsked/1.

/*Determine member of a list*/
member(X,[X|_]).
member(X,[_|R]) :- member(X,R).


/*List for front words*/
positiveFront(['Great!', 'Perfect!', 'Wonderful!']).
negativeFront(['Aww :(', 'Oh no :(', 'Oh dear :(']).
neutralFront(['Hmm,','I see,', 'Really?']).

/*List of activities based on categories*/
eat([eat_noodles, eat_watermelon, eat_sandwich]).
watch([watch_movie, watch_comedy, watch_cartoon]).
learn([learn_ballet, learn_coding, learn_martial_arts]).

/*List of related questions to asked based on activities category*/
eat_related(['Was it tasty','Did it taste good','Did you like it','Was it yummy']).
watch_related(['Was it funny','Was it nice','Was it exciting','Did you like the movie']).
learn_related(['Did you enjoy the session','Was it engaging','Was it fun']).


/*Start by asking if kid ate noodles */
getQuestion(eat_noodles, 0).

/*Rules to determine what question to ask next.
  All rules do not ask activities which are asked before*/
/*If kid likes the activity, ask a related activity which has not been asked*/
getQuestion(X,Y):- kidLike(Y), relatedActivity(X,Y), \+ kidAsked(X).

/*If kid did not like the activity, ask a random activity that is not related to previous activity asked 
ie. activity from another category*/
getQuestion(X,Y):- kidDidntLike(Y), randomActivity(X), \+ relatedActivity(X,Y), \+ kidAsked(X).

/*Default rule to ask a random activity that has not been asked*/
getQuestion(X,Y):- kidAsked(Y), randomActivity(X), \+ kidAsked(X).


/*Rules to determine front word*/
/*Get positive front word*/
getPositiveFront(positive,X):- positiveFront(L), random_member(X,L).

/*Get negative front word*/
getNegativeFront(negative,X):- negativeFront(L), random_member(X,L).

/*Get neutral front word*/
getNeutralFront(neutral,X):- neutralFront(L), random_member(X,L).


/*Determine the related question to be asked based on activity done*/
getRelatedQuestion(X, Y) :-
	eat(L), member(X, L), eat_related(M), member(Y,M);
	watch(L), member(X, L), watch_related(M), member(Y,M);
	learn(L), member(X, L), learn_related(M), member(Y,M).

/*Determine if 2 activities are related*/
relatedActivity(X,Y) :-
	eat(L), member(X, L), member(Y, L);
	watch(L), member(X, L), member(Y, L);
	learn(L), member(X, L), member(Y, L).

/*Get random activity*/
randomActivity(X) :-
	eat(L), member(X, L);
	watch(L), member(X, L);
	learn(L), member(X, L).



