# Deep learning course project

This repo contains a deep learning course final project of team **supermoniveto**:
- Ville Tanskanen
- Ville Hyvönen
- Anisia Katinskaia


### Navigtion

#### Testing models
* [text_processing.py](https://github.com/vioshyvo/team-supermoniveto/blob/master/text_processing.py) python file for constructing and testing different CNN models. **Contains the final model.**
* [text_projectVilleT.ipynb](https://github.com/vioshyvo/team-supermoniveto/blob/master/text_projectVilleT.ipynb) python notebook for testing LSTM models.
* [test_onehot.py](https://github.com/vioshyvo/team-supermoniveto/blob/master/test_onehot.py) python file for testing MLP with bag-of-words presentation with whole data. **Contains the simple MLP model.**
* [text_project.ipynb](https://github.com/vioshyvo/team-supermoniveto/blob/master/text_project.ipynb) notebook with initial modeling with bag-of-words MLP with 10K/10K train/test split.
* [test_conv.py](https://github.com/vioshyvo/team-supermoniveto/blob/master/test_conv.py) python script with initial tests with a simple CNN with multiple parallel CNN layers.

#### Pre-processing & helpers

* [src/data_utility.py](https://github.com/vioshyvo/team-supermoniveto/blob/master/src/data_utility.py) contains the preprocessing functions such as downloading and parsing the data and tags. It also has functions to clean the texts and vectorize them.
* [tags_dist.py](https://github.com/vioshyvo/team-supermoniveto/blob/master/tags_dist.py) contains a function to plot the distribution of the tags.
* [text_generator.py](https://github.com/vioshyvo/team-supermoniveto/blob/master/text_generator.py) helper for training a network in batches.
* [check_test.py](https://github.com/vioshyvo/team-supermoniveto/blob/master/check_test.py) print predicted labels for the test set along with contents of files to perform a sanity check on the results

#### Delivering the results
* [read_test.py](https://github.com/vioshyvo/team-supermoniveto/blob/master/read_test.py) python script for reading the test set and predicting its outcome with the best model.


### Summary

The data we chose for our group was the [text data](https://keras.io/datasets/#reuters-newswire-topics-classification).
In the fashion of the course we used deep learning to learn the problem and do predictions.
We tried a vast range of different models ranging from the multilayer perceptron (MLP) built on top of the binary bag-of-words representation to the convolutional neural networks (CNN) and long short term memory networks (LSTM) built on top of the word embeddings.

We looked at the distribution of tags in the released data and found out that some of the topics are present most of the samples
 while others are never present, or appear very seldom. Rare tags would be difficult to learn to predict.
![](images/Figure_1.png)

Later we found out that tags are in hierarchical relations which explains why some tags are over-represented. We did not
use this information for our experiments.

### Pre-processing

First, we pre-processed the data, i.e. parsed xml-files, tokenized all texts, removed stop-words and punctuation,
lowercased all words and replaced numbers with NUM tag which might have not been a good idea as GloVe (see below) has embeddings for most of the numbers.

For the word embeddings we used the pre-trained [GloVe embeddings](https://nlp.stanford.edu/projects/glove/).
Most of the modelling is done with 200 dimensional representations and the competition model training was done with
300 dimensional representations. For words which are not presented in Glove embedding set we initialised vectors
of random numbers from normal distribution.

We divided the data set into a training set consisting of 80% of the news items, and into the test set and the validation set, which was used to compute the validation loss after each iteration to check for the convergence, each consisting of 10% of the corpus (In Keras term validation set is used in a bit different meaning than normally; I think that normally by the validation set is meant a set that is not used in the model selection phase, and which you use to estimate the generalization error of your best model). We decided not to do any cross-validation, because training of the models was slow enough even without it.

### Initial modelling attempts

Some verification of the model was done with 20K random sample from the data, which was split on the training set of 10K points and a test set of 10K points. A first thing we tried was a MLP with one hidden layer that was using a binary bag-of-words representation (on the file `text_project.ipynb`). This gave 0.79 F-score on the test set: this was a nice baseline for us to beat with more complicated models trained with the whole data set.

Experiments with combination of CNN and LSTM were done on the same 20K split that above BOW model used. With this little data, the best results were similar to the F-score achieved by the simple MLP. The best performance out of these trials was 0.7876 and it was achieved with one 1D convolutional layer with two following Dense layers with 512 and number of classes hidden units respectively. The best performance for LSTM-like network was with bidirectional LSTM, where it had the same dense layers, but instead of 1D convolution it had bidirectional LSTM layer with 100 memory units. This achieved F-score of 0.7067.


### CNN

During the testing, we quickly realized that CNN was showing much better F-score than any other models. As it seemed that
the CNN was the way to go, we experimented a lot of different sets of hyperparameters by hand (batch size, number of epochs,
dimensionality of embeddings, with/without random initialisation for words not presented in Glove embedding set, number of
convolutional layers, number and sizes of filters, size of dropout, with/without batch normalization, pool size, size and
number of dense layers). After exhaustive search for the best hyperparameters we had some idea of what would be
our chosen model for the competition. Most of the experiments with hyperparameters and their results (F-scores) are
saved in comments in text_processing.py module. Our best model has the following configuration:

![](images/CNN_conf.png)

The best model got the F-score equal to 0.8556 on our own test set. The loss and accuracy during training and validation presented on the figure below.

![](images/loss_acc.png)


### Bag-of-words

We also tried a very simple approach without any embeddings (experiments in the file `test_onehot.py`): we just read a whole training set into the binary bag-of-words format. This representation of the data has d = 402716 dimensions and each of the dimensions presents one word in a dictionary: it is 1 if the word is present for this document, and 0 otherwise. This representation discards all the information regarding the order and frequencies of the words (we also did some initial testing with using word counts or TF-IDF instead of the binary representation, but they gave worse results, so we stuck with the binary representation).

Then we build a MLP with only one hidden layer consisting of 64 nodes on top of this presentation (we already saw in the exercise set 4 that building a deeper network on top of this representation does not help the accuracy at all, but only makes the training slower) with dropout layer with the parameter 0.5 added before the output layer:

![](images/bow_model64.png)    

This simple network gave very nice results with F-score of 85.1% on our test set after training with 10 epochs. So the result is almost as good as with the much more complicated CNN approach (F-score of 85.4% on our test set). Our hypothesis is that this is because this kind of a topic classification is actually quite simple task, because each topic has a distinct (though they are of course heavily overlapping especially on the related topics) vocabulary. For instance if the news item has words `stock` and `price`, it is probably about stock markets, and so on.

This means that you do not actually have to extract the meaning or any sentence structures from the test to get very nice results, and this is why the simple MLP built on top of the bag-of-words representation, which discards all the information about the order of words, has a performance that is comparable to the much more complicated CNN and LSTM approaches.

### GRU, Bidirectional and other attempts

Being curious, we also expanded our views outside of the course and did some trials
with combination of CNN and LSTM where first comes the convolutions and then the LSTM is applied for the convolved layers. We also tried to approximate F-score by a differentiable function and optimize a network using that as a loss.
Final two models that we tried were bidirectional LSTM, which is used for the sequence classification when the whole sequence
is known, and gated recurrent unit (GRU) which should be similar to LSTM but have faster training as it is missing one
of the gates from LSTM. These approaches did not outperform any other methods but they had some interesting properties in terms of convergence speed in terms of real time and in epochs.


### Future work

During the project, we discussed a lot and unfortunately some of the ideas were left out because of lack of time.
There were bad ideas, decent ideas and great ideas. Some of the good ideas are presented below.

On the pre-processing side we could have done some phrase n-gram modelling.
That is, to concatenate some combination of n words that often occur together and have a different meaning when
 they are presented together rather than separately. Such words could be mapped to one index of dictionary instead
  of mapping them to different indexes. Examples of such words could be ice hockey for 2-gram, Golden State Warriors for 3-gram and so on.
   It would probably be enough to look at the 2-grams and 3-grams only as they would capture most of the structure
   in everyday language. However, one can find data sets that include 5-grams for example from [https://www.ngrams.info/download_coca.asp](https://www.ngrams.info/download_coca.asp).

   It also has been proposed that character n-gram models could improve the predictive power of the methods used. It is a method that uses subword information and combine it into a complete embedding. [fastText](https://fasttext.cc/) uses character n-grams among other methods. They too provide a ready-to-use word embeddings. These embeddings should improve the accuracy especially in the case of out of vocabulary words.

Reading the notes from Moodle, we also discussed that in order to capture the best result
in the tags we should follow their tree structure also in modelling. One approach could be that we first predict which one
of the "main" topics does an article belong, and then recursively go deeper with the predictions taking into account
the results achieved higher in the hierarchy of tags. Because there is hierarchy, we could also do some rule based
verification after our current model. That is, we could adjust our predictions by the tree structure.
For example, if we predict a tag that is in the same branch of the tag tree but we are not predicting its parents,
we should probably also predict the parent, or adjust the prediction so that we do not predict the child.
These could be handled whichever way, but the most important thing would be to avoid contradictions in the tree structure.

Since we tried out wide range of different kind of models, a natural way to expand the approach to the test set would be to train all of them with full data. After saving the models we could then use ensemble methods to perform the final predictions. Such approach would take a lot of time to train, but it could be beneficial as different models can capture different aspects of the news articles.
