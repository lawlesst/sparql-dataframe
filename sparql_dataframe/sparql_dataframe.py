"""
Query a SPARQL endpoint and return results as a Pandas dataframe.
"""
from io import StringIO

import pandas as pd

from SPARQLWrapper import SPARQLWrapper, CSV, SELECT, POST, POSTDIRECTLY


class QueryException(Exception):
    pass


def get_sparql_dataframe(endpoint, query, post=False):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    if sparql.queryType != SELECT:
        raise QueryException("Only SPARQL SELECT queries are supported.")

    if post:
        sparql.setOnlyConneg(True)
        sparql.addCustomHttpHeader("Content-type", "application/sparql-query")
        sparql.addCustomHttpHeader("Accept", "text/csv")
        sparql.setMethod(POST)
        sparql.setRequestMethod(POSTDIRECTLY)

    sparql.setReturnFormat(CSV)
    results = sparql.query().convert()
    _csv = StringIO(results.decode('utf-8'))
    return pd.read_csv(_csv, sep=",")
