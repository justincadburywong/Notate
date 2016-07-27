from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from notate_runner import run_opencv
from sync_files.models import Document
from sync_files.forms import DocumentForm
from list_moves import listMoves
from sync_files.models import Document, Notations
import sqlite3

def index(request):
	# How many images did user upload?
	imageCount = Document.objects.count()

	# Since deletion of previous images changes the first ID, 
	# This finds the first image in the database
	indexFirst = Document.objects.first().id
	# This next variable is one we increase within for loop
	increaseIndex = indexFirst
	print "increaseIndex"
	print increaseIndex

	for x in range(indexFirst,(indexFirst + imageCount)):
		# We cannot run this with only one image file left
		if (Document.objects.count() != 1):
			# This finds the first image to compare
			print "increaseIndex"
			print increaseIndex
			imageFirst = Document.objects.get(id=increaseIndex)
			print "image one"
			print imageFirst.docfile
			increaseIndex += 1
			
			# This finds the second image to compare
			print "increaseIndex"
			print increaseIndex
			imageSecond = Document.objects.get(id=(increaseIndex))
			print "image two"
			print imageSecond.docfile

			# Now we run the two images through OpenCV and return a notation
			notation = run_opencv(imageFirst.docfile.url, imageSecond.docfile.url)
			# We save that notation into the database
			newNotation = Notations(name=notation)
			newNotation.save()

			# We delete only the first image
			imageFirst.delete()

	# How many notations objects do we need to go through?
	notationCount = Notations.objects.count()

	# Since deletion of previous notations changes the first ID, 
	# This finds the first notation in the database
	notationIndexFirst = Notations.objects.first().id
	# This next variable is one we increase within for loop
	indexForNotation = notationIndexFirst

	# These variable save each instance of notation outside of 
	# the loop so we can constanly overwrite them
	moveWhite = ""
	moveBlack = ""

	# This variable stores the entire list of notations so 
	# they aren't overwritten by the for loop
	finalNotation = ""

	# This gets modified each time we go through the for loop
	# from white's move to black's move, starting with white's move
	whiteOrBlack = "white"

	for y in range(notationIndexFirst,(notationIndexFirst + notationCount)):

		# Stops when there are no more notations
		if (Notations.objects.count() != 0):
			# This prints out which move it is
			print "x"
			print x
			print "notationIndexFirst"
			print notationIndexFirst
			moveNumber = str(notationIndexFirst - (notationIndexFirst-1)) + ". "
			
			# notates for White's move
			if(whiteOrBlack == "white" and Notations.objects.count() != 0):
				moveWhite = Notations.objects.get(id=indexForNotation)

				# changes variable so that the next notation is black's
				whiteOrBlack = "black"
				indexForNotation +=1
				print "indexForNotation"
				print indexForNotation
				print "moveWhite"
				print moveWhite

				# Saves white's move
				finalNotation += str(moveNumber) + str(moveWhite)
				# Deletes the notation from the database
				moveWhite.delete()

			# notates for Blacks's move
			elif(whiteOrBlack == "black" and Notations.objects.count() != 0):
				moveBlack =  Notations.objects.get(id=indexForNotation)

				# changes variable so that the next notation is whites's
				whiteOrBlack = "white"
				indexForNotation +=1
				print "indexForNotation"
				print indexForNotation
				print "moveBlack"
				print moveBlack

				# Saves black's move
				finalNotation += " .. " + str(moveBlack) + "\n"
				# Deletes the notation from the database 
				moveBlack.delete()

	# This prints the finalNotation (list of all notations) 
	# into the web browser 
	return HttpResponse(finalNotation)

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'list.html',
        {'documents': documents, 'form': form}
    )
    # return HttpResponse("yippee")







