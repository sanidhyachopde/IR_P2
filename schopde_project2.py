import sys
from io import StringIO

fu = StringIO()

def input():
    with open("/Users/sanidhya/Downloads/input_corpus (1).txt", "r", encoding="utf8") as d:
        f = d.readlines()
        MyDictionary = {}
        for x in f:
            line = x.split()
            docID = line[0]
            line = line[1:]
            for l in line:
                if l not in MyDictionary:
                    MyDictionary[l] = []
                    MyDictionary[l].append(docID)
                else:
                    if docID not in MyDictionary[l]:
                        MyDictionary[l].append(docID)
    return MyDictionary


def read_input(corpus, output, query):
    with open(query, "r", encoding="utf8") as g:
        file = g.readlines()
        for w in file:
            main_list = []
            lines = w.split()
            for words in lines:
                main_list.append(words)
            printing_results(main_list, w, corpus)
            print(file=fu)


def printing_results(list, word, corpus):
    list = sorted(list, reverse=True)
    MyDictionary = input()
    for i in list:
        print("GetPostings",file=fu)
        print(i)
        print("Postings list: ",end = '',file= fu)
        print(' '.join(MyDictionary[i]),file= fu)
        result_and = MyDictionary[list[0]]
        result_or = MyDictionary[list[0]]
        comparision_count_and = 0
        comparision_count_or = 0
        orresult_final = []
        result_dict = {}
        j = 0
    while j < len(list)-1:
        result,comparision_count_1 = compareAnd(result_and, MyDictionary[list[j+1]])

        orresult,comparision_count_2 = compareOr(result_or,MyDictionary[list[j+1]])

        comparision_count_and = comparision_count_and + comparision_count_1
        comparision_count_or = comparision_count_or + comparision_count_2
        result_and = result
        for o in orresult:
            if o not in orresult_final:
                orresult_final.append(o)
        j = j+1

    temp,doc_count = TFIDF_Corpus(corpus)
    temp2 = TFIDF_Input(corpus)
    for doc in result:
        tfidfresult = 0
        for term in list:
            if doc in temp:
                term_freq = temp[term][doc]
                total_terms_in_doc = int(temp2[doc])
                docs_with_term = len(temp[term])
                tf = term_freq/total_terms_in_doc
                idf = doc_count/docs_with_term
                tfidf = tf * idf
                tfidfresult += tfidf
        result_dict[doc] = tfidfresult
    result_tfidf = sorted(result_dict.items(), key=lambda kv: kv[1],reverse=True)


    temp,doc_count = TFIDF_Corpus(corpus)
    temp2 = TFIDF_Input(corpus)
    for doc in orresult_final:
        tfidfresult_or = 0
        for term in list:
            if doc in temp[term]:
                term_freq = temp[term][doc]
                total_terms_in_doc = int(temp2[doc])
                docs_with_term = len(temp[term])
                tf = term_freq/total_terms_in_doc
                idf = doc_count/docs_with_term
                tfidf = tf * idf
                tfidfresult_or += tfidf
        result_dict[doc] = tfidfresult_or
    result_tfidf_or = sorted(result_dict.items(), key=lambda kv: kv[1],reverse=True)

    print("DaatAnd",file= fu)
    print(word, end='',file= fu)
    if not result:
        print("Results: empty",file= fu)
    else:
        print("Results: ", end='',file= fu)
        print(' '.join(result),file= fu)
    print("Number of documents in results: {}".format(len(result)),file= fu)
    print("Number of comparisons: {}".format(comparision_count_and),file= fu)
    print("TF-IDF",file= fu)
    print("Results: ",end='',file= fu)
    if not result:
        print("empty",file= fu)
    else:
        for things in result_tfidf:
            print(things[0],end =' ',file= fu)
    print("DaatOr",file= fu)
    print(word, end='',file= fu)
    if not orresult_final:
        print("Results: empty",file= fu)
    else:
        print("Results: "+' '.join(orresult_final),file= fu)
    print("Number of documents in results: {}".format(len(orresult_final)),file= fu)
    print("Number of comparisons: {}".format(comparision_count_or),file= fu)
    print("TF-IDF",file= fu)
    print("Results: ",end="",file= fu)
    if not orresult_final:
        print("empty",file= fu)
    else:
        for things in result_tfidf_or:
            print(things[0],end =' ',file= fu)
    print(" ",file= fu)


