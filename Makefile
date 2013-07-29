all: tags_listed.vec

clean: 
	rm -f *.pyc *.vec *.json

top_words.json:
	python ./words.py ./all_items_listed.csv 10 > top_words.json

listed.vec: top_words.json
	python ./vectorize.py ./top_words.json ./all_items_listed.csv > listed.vec

tags.vec:
	python ./tag.py ./tagged_items.csv > tags.vec

tags_listed.vec: listed.vec tags.vec
	./join_csv.py --data tags.vec listed.vec --keys 0 0 > tags_listed.vec
