# sparql-dataframe

Helper to convert [SPARQLWrapper](https://github.com/RDFLib/sparqlwrapper) results to [Pandas](https://pandas.pydata.org/) [dataframes](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html).

```
import sparql_dataframe

endpoint = "http://dbpedia.org/sparql"

df = sparql_dataframe.get(endpoint, q)
...
```


## Tests

```
$ python -m unittest
```
