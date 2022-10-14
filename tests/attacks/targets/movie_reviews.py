import pickle
import re
import copy

import numpy as np
import pandas as pd
from torch import nn
import torch

from counterfit.core.targets import CFTarget

class MovieReviewsTarget(CFTarget):
    """Defining movie reviews target which is responsible for predicting the scores for a given input and convert scores to labels.
    """
    data_type = "text"
    name = "movie_reviews"
    endpoint = f"movie_reviews_sentiment_analysis.pt"
    input_shape = (1,)
    output_classes = [0, 1]  # textattack requires these to be integers
    classifier = "blackbox"

    sample_input_path = f"movie-reviews-scores-full.csv"
    vocab_file = f"movie-reviews-vocab.pkl"
    X = []

    def load(self):
        """[summary]
        """
        self.data = pd.read_csv(self.fullpath(self.sample_input_path))
        print(f"\n[+] Total Movie Reviews: {len(self.data)}\n")
        self._load_x()
        self.vocab = self._load_vocab()
        self.model = self._load_model()

    def _load_x(self):
        """[summary]
        """
        # Append input reviews to X list
        for idx in range(len(self.data)):
            self.X.append(self.data['review'][idx])

    def _load_vocab(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        # Load vocabulary file; 1000 most occurence words
        with open(self.fullpath(self.vocab_file), 'rb') as fp:
            vocab = pickle.load(fp)
        return vocab

    def preprocess_string(self, s):
        """[summary]

        Args:
            s ([type]): [description]

        Returns:
            [type]: [description]
        """
        # Remove all non-word characters (everything except numbers and letters)
        s = re.sub(r"[^\w\s]", '', s)
        # Replace all runs of whitespaces with no space
        s = re.sub(r"\s+", '', s)
        # replace digits with no space
        s = re.sub(r"\d", '', s)

        return s

    def _load_model(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        # Load the LST model that's already trained
        no_layers = 2
        vocab_size = len(self.vocab) + 1  # extra 1 for padding purpose
        embedding_dim = 64
        output_dim = 1
        hidden_dim = 256
        model = MovieReviewsSentimentLSTM(
            no_layers, vocab_size, hidden_dim, embedding_dim, output_dim, drop_prob=0.5)
        model.load_state_dict(copy.deepcopy(
            torch.load(self.fullpath(self.endpoint), 'cpu')))
        model.eval()
        return model

    def padding_(self, sentences, seq_len):
        # Padding with zeros if sentence is less than required seq length
        features = np.zeros((len(sentences), seq_len), dtype=int)
        for ii, review in enumerate(sentences):
            if len(review) != 0:
                features[ii, -len(review):] = np.array(review)[:seq_len]
        return features

    def predict(self, x):
        """This function takes list of input texts. For example., ["how are you?"]

        Args:
            x (list): [input_text]

        Returns:
            final_prob_scores: [[0.98, 0.02]] 0.98 probability score represents the sentence tone is positive and 0.02 score represents   
        """
        final_prob_scores = []
        for text in x:
            word_seq = np.array([self.vocab[self.preprocess_string(word)] for word in text.split()
                                 if self.preprocess_string(word) in self.vocab.keys()])
            word_seq = np.expand_dims(word_seq, axis=0)
            pad = torch.from_numpy(self.padding_(word_seq, 500))
            inputs = pad.to('cpu')
            batch_size = 1
            h = self.model.init_hidden(batch_size)
            h = tuple([each.data for each in h])
            output, h = self.model(inputs, h)
            probability = output.item()
            final_prob_scores.append([probability, 1.0-probability])
        return final_prob_scores  # this must produce a list of class probabilities

class MovieReviewsSentimentLSTM(nn.Module):
    """pre-trained LSTM model on 25 epochs for building sentiment analysis model on IMDB movies review dataset. 
    """

    def __init__(self, no_layers, vocab_size, hidden_dim, embedding_dim, output_dim, drop_prob=0.5):
        # embedding_dim: number of expected features in the input `x`
        # hidden_dim: number of features in the hidden state `h`

        super(MovieReviewsSentimentLSTM, self).__init__()

        self.no_layers = no_layers  # number of recurrent layers
        self.vocab_size = vocab_size
        self.hidden_dim = hidden_dim  # The number of features in the hidden state h
        # embedding and LSTM layers
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.proj_size = 0
        self.output_dim = output_dim  # The size of the output you desire from your RNN
        # dropout layer
        # a Dropout layer on the outputs of each LSTM layer except the last layer, with dropout probability equal to dropout
        self.dropout = nn.Dropout(drop_prob)

        # lstm
        self.lstm = nn.LSTM(input_size=embedding_dim, hidden_size=self.hidden_dim,
                            num_layers=no_layers, batch_first=True, proj_size=self.proj_size)

        # final fully connected linear and sigmoid layer
        self.fc = nn.Linear(self.hidden_dim, self.output_dim)
        self.sig = nn.Sigmoid()

    def forward(self, x, hidden):
        """Forward process of LSTM model

        Args:
            x ([tensor]): training data/batch_first


        Returns:
            Last sigmoid output and hidden state
        """
        batch_size = x.size(0)
        # embeddings and lstm_out
        # shape: Batch x Sequence x Feature   since batch_first = True
        embeds = self.embedding(x)
        lstm_out, hidden = self.lstm(embeds, hidden)

        lstm_out = lstm_out.contiguous().view(-1, self.hidden_dim)

        # dropout and fully connected layer
        out = self.dropout(lstm_out)
        out = self.fc(out)

        # sigmoid function
        sig_out = self.sig(out)

        # reshape to be batch_size first
        sig_out = sig_out.view(batch_size, -1)

        sig_out = sig_out[:, -1]  # get last batch of labels

        return sig_out, hidden

    def init_hidden(self, batch_size, device='cpu'):
        # initialize hidden weights (h,c) to 0
        weights = next(self.parameters()).data
        h = (weights.new(self.no_layers, batch_size, self.hidden_dim).zero_().to(device),
             weights.new(self.no_layers, batch_size, self.hidden_dim).zero_().to(device))

        return h


