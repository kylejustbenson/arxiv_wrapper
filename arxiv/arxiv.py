import feedparser
import os

###############################################################################
# Ways to improve
#   - byte buffer the files so they're not loaded to memory
#   - better error handling

class arxiv_paper:
    def __init__(self, entry):
        """
        Parsing metadata from arXiv search into object

        entry   - element from feedparser.parse(url)['entries']
        """

        self.title = ""
        self.abstract = ""
        self.authors = []
        self.link = ""
        self.id = ""
        self.category = ""
        self.journal = ""
        self.details = ""
        self.download_link = ""

        # Used to cleanup the conversion to ascii below
        to_ascii = lambda x: x.encode('ascii', 'replace')

        if entry.get('title'):
            self.title = to_ascii(entry['title'])
        if entry.get('summary'):
            self.abstract = to_ascii(entry['summary'])
        if entry.get('id'):
            self.link = to_ascii(entry['id'])
            self.id = self.link.split('/')[-1]
        if entry.get('arxiv_primary_category'):
            self.category = to_ascii(entry['arxiv_primary_category']['term'])
        if entry.get('arxiv_journal_ref'):
            self.journal = to_ascii(entry['arxiv_journal_ref'])
        if entry.get('arxiv_comment'):
            self.details = to_ascii(entry['arxiv_comment'])

        self.authors = [ to_ascii(info['name']) for info in entry['authors'] ]

        # Finding link to pdf for downloading purposes
        for link in entry['links']:
            if link['type'] == u'application/pdf':
                self.download_link = to_ascii(link['href'])

        # If link exists, parse it to where you can actually download it.
        # Original format wasn't working
        if self.download_link:
            self.download_link = "https" + self.download_link[4:]
            self.download_link += ".pdf"


    def download(self, filename = None, outdir = None):
        """
        Downloads paper to outdir with name filename

        outdir      - output directory
        filename    - what to name file (include the file extension)
        """
        # If no name given, default is paper id + .pdf
        if not filename:
            filename = self.download_link.split('/')[-1]

        # If no directory given, output to directory of executing file
        if not outdir:
            outdir = os.path.dirname(os.path.abspath( __file__ ))

        import urllib2

        data = urllib2.urlopen(self.download_link)
        fullpath = os.path.join(outdir, filename)

        # This currently loads entire file to memory. If this becomes a
        #   problem, we may want to buffer the file
        with open( fullpath, 'wb' ) as f:
            f.write( data.read() )

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.__str__()

def search(query, start=0, end=None, max_results=10, adv_search="all"):
    """
    Fills html query for arXiv.org search API

    query           - search query
                        * string or list of strings if multiple ID query
    start           - index of found results to start at
    end             - index of found results to end at
    max_results     - Max number of results to return
    adv_search      - see README

    returns list of arxiv_papers
    """

    advanced_map = { "all" : "all",
                     "title" : "ti",
                     "author": "au",
                     "abstract" : "abs",
                     "comment" : "co",
                     "journal" : "jr",
                     "category" : "cat",
                     "report" : "rn",
                     "id" : "id"}

    adv_search = advanced_map.get(adv_search)

    # Returns null if no valid search is given
    if not adv_search:
        print "Invalid 'adv_search' option."
        return None


    # If end result not given, default to start + max_results
    if not end:
        end = start + max_results

    # The ID must be section/id# for this to work
    if adv_search == "id":
        # id query is either a single string or list of string ids
        if type(query) == list:
            max_results = len(query)
            query = ",".join(query)

        q = "http://export.arxiv.org/api/query?"\
                "id_list=%s&max_results=%d"%(query, max_results)
    # Non-ID query
    else:
        q = "http://export.arxiv.org/api/query?"\
            "search_query=%s:%s&start=%d&end=%d&max_results=%d"%(adv_search,
                                                                  query,
                                                                  start,
                                                                  end,
                                                                  max_results)

    data = feedparser.parse(q)

    papers = []
    for entry in data['entries']:
        papers.append( arxiv_paper(entry) )

    return papers
