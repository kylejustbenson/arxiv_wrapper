## Description
This is a python wrapper for the online academic paper repository arXiv.org. Currently, most of the arXiv web API search functionality has been implemented including advanced search options and searching by ID. However, if you will be using this
for ID searches, please read the details about the id search below; there are a few subtleties. 

## Installation
If I'm not the only one that uses this, I'll make this pip-installable.

However, currently just clone this repo and extract the file to a place on your $PYTHONPATH and import normally.

You will also need to download the `feedparser` module.

`sudo pip install feedparser`

## Examples
```python
results = arxiv.search("electron")
```
Returns the first 10 results for searching 'electron' in arXiv in all categories processed into arxiv_result objects. If you wanted to download the PDF of a certain result, i, you would then...

```python
results[i].download()
```
This will download the pdf into the directory where the arxiv.py file is stored. Use the variables `filename` and `outdir` to change the name and location respectively.

Now let's utilize the `adv_search` option.
```python
results = arxiv.search("George", max_results=2, adv_search="title")
```
Returns the query for titles of articles including "George" with a max of 2 results

See the [arXiv documentation](https://arxiv.org/help/api/user-manual) for details on what else you are able to do and how to utilize the `start`, `end`, and `max_results` parameters.

Once you know what is possible, see the Advanced Search section below to get details on how to utilize `adv_search` parameter.

## Advanced Search
As I hope you've read about in the [arXiv documentation](https://arxiv.org/help/api/user-manual), you are able to utilize more advanced queries. To specify these in your search, send the `adv_search` parameter easily allows you to do this. Below is a list of the possible values for `adv_search`:

* all
	- Searches for `query` in all of arXiv
* title
	- Searches for `query` in publication titles
* author
	- Searches for `query` in authors of publications
* abstract
	- Searches for `query` in abstract of publications
* comment
	- Searches for `query` in arXiv comment metadata
* journal
	- Searches for `query` in publications to journal
* category
	- Searches for `query` in category of paper
* report
	- Searches for `query` in report of paper
* id
	- See id search notes below

### id Search
Using the `adv_search` option 'id' you can either send a single id in the form of a string, or you can send a list of string ids through the query parameter.

```python
results = search(['hep-th/0012018', 'hep-th/9901023'])
```
Returns the metadata for the two papers specified by those ids. 

Take notice of that format for ids! arXiv ids are unique to each category rather than the enture archive itself. So make sure when doing id searches, you include the category of the paper.

## Summary of arXiv metadata when parsed with feedparser

Letting data = (feedparser.parse(url))

data['entries'] = List of parsed metadata for each paper returned by query

Used fields:
* data['entries'][i]['arxiv_affiliation']
	- affiliation of authors (string)
* data['entries'][i]['title']
 	- title of article (string)
* data['entries'][i]['summary']
 	- article abstract (string)
* data['entries'][i]['authors]
 	- list of authors (list of dictionaries [ {'name' : name1},...]
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
	
Unused fields:
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
