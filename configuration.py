import lucene
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
import jieba

from org.apache.lucene.search.highlight import Formatter
from org.apache.lucene.search.highlight import Fragmenter
from org.apache.lucene.search.highlight import Highlighter
from org.apache.lucene.search.highlight import InvalidTokenOffsetsException
from org.apache.lucene.search.highlight import QueryScorer
from org.apache.lucene.search.highlight import SimpleFragmenter
from org.apache.lucene.search.highlight import SimpleHTMLFormatter
from org.apache.lucene.search.highlight import SimpleSpanFragmenter
from org.apache.lucene.search.highlight import TokenSources

import sys

reload(sys)
sys.setdefaultencoding('utf8')

vm_env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])

stopwords = ""
with open("INDEX/stop.txt") as sws:
    for sw in sws:
        sw = sw.decode("gbk")[:-3]
        stopwords += sw
