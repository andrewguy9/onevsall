NUM_FEATURES=1000
MAX_ITER=400
TRAINING_PERCENT=100
TAGS=`wc -l tags.vec  | awk '{print $$1}'`

all: check_predictions.txt


clean:
	rm -f *.pyc *.vec *.json *.mat

top_words.vec:
	python ./words.py ./all_items_listed.csv ${NUM_FEATURES} > top_words.vec

listed.vec: top_words.vec
	python ./vectorize.py ./top_words.vec ./all_items_listed.csv > listed.vec

tags.vec:
	python ./tags.py ./tagged_items.csv | sort -n  > tags.vec

tagged_items.vec:
	python ./tag.py ./tagged_items.csv > tagged_items.vec

training_tags.vec: tagged_items.vec
	./split_tags.sh ./tagged_items.vec training_tags.vec testing_tags.vec ${TRAINING_PERCENT}

testing_tags.vec: tagged_items.vec
	./split_tags.sh ./tagged_items.vec training_tags.vec testing_tags.vec ${TRAINING_PERCENT}

tags_listed.vec: listed.vec training_tags.vec
	./join_csv.py training_tags.vec listed.vec:0:0 > tags_listed.vec

theta.mat: tags_listed.vec tags.vec
	octave ./calc_theta.m  ./tags_listed.vec ${TAGS} ${MAX_ITER} theta.mat

item_predictions.vec: theta.mat listed.vec
	octave ./calc_predictions.m ./listed.vec theta.mat item_predictions.vec

check_predictions.txt: item_predictions.vec testing_tags.vec
	./join_csv.py testing_tags.vec item_predictions.vec:0:0 | tr "," " " | awk 'BEGIN{good=0; bad = 0}{if($$2==$$3){good++}else{bad++}}END{print good,bad,int(100*good/(good+bad))"%"}' | tee check_predictions.txt
