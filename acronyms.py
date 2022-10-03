# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 18:17:55 2019

@author: Rafael C. Carrasco
"""

import sys


class Vocabulary(set):
    """
    The set of words which are valid acronyms

    """
    
    def __init__(self, filename):
        """ 
        Parameters
        ----------
        filename : str
            the name of the file containing the words (one per line)

        """
        with open(filename, 'r') as f:
            for w in f:
                self.add(w.strip().upper())



class Title(str):
    """
    A Title is a string containing tokens 
    (tokes are maximal segments of non-blak characters)
    """
    def __new__(cls, content, case_sensitive=True):
        # merge runs of consecutive whitespaces into a single one
        reduced = ' '.join(content.split())
        if case_sensitive:
            return super().__new__(cls, reduced)
            str.__init__(reduced)
        else:
            return super().__new__(cls, reduced.upper())
        
   
    """
    Parameters
    ----------
    case_sensitive (bool):
        
    """
    def __init__(self, content, case_sensitive=True):
        """
        

        Parameters
        ----------
        content : str
            a project title.
        case_sensitive : bool, optional
            if True, only uppercase characters in content can be selected for 
            the acronym. For example, in 'First PLAN' only F, P, L, A, and N 
            can be selected. The default is True.


        """
        self._tokens = self.split()

        # map every position in the title to the number of preceding blanks (tokens) 
        self._token_number = {n:self[:n].count(' ') for n in range(len(self)) if self[n] != ' '}

    

    def tokens(self):
        """
        Returns
        -------
         list of str
             tokens in this title.
             
        """
        return self._tokens
    
  
  
    def token_number(self, pos):
        """
        Returns
        -------
        token number for the specified position in the title
    
        """
        return self._token_number[pos]
    
    def contains(self, word):
        """
        Parameters
        ----------
        word : str
            any word.

        Returns
        -------
        bool
            True if the word is a subsequence of this Title, that is,
            word is the result of removing some characters (or none) in the Title

        """
        n = -1
        for c in word:
            n = self.find(c, n + 1) 
            if n < 0:
                return False
        
        return True
    
    
    def all_alignments(self, word):
        """
        Parameters
        ----------
        word : str
            any word
            
        Returns
        -------
        set of tuples
         set of all possible alignments between the word and the title.
         For word w_1....w_N of length N, 
         an aligment is an N-tuple a = (a_1, a_2, .., a_N) 
         such that a_1 < a_2 < ... < a_N and word[k] = title[a_k] for all k. 
         For example, if word = 'AB' and title = 'ABAB', the alignments are
         {(0, 1), (0, 3), (2, 3)}.

        """
        A = [list(), list()]
        wsize = len(word)
        tsize = len(self)
        for j in range(1 + tsize):
            A[0].append(set())
        
        for i in range(1, 1 + wsize):
            A[i % 2] = [set()]
            for j in range(1, 1 + tsize):
                a = A[i%2][j - 1].copy()
                A[i % 2].append(a)
                if word[i - 1] == self[j - 1]: # add j - 1 to the tuples
                    A[i % 2][j].add((j - 1,)) 
                    for a in A[(i - 1) % 2][j - 1]:
                        A[i % 2][j].add(a + (j - 1,))
            
        # return only full aligments (word is exhausted and all chars matched)
        return set(a for a in A[wsize % 2][-1] if len(a) == len(word))
    

"""             
 Demo
 If case sensitive, only uppercase characters are matched
 For example, in 'First PLAN' only the F, P, L, A, and N can be selected.
 
"""

try:
    case_sensitive = '-i' not in sys.argv
except IndexError:
    case_sensitive = True
try:
    title = Title(sys.argv[1], case_sensitive) 
except IndexError:
    title = Title('Platform for OPEN DATA ACCESS in DIGITAL HUMANITIES RESEARCH', True)
    
words = Vocabulary('input/en_words.txt')
print("lexicon has", len(words), 'words')

# stopwords can be optionally matched (not match is required)
stopwords = Vocabulary('input/en_stopwords.txt')
lowercase = {token for token in title.tokens() if token.islower()}

# terms in title which do not need to be matched
ignore = {n for n, token in enumerate(title.tokens()) if token.upper() in stopwords|lowercase}

for word in sorted(words):
    if title.contains(word):
        alignments = title.all_alignments(word)
        for a in alignments:
            matched = {title.token_number(pos) for pos in a}
            if len(ignore | matched) == len(title.tokens()):
                res = [c.upper() if n in a else c.lower() for n, c in enumerate(title)]
                print(word, ': ', ''.join(res))
                break
           
