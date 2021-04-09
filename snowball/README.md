Bootstrapping Relationship Extraction with Distributional Semantics
===================================================================

Demo
====


python friend_main.py parameters.cfg HP_processed_TAG_final.txt friend_seeds_positive.txt friend_seeds_negative.txt 0.5 0.5

python foe_main.py parameters.cfg HP_processed_TAG_final.txt foe_seeds_positive.txt foe_seeds_negative.txt 0.5 0.5

You can edit the file it wirtes to on line 140

NOTE: in between running you need to delete the processed_tuples.plk - Otherwise you are not getting the NEW tuples of the file


Dependencies
============

You need to have Python 3.6.5 and the following libraries installed:

**Numpy**: http://www.numpy.org/

**NLTK**: http://www.nltk.org/

**Gensim**: https://radimrehurek.com/gensim/

which you can install issuing the following command:

    pip install -r requirements.txt

You also need to install NLTK's Treebank PoS-tagger, stop words list, punkt, and wordnet:

    import nltk
    nltk.download('maxent_treebank_pos_tagger')
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')
    
You need to specify a word2vec model in the `parameters.cfg` file, the model used in my experiments is available for download. It was generated from the sub collections of the English Gigaword Collection, namely the AFP, APW and XIN. The model is available here: 

[afp_apw_xin_embeddings.bin](https://drive.google.com/file/d/0B0CbnDgKi0PyZHRtVS1xWlVnekE/view?usp=sharing)


Usage:
=====

**parameters**

A sample configuration is provided in `parameters.cfg`. The file contains values for differentes parameters:

    max_tokens_away=6           # maximum number of tokens between the two entities
    min_tokens_away=1           # minimum number of tokens between the two entities
    context_window_size=2       # number of tokens to the left and right

    wUpdt=0.5                   # < 0.5 trusts new examples less on each iteration
    number_iterations=4         # number of bootstrap iterations
    wUnk=0.1                    # weight given to unknown extracted relationship instances
    wNeg=2                      # weight given to extracted relationship instances
    min_pattern_support=2       # minimum number of instances in a cluster to be considered a pattern

    word2vec_path=vectors.bin   # path to a word2vecmodel in binary format

    alpha=0.2                   # weight of the BEF context in the similarity function
    beta=0.6                    # weight of the BET context in the similarity function
    gamma=0.2                   # weight of the AFT context in the similarity function



References:
==========
BREDS is a bootstrapping system for relationship extraction relying on word vector representations (i.e., word embeddings). For more details please refer to:

- David S Batista, Bruno Martins, and Mário J Silva. , [Semi-Supervised Bootstrapping of Relationship Extractors with Distributional Semantics](http://davidsbatista.net/assets/documents/publications/breds-emnlp_15.pdf). In Empirical Methods in Natural Language Processing. ACL, 2015. (Honorable Mention for Best Short Paper)

- David S Batista, Ph.D. Thesis, [Large-Scale Semantic Relationship Extraction for Information Discovery (Chapter 5)](http://davidsbatista.net/assets/documents/publications/dsbatista-phd-thesis-2016.pdf), Instituto Superior Técnico, University of Lisbon, 2016

- [Presentation at PyData Berlin 2017](https://www.youtube.com/watch?v=Ra15lX-wojg)

  &nbsp;&nbsp;[![Presentation at PyData Berlin 2017](https://img.youtube.com/vi/Ra15lX-wojg/default.jpg)](https://www.youtube.com/watch?v=Ra15lX-wojg)