def compareAnd(a, b):
    i = 0
    j = 0
    result_array = []
    comparision_count = 0
    while i < len(a) and j < len(b):
        comparision_count = comparision_count + 1
        if a[i] == b[j]:
            result_array.append(a[i])
            i = i + 1
            j = j + 1
        elif a[i] > b[j]:
            j = j + 1
        elif a[i] < b[j]:
            i = i + 1

    return result_array,comparision_count


def compareOr(a, b):
    i = 0
    j = 0
    result_array = []
    comparision_count = 0
    while i < len(a) and j < len(b):
        comparision_count = comparision_count + 1
        if a[i] == b[j]:
            if a[i] not in result_array:
                result_array.append(a[i])
            i = i + 1
            j = j + 1
        elif a[i] > b[j]:
            result_array.append(b[j])
            j = j + 1
        elif a[i] < b[j]:
            result_array.append(a[i])
            i = i + 1

    while i < len(a):
        comparision_count = comparision_count + 1
        if a[i] not in result_array:
            result_array.append(a[i])
            i = i + 1
    while j < len(b):
        comparision_count = comparision_count + 1
        if b[j] not in result_array:
            result_array.append(b[j])
            j = j + 1
    return result_array,comparision_count


def TFIDF_Corpus(filename):
    TFIDF_Dictionary = {}
    doc_count = 0
    with open(filename, "r", encoding="utf8") as m:
        file = m.readlines()
        for w in file:
            doc_count += 1
            lines = w.split()
            doc_id = lines[0]
            lines = lines[1:]
            for l in lines:
                if l not in TFIDF_Dictionary:
                    TFIDF_Dictionary[l] = {}
                    TFIDF_Dictionary[l][doc_id] = 1
                else:
                    if doc_id in TFIDF_Dictionary[l]:
                        TFIDF_Dictionary[l][doc_id] += 1
                    else:
                        TFIDF_Dictionary[l][doc_id] = 1
    return TFIDF_Dictionary,doc_count


def TFIDF_Input(filename):
    dict = {}
    with open(filename, "r", encoding="utf8") as m:
        file = m.readlines()
        for w in file:
            lines = w.split()
            doc_id = lines[0]
            lines = lines[1:]
            if doc_id not in dict:
                dict[doc_id] = len(lines)
    return dict


def tf(term_in_doc_freq, total_terms_in_doc):
    tf = term_in_doc_freq/total_terms_in_doc
    return tf


def idf(total_docs, docs_with_term):
    idf = total_docs/docs_with_term
    return idf


def calculate_tfidf(resultarray,filename, term):
    temp,doc_count = TFIDF_Corpus(filename)
    temp2 = TFIDF_Input(filename)
    for doc in resultarray:
        term_freq = temp[term][doc]
        total_terms_in_doc = temp2[doc]
        docs_with_term = len(temp[term])
        tf = term_freq/total_terms_in_doc
        idf = doc_count/docs_with_term
        tfidf = tf * idf
    return tfidf,doc


# corpus_file = sys.argv[1]
# output_file = sys.argv[2]
# query_file = sys.argv[3]
corpus_file = "/Users/sanidhya/Downloads/input_corpus (1).txt"
output_file = ""
query_file = "/Users/sanidhya/Downloads/Project2_Sample_input.txt"
read_input(corpus_file,output_file,query_file)
print(fu.getvalue())
# with open(output_file,'w') as fopen:
#     fopen.write(fu.getvalue())

