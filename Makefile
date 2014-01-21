NUM_FEATURES=1000
MAX_ITER=800
TRAINING_PERCENT=80
TAGS=`wc -l tags.vec  | awk '{print $$1}'`

all: check_predictions.debug


clean:
	rm -f *.pyc *.vec *.json *.mat *.debug

top_words.vec:
	python ./words.py --exclude stop_words.csv --output top_words.vec ${NUM_FEATURES} title,description all_items_listed.csv

listed.vec: top_words.vec
	python ./vectorize.py --output listed.vec ./top_words.vec title,description ./all_items_listed.csv

tags.vec:
	python ./tags.py --output tags.vec ./tagged_items.csv

tagged_items.vec:
	python ./tag.py --output tagged_items.vec ./tagged_items.csv

training_tags.vec: tagged_items.vec
	./split_tags.sh ./tagged_items.vec training_tags.vec testing_tags.vec ${TRAINING_PERCENT}

testing_tags.vec: tagged_items.vec
	./split_tags.sh ./tagged_items.vec training_tags.vec testing_tags.vec ${TRAINING_PERCENT}

tags_listed.vec: listed.vec training_tags.vec
	./join_csv.py --output tags_listed.vec training_tags.vec listed.vec:0:0

theta.mat: tags_listed.vec tags.vec
	octave ./calc_theta.m  ./tags_listed.vec ${TAGS} ${MAX_ITER} theta.mat

item_predictions.vec: theta.mat listed.vec
	octave ./calc_predictions.m ./listed.vec theta.mat item_predictions.vec

check_predictions.debug: item_predictions.vec testing_tags.vec
	./join_csv.py testing_tags.vec item_predictions.vec:0:0 | tr "," " " | awk 'BEGIN{good=0; bad = 0}{if($$2==$$3){good++}else{bad++}}END{print good,bad,int(100*good/(good+bad))"%"}' | tee check_predictions.debug
	./join_csv.py testing_tags.vec item_predictions.vec:0:0 | perl -ne 'chomp; @s=split(",", $$_); if($$s[1]==$$s[2]){$$good++;}else{$$bad++;}BEGIN{$$good=0; $$bad = 0;}END{$$ratio = $$good/($$good+$$bad); print "$$good $$bad $$ratio\n"}'
