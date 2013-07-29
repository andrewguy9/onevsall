all: top_words.json listed_vector.csv tag_vector.csv

clean: 
	rm -f top_words.json listed_vector.csv tags.csv 

top_words.json:
	python ./words.py ./hawaii_items_listed.csv 10 > top_words.json

listed_vector.csv:
	python ./vectorize.py ./top_words.json ./hawaii_items_listed.csv > listed_vector.csv

tag_vector.csv:
	python ./tag.py ./tagged_items.csv > tagged_vector.csv
