#Import statements needed to run program
from pyswip import Prolog
import easygui
import random

#Interface to start conversation with child
def askFirst():
	title = "Introduction"
	image = "hi_baby.png"
	msg = 'Hi Baby! Welcome Home!'
	choices = ["OK"]
	return easygui.buttonbox(msg, title=title, image=image, choices=choices)

#Interface to ask if child did an activity
#Word added in front to denote positive or negative feelings by parent
#Returns True if 'Yes', False if 'No
def ask(activity, frontWord):
	if activity == "eat_noodles":
		image = "eat_noodles.png"
	elif activity == 'eat_watermelon':
		image = "eat_watermelon.png"
	elif activity == "eat_sandwich":
		image = "eat_sandwich.png"
	elif activity == "watch_movie":
		image = "watch_movie.png"
	elif activity == "watch_comedy":
		image = "watch_comedy.png"
	elif activity == "watch_cartoon":
		image = "watch_cartoon.png"
	elif activity == "learn_coding":
		image = "learn_coding.png"
	elif activity == "learn_ballet":
		image = "learn_ballet.png"
	elif activity == "learn_martial_arts":
		image = "learn_martial_arts.png"

	msg = ('{} Did you {} today?'.format(frontWord,activity))
	choices = ["Yes","No"]
	title = 'Activity Question'
	return easygui.boolbox(msg, title=title, image=image, choices=choices)


#Interface to ask child a related question to activity done
#Returns True if "Yes", False if "No"
def askRelatedQn(activity):
	msg = 'Oh! {} ?'.format(activity)
	choices = ["Yes","No"]
	title = "Related Question"
	return easygui.boolbox(msg, title=title,choices=choices)

#Main Program Starts
def main():

    # Initialize the prolog code
	prolog = Prolog()

	#Read "mekid.pl" file as a Prolog Source File 
	prolog.consult("3.kid_prolog.pl")

	#Initialise variables used
	activity = 'eat_noodles'		#Activity that child did
	frontWord = ''					#Word to place at the start of next sentence to denote feelings
	startLoop = True				#Loop Variable
	firstQuestion = True			#Variable to denote initial question asked
	kidReply = True					#Whether kid has done activity or not
	relatedQnReply = True			#Whether kid liked the activity or not
	positiveCounter = 0				#Counter for positive replies
	negativeCounter = 0				#Counter for negative replies

	# Main Program Loop
	while startLoop:
		
		#Ask first question 
		if firstQuestion:
			askFirst()
			kidReply = ask(activity, frontWord)
			firstQuestion = False	
		
		#Ask subsequent questions for activity 
		else:
			#If child has positive reply, ask with positive front word
			if relatedQnReply:
				kidReply = ask(activity, frontWord)
			#If chid has negative reply, ask with negative front word
			else:
				kidReply = ask(activity, frontWord)

		#Kid has done activity asked; Ask related question next
		if kidReply:
			relatedQnList = list(prolog.query('getRelatedQuestion({}, Y)'.format(activity)))#Query prolog
			relatedQn = random.choice(relatedQnList)['Y']									#Choose random related question to ask
			relatedQnReply = askRelatedQn(relatedQn)										#Ask related question

			#If kid likes activity
			if relatedQnReply:
				prolog.assertz('kidLike({})'.format(activity))								#Assert fact
				positiveWordList = list(prolog.query('getPositiveFront(positive,X)')) 		#Query prolog
				positiveFrontWord = random.choice(positiveWordList)['X']					#Choose random front word
				frontWord = positiveFrontWord
				relatedQnReply = True 
				positiveCounter = positiveCounter +1 										#Increment positive counter
			
			#If kid does not like activity
			else:
				prolog.assertz('kidDidntLike({})'.format(activity))							#Assert fact
				negativeWordList = list(prolog.query('getNegativeFront(negative,X)'))		#Query prolog
				negativeFrontWord = random.choice(negativeWordList)['X']					#Choose random front word
				frontWord = negativeFrontWord
				relatedQnReply = False
				negativeCounter = negativeCounter +1										#Increment negative counter

		#Kid has not done activity 
		else:
			neutralWordList = list(prolog.query('getNeutralFront(neutral,X)'))				#Query prolog
			neutralFrontWord = random.choice(neutralWordList)['X']							#Choose random front word
			frontWord = neutralFrontWord
			relatedQnReply = False
        
		#Assert fact
		prolog.assertz('kidAsked({})'.format(activity))

		#Query prolog for list of activities to ask next
		toAskList = list(prolog.query('getQuestion(X, {})'.format(activity)))
		listLength = len(toAskList)
		
		#No more activities to ask ie. all activities asked
		if listLength == 0:
			if(positiveCounter > negativeCounter):											#Child had positive day
				title = "Conclusion - Positive Day"
				image = "positive_day.png"
				msg = 'Good job sweetheart! Glad that you had an awesome day in school!'
				choices = ["OK"]
				easygui.buttonbox(msg, title=title, image=image, choices=choices)
			elif(negativeCounter > positiveCounter):										#Child has negative day
				title = "Conclusion - Negative Day"
				image = "negative_day.png"
				msg = 'Its alright sweetheart! I am sure you will have more fun tomorrow!'
				choices = ["OK"]
				easygui.buttonbox(msg, title=title, image=image, choices=choices)
			else:																			#Child had neutral day
				title = "Conclusion - Neutral Day"
				image = "neutral_day.png"
				msg = 'Seems like your day is fine!'
				choices = ["OK"]
				easygui.buttonbox(msg, title= title, image=image, choices=choices)																		
			
			startLoop = False 		#Stop main loop
			break

		#Take first element from the list as activity to be asked
		activity = toAskList[0]['X']

# Run the main program
if __name__ == "__main__":
	main()
