#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from string import punctuation


# In[2]:


punctuation += ' '


# In[3]:


filename = r"C:\Users\Иннокентий\Downloads\dev.tsv"


# In[4]:


sep='>'


kiche_anbur = "a [a], ä [ə], e [ɛ], i [i], o [o], u [u], m [m], n [n], nh [ŋ], p [p], bʼ [ɓ], t [t], tʼ [tʼ], k [k], kʼ [kʼ], q [q], qʼ [qʼ], tz [ʦ], tzʼ [ʦ’], ch [ʧ], chʼ [ʧ’], s [s], x [ʃ], j [χ], h [h], r [r], l [l], y [j], w [w], ʼ [ʔ]"
alphabet = []
for letter in kiche_anbur.split(","):
    letter = letter.split()[0]
    alphabet.append(letter)
    alphabet.append(letter[0].upper() + letter[1:])


alph_to_int = dict(zip(alphabet, range(len(alphabet))))
int_to_alph = dict(zip(range(len(alphabet)), alphabet))


# In[10]:


def window(text, size):
    tokens = []
    i = 0
    while i < (len(text)-size+1):
        try:
            current = ''.join(text[i:i+size])
        except:
            current = 'not_in_alphabet'
        if current in alphabet:
            tokens.append(alph_to_int[current])
            i += size
        else:
            tokens.append(text[i])
            i += 1
    return tokens


# In[11]:


def tokenize(text):
    tokens = list(text + 'ггг')
    for i in range(3, 0, -1):
        tokens = window(tokens, i)
    tokens_2 = []
    for token in tokens:
        if token in int_to_alph:
            token = int_to_alph[token]
        tokens_2.append(token)
    return tokens_2


# In[12]:


def tokenize_simple(text):
    return(list(text))


# In[13]:


#sep — c разделителем, not — без разделителя
#b, m и s значат beginning, middle и end, а s — single
def to_labels(tokens):
    border_tokens = sep + punctuation
    labels = []
    tokens = [sep] + tokens + [sep]
    for i in range(1, len(tokens)-1):
        current = tokens[i]
        previous = tokens[i-1]
        next_ = tokens[i+1]
        if current != sep:
            if current not in punctuation:
                if previous in border_tokens:
                    if next_ in border_tokens:
                        labels.append('s-morph') #labels.append('sep')
                    else:
                        labels.append('b-morph') #labels.append('not')
                elif next_ in border_tokens:
                    labels.append('e-morph') #labels.append('sep')
                else:
                    labels.append('m-morph') #labels.append('not')
            else:
                labels.append(current) #labels.append('punct')
    return labels


def tokenize_df(df, text='text', with_sep='with_sep'):


    df['tokens_with_sep'] = df[with_sep].apply(tokenize)

    df['tokens'] = df['tokens_with_sep'].apply(lambda array: list(filter(lambda x: x!=sep, array)))


    df['tokens_honest'] = df[text].apply(tokenize)


    df['tokens_simple'] = df[text].apply(tokenize_simple)


    df['tokens_simple_with_sep'] = df[with_sep].apply(tokenize_simple)

    #df['labels'] = df['tokens_simple_with_sep'].apply(to_labels)
    df['labels'] = df['tokens_with_sep'].apply(to_labels)


