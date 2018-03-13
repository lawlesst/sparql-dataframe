"""
Query a SPARQL endpoint and return results as a Pandas dataframe.
"""

import pandas as pd

from SPARQLWrapper import SPARQLWrapper, CSV, SELECT


class QueryException(Exception):
    pass


def get_sparql_dataframe(endpoint, query):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    if sparql.queryType != SELECT:
        raise QueryException("Only SPARQL SELECT queries are supported.")
    sparql.setReturnFormat(CSV)
    results = sparql.query().convert()
    _csv = pd.compat.StringIO(results.decode('utf-8'))
    return pd.read_csv(_csv, sep=",")
