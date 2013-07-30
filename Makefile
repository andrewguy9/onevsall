all: predictions.csv

clean: 
	rm -f *.pyc *.vec *.json *.mat

#TODO MAKE FEATURES A VAR.
top_words.json:
	python ./words.py ./all_items_listed.csv 1000 > top_words.json

listed.vec: top_words.json
	python ./vectorize.py ./top_words.json ./all_items_listed.csv > listed.vec

tags.vec:
	python ./tag.py ./tagged_items.csv > tags.vec

tags_listed.vec: listed.vec tags.vec
	./join_csv.py --data tags.vec listed.vec --keys 0 0 > tags_listed.vec
	
#TODO 22 should be calculated
#TODO 1 SHOULD BE A VAR
theta.mat: tags_listed.vec
	octave ./calc_theta.m  ./tags_listed.vec 22 100 theta.mat

predictions.csv: theta.mat listed.vec
	octave ./calc_predictions.m ./listed.vec theta.mat predictions.csv
