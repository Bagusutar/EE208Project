#!/usr/bin/env python
# -*- coding:utf-8 -*-

INDEX_DIR = 'INDEX'

from configuration import *

"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""


def parseTerm(term):
    # Get a dict of keywords
    term_dict = {}
    opt = 'contents'
    for i in str(term).split(' '):
        term_dict[opt] = term_dict.get(opt, '') + ' ' + i
    term = jieba.cut(term_dict.get("contents", ''))
    term = [i for i in term if i not in stopwords]
    term_dict["contents"] = " ".join(term)
    return term_dict


def search(root, term, maxNum=50):
    """
    :param root: choose 'music', 'lyrics', 'album' or 'artist'
    :param term: the keyword you want to search
    :return: a list of results; the number of results
    """
    # Initialize the searcher
    vm_env.attachCurrentThread()
    directory = SimpleFSDirectory(File("{}/{}_index".format(INDEX_DIR, root)))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)

    # If the input is blank, return an empty list.
    if term == '':
        return [], 0

    # Get the keyword dict
    term_dict = parseTerm(term)

    # Start searching in the index directory
    querys = BooleanQuery()
    for k, v in term_dict.iteritems():
        query = QueryParser(Version.LUCENE_CURRENT, k,
                            analyzer).parse(v)
        querys.add(query, BooleanClause.Occur.MUST)

    # Get the results
    scoreDocs = searcher.search(querys, maxNum).scoreDocs

    # Store the results
    contents = []
    if root == 'lyrics':
        htmlFormatter = SimpleHTMLFormatter("<span style='color:red;'>", "</span>")
        highlighter = Highlighter(htmlFormatter, QueryScorer(querys))
        highlighter.setTextFragmenter(SimpleFragmenter(200000000))

    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        if root is 'music' or root is 'lyrics':
            song_id = doc.get("song_id")
            song_name = doc.get("song_name")
            artist_link = doc.get("artist_link")
            artist_name = doc.get("artist_name")
            album_link = doc.get("album_link")
            album_name = doc.get("album_name")
            img_link = doc.get("img_link")
            lyrics = doc.get("lyrics")
            if root=='lyrics':
                tokenStream = TokenSources.getAnyTokenStream(searcher.getIndexReader(), scoreDoc.doc, "lyrics",
                                                             analyzer)
                frag = highlighter.getBestTextFragments(tokenStream,lyrics, False, 1)
                lyrics = frag[0].toString()
            # i=lyrics.split('\n')
            # for k in i:
            #     print k
            contents.append([song_id, song_name, album_link, album_name, artist_link, artist_name, img_link,
                             lyrics])
        if root is 'album':
            album_id = doc.get('album_id')
            album_name = doc.get('album_name')
            artist_link = doc.get('artist_link')
            artist_name = doc.get('artist_name')
            img_link = doc.get('img_link')
            contents.append([album_id, album_name, artist_link, artist_name, img_link])

        if root is 'artist':
            artist_id = doc.get('artist_id')
            artist_name = doc.get('artist_name')
            img_link = doc.get('img_link')
            contents.append([artist_id, artist_name, img_link])

    # Delete the searcher
    del searcher

    return contents, len(contents)

"""
# example:
# results, num = search('music', "吻")
results, num = search('lyrics', "悠长")
# results, num = search('album', "世界")
# results, num = search('artist', "蔡健雅")
for result in results:
    # music(lyrics): song_id, song_name, album_link, album_name, artist_link, artist_name, img_link, lyrics
    # artist: artist_id, artist_name, img_link
    # album: album_id, album_name, artist_link, artist_name, img_link
    result = " | ".join(result)
    print result
    print "-" * 150
print "Total:", num
"""