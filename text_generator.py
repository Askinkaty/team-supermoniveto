import os
import numpy as np
from keras.preprocessing import sequence


"""
Function for reading files into batches during training: text_generator(). The function returns a generator
which yelds data vectors and tag vectors by batches. For details of using keras.fit_generator see
keras.fit_generator here https://keras.io/models/sequential/
"""

def iter_window(iterable, size):
    it = iter(iterable)
    while True:
        result = []
        try:
            for _ in range(size):
                n = next(it)
                result.append(n)
            yield result
        except StopIteration:
            if len(result) > 0:
                yield result
            break


def read_file_batch(n_class, max_text_length, corpus_path, file_batch, data_cache=None, bag_of_words=False,
                    dict_size=None):
    data_path = corpus_path + 'vectorized/'
    tag_path = corpus_path + 'tags/'
    data_rows = []
    tag_rows = []

    n_row = len(file_batch)
    if bag_of_words:
        data_matrix = np.zeros((n_row, dict_size), dtype=np.int32)

    c = 0
    for f in file_batch:
        if data_cache:
            data = data_cache['data'][f]
            if bag_of_words:
                data_matrix[c, list(data)] = 1
                c += 1
            else:
                data = sequence.pad_sequences([data], maxlen=max_text_length,
                                              padding='post')
        else:
            data = np.load(data_path + f)
            if bag_of_words:
                data_matrix[c, list(data)] = 1
                c += 1
            else:
                data = sequence.pad_sequences([data], maxlen=max_text_length, padding='post')
        data_rows.append(data)

        if data_cache:
            tags = data_cache['tags'][f]
        else:
            tags = np.load(tag_path + f)

        tag_rows.append(tags)

    n_rows = len(tag_rows)

    if not bag_of_words:
        data_matrix = np.vstack(data_rows)
    tags_matrix = np.zeros((n_rows, n_class))
    for ii in range(n_rows):
        tags_matrix[ii, list(tag_rows[ii])] = 1
    return data_matrix, tags_matrix


def text_generator(batch_size, n_class, max_text_length, corpus_path, files_to_use, data_cache=None, bag_of_words=False,
                   dict_size=None):
    while True:
        for file_batch in iter_window(files_to_use, batch_size):
            data_matrix, tags_matrix = read_file_batch(n_class, max_text_length, corpus_path, file_batch, data_cache,
                                                       bag_of_words, dict_size)
            yield (data_matrix, tags_matrix)
    pass


def text_generator_test(batch_size, max_text_length, database_path, files_to_use, bag_of_words = False, dict_size = None):
    while True:
        for file_batch in iter_window(files_to_use, batch_size):
            data_matrix = read_test_batch(max_text_length, database_path, bag_of_words, dict_size, file_batch)
            yield data_matrix
    pass


def read_test_batch(max_text_length, database_path = 'test/', bag_of_words = False, dict_size = None, batch = None):
    vectorized_path = database_path + 'REUTERS_CORPUS_2/vectorized/'
    if batch:
        file_batch = batch
    else:
        file_batch = os.listdir(vectorized_path)
        file_batch.sort()

    data_rows = []

    n_row = len(file_batch)
    if bag_of_words:
        data_matrix = np.zeros((n_row, dict_size), dtype = np.int32)
    
    for c, f in enumerate(file_batch):
        data = np.load(vectorized_path + f)
        if bag_of_words:
            data_matrix[c, list(data)] = 1
        else:
            data = sequence.pad_sequences([data], maxlen=max_text_length, padding='post')
        data_rows.append(data)
    
    if not bag_of_words:
        data_matrix = np.vstack(data_rows)
    return data_matrix


def read_tag_batch(n_class, corpus_path, file_batch, data_cache = None):
    tag_path = corpus_path + 'tags/'
    tag_rows = []
    for f in file_batch:
        if data_cache:
            tags = data_cache['tags'][f]
        else:
            tags = np.load(tag_path + f)
        tag_rows.append(tags)
    
    n_rows = len(tag_rows)
    tags_matrix = np.zeros((n_rows, n_class))
    for i in range(n_rows):
        tags_matrix[i, list(tag_rows[i])] = 1
    return tags_matrix            



if __name__== '__main__':
    corpus_path = "train/REUTERS_CORPUS_2/"
    files_to_use = os.listdir(corpus_path + "vectorized/")
    g = text_generator(5, 126, 300, corpus_path, files_to_use)
    print(next(g))
    pass
