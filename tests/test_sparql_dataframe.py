"""
Test cases for sparql_dataframe.

Requires connecting to http://dbpedia.org/sparql.

"""

from unittest import TestCase

import sparql_dataframe
import SPARQLWrapper


endpoint = "http://dbpedia.org/sparql"

class TestQuery(TestCase):

    def test_get_integer(self):
        q = """
    SELECT DISTINCT ?wikiPageID
    WHERE {
    <http://dbpedia.org/resource/Baseball> rdfs:label ?label ;
         <http://dbpedia.org/ontology/wikiPageID> ?wikiPageID
    }
"""
        df = sparql_dataframe.get(endpoint, q)
        self.assertEqual(df['wikiPageID'].iloc[0], 3850)

    def test_get_multiple(self):
        q = """
    SELECT ?label ?wikiPageID
    WHERE {
    <http://dbpedia.org/resource/Baseball> rdfs:label ?label ;
         <http://dbpedia.org/ontology/wikiPageID> ?wikiPageID
    }
"""
        df = sparql_dataframe.get(endpoint, q)
        # Make sure we get 5 or more labels.
        self.assertTrue(len(df) > 5)
        # Both variables should be of equal length.
        self.assertEqual(len(df['label']), len(df['wikiPageID']))


    def test_bad_query(self):
        with self.assertRaises(SPARQLWrapper.SPARQLExceptions.QueryBadFormed):
            df = sparql_dataframe.get(endpoint, "SELECT ?label FROM {}")

    def test_construct_query(self):
        q = """
    CONSTRUCT { v:tmp rdfs:label ?label }
    WHERE {
    <http://dbpedia.org/resource/Baseball> rdfs:label ?label ;
         <http://dbpedia.org/ontology/wikiPageID> ?wikiPageID
    }
        """
        with self.assertRaises(sparql_dataframe.QueryException):
            df = sparql_dataframe.get(endpoint, q)


if __name__ == '__main__':
    unittest.main()
