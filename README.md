## Details for advanced search

(adv_search="" values)
The arXiv API allows for these advances search terms:
* (acronym) - (description)
* 'ti' - title
* 'au' - Author
* 'abs' - Abstract
* 'co' - Comment
* 'jr' - Journal Reference
* 'cat' - Subject Category
* 'rn' - Report Number
* 'id' - ID (can use id_list instead)

Example use:

papers = search(query="Foo Bar", adv_search="title")

will return a list of arxiv_paper objects from searching for articles with the
name 'Foo Bar'

## arXiv metadata when parsed with feedparser

Letting data = (feedparser.parse(url))

data['entries'] = List of parsed metadata for each paper returned by query

Contains fields:
* data['entries'][i]['arxiv_affiliation']
 * affiliation of authors (string)
* data['entries'][i]['title']
 * title of article (string)
* data['entries'][i]['summary']
 * article abstract (string)
* data['entries'][i]['authors]
 * list of authors (list of dictionaries [ {'name' : name1},...]
* data['entries'][i]['links']
 * list of other links including pdf download link
* data['entries'][i]['id']
 * url to paper on arXiv website
* data['entries'][i]['updated_parsed']
 * date article was last updated
 * time.struct_time parsed 'updated'
* data['entries'][i]['published_parsed']
 * date published
 * time.struct_time parsed 'published'
* data['entries'][i]['arxiv_primary_category']
 * category article was published under
* data['entries'][i]['arxiv_journal_ref']
 * journal paper was submitted to
* data['entries'][i]['arxiv_comment']
 * information about article (#pages, #tables, etc)
	
Useless fields:
* data['entries'][i]['author_detail']
* data['entries'][i]['guidislink']
* data['entries'][i]['title_detail']
* data['entries'][i]['summary_detail']
* data['entries'][i]['author']
* data['entries'][i]['link'] (same as 'id')
 * link to article on arXiv website
* data['entries'][i]['tags']
 * list of tags (list of dictionaries)
* data['entries'][i]['updated']
 * date of when the article was last updated
* data['entries'][i]['published']
 * date published
