
import numpy, copy

class DistanceReader(object):
    def __init__ (self, distance_file, word_set = set()):
        """ word_set is used to limit the list of vectors being loaded 
        to a limited set of words for memory efficiency. If not used,
        the whole set of vectors will be loaded.

        This function loads a dictionary self.vocab_hash 

               key: word, value: distance vector

        """
        
        self.distance_file = distance_file
        self.is_loadall = len(word_set) == 0

        with open(distance_file, 'rb') as fin:
            header = fin.readline()
            vocab_size, vector_size = list(map(int, header.split()))
            vocab = numpy.empty(vocab_size, dtype='<U%s' % 78)
            vectors = numpy.empty((vocab_size, vector_size), dtype=numpy.float)
            binary_len = numpy.dtype(numpy.float32).itemsize * vector_size
            for i in range(vocab_size):
                word = b''
                while True:
                    ch = fin.read(1)
                    if ch == b' ':
                        break
                    word += ch
                vector = numpy.fromstring(fin.read(binary_len), dtype=numpy.float32)
                if self.is_loadall or (word in word_set):
                    vocab[i] = word.decode("utf-8")
                    vectors[i] = (1.0 / numpy.linalg.norm(vector, ord=2)) * vector
                fin.read(1)
    
        vectors = vectors[vocab != '', :]
        vocab = vocab[vocab != '']
        vocab_hash = {}
        for i, word in enumerate(vocab):
            vocab_hash[word] = vectors[i]
            
        self.vocab_hash = vocab_hash
    
    def get_distance(self, pairs):
        d = {}
        not_found = []
        for (word1, word2) in pairs:
            dist = self.get_distance_pair(self, word1, word2)
            if dist == None:
    	        not_found.append( (word1, word2) )
    	    else:
    	        d[(word1,word2)] = dist
        return d, not_found

    def get_distance_pair(self, word1, word2):
        if word1 not in self.vocab_hash or word2 not in self.vocab_hash:
            return None
    	elif word1 == word2:
    	    return 1.0
    	else:
    	    return numpy.dot(self.vocab_hash[word1], self.vocab_hash[word2])

    def get_distance_withvector(self, word, vector):
        if word not in self.vocab_hash:
            return None
    	else:
    	    return numpy.dot(self.vocab_hash[word], vector)
        
    def get_vector(self, word):
        if word in self.vocab_hash:
            return copy.copy( self.vocab_hash[word] )
        else:
            return None
        
    def get_centroid(self, word_list, weights):
        ## assume weights are already normalized
        ## multiply vectors with weights
        vectors = []
        for i,word in enumerate(word_list):
            ##create a copy of the vector
            if word in self.vocab_hash:
                vectors.append ( copy.copy(self.vocab_hash[word]) * weights[i] )
        if len(vectors) > 0:
            return numpy.average(vectors, axis=0)
        else:
            ## duct tape for now to not have to check errors in the code
            ## nothing is found, then return the least contentful vector
            return copy.copy(self.vocab_hash['the'])

    
            
