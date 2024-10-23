# sparql-dataframe

Helper to convert [SPARQLWrapper](https://github.com/RDFLib/sparqlwrapper) results to [Pandas](https://pandas.pydata.org/) [dataframes](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html).

> Update 10/23/2024 - this library is no longer maintained. SPARQL to dataframe functionality has been added directly to [SPARQLWrapper](https://github.com/RDFLib/sparqlwrapper/blob/master/SPARQLWrapper/sparql_dataframe.py). Please try that library.


See this [blog post](http://lawlesst.github.io/notebook/sparql-dataframe.html) for examples. You might also be interested in these related examples from [Su Labs tutorial](https://github.com/SuLab/sparql_to_pandas/blob/master/SPARQL_pandas.ipynb).

## Install

Directly from [PyPi](https://pypi.org/project/sparql-dataframe/) for Python 3.4+.

```
$ pip install sparql-dataframe
```

From Github. This should support Python 2.7 as well.

```
$ pip install git+https://github.com/lawlesst/sparql-dataframe.git
```

## Usage

```
import sparql_dataframe

endpoint = "http://dbpedia.org/sparql"

q = """
    SELECT ?label ?wikiPageID
    WHERE {
    <http://dbpedia.org/resource/Baseball> rdfs:label ?label ;
         <http://dbpedia.org/ontology/wikiPageID> ?wikiPageID
    }
"""

df = sparql_dataframe.get(endpoint, q)
...
```

By default, the query will be passed to the server as a `GET` request. To pass the query to the server as a `POST` request, use the `post=True` keyword.

```
df = sparql_dataframe.get(endpoint, q, post=True)
```

## Tests

```
$ python -m unittest
```


