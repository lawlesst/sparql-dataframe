"""
Test cases for sparql_dataframe.

Requires connecting to http://dbpedia.org/sparql.

"""

from unittest import TestCase

import sparql_dataframe
import SPARQLWrapper


class TestQuery(TestCase):

    endpoint = "http://dbpedia.org/sparql"

    def test_get_integer(self):
        q = """
        SELECT DISTINCT ?wikiPageID
        WHERE {
        <http://dbpedia.org/resource/Baseball> rdfs:label ?label ;
             <http://dbpedia.org/ontology/wikiPageID> ?wikiPageID
        }
        LIMIT 10
        """
        df = sparql_dataframe.get(self.endpoint, q)
        self.assertEqual(df['wikiPageID'].iloc[0], 3850)

    def test_get_multiple(self):
        q = """
        SELECT ?label ?wikiPageID
        WHERE {
        <http://dbpedia.org/resource/Baseball> rdfs:label ?label ;
             <http://dbpedia.org/ontology/wikiPageID> ?wikiPageID
        }
        LIMIT 10
        """
        df = sparql_dataframe.get(self.endpoint, q)
        # Make sure we get 5 or more labels.
        self.assertTrue(len(df) > 5)
        # Both variables should be of equal length.
        self.assertEqual(len(df['label']), len(df['wikiPageID']))

    def test_bad_query(self):
        with self.assertRaises(SPARQLWrapper.SPARQLExceptions.QueryBadFormed):
            sparql_dataframe.get(self.endpoint, "SELECT ?label FROM {}")

    def test_construct_query(self):
        q = """
        CONSTRUCT { v:tmp rdfs:label ?label }
        WHERE {
        <http://dbpedia.org/resource/Baseball> rdfs:label ?label ;
             <http://dbpedia.org/ontology/wikiPageID> ?wikiPageID
        }
        """
        with self.assertRaises(sparql_dataframe.QueryException):
            sparql_dataframe.get(self.endpoint, q)


class TestWikiDataQuery(TestCase):
    """
    Running the tests multiple times during a short time window will result
    in Wikidata throttling errors. Therefore these tests are ignored by Travis.
    """

    endpoint = 'https://query.wikidata.org/sparql'
    prefixes = """
    PREFIX bd: <http://www.bigdata.com/rdf#>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    """

    def test_get_integer(self):
        q = self.prefixes + """
                SELECT ?astronaut ?astronautLabel ?birthdate (YEAR(?birthdate) as ?year) ?birthplace WHERE {
                  ?astronaut ?x1 wd:Q11631;
                    wdt:P569 ?birthdate;
                    wdt:P19 ?birthplace.
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                }
                ORDER BY DESC (?birthdate)
                LIMIT 10
        """
        df = sparql_dataframe.get(self.endpoint, q, post=True)
        self.assertEqual(df['year'].iloc[0], 1988)

    def test_get_multiple(self):
        q = self.prefixes + """
        SELECT ?human ?humanLabel
        WHERE
        {
            ?human wdt:P31 wd:Q5 .       #find humans
            ?human rdf:type wdno:P40 .   #with at least one P40 (child) statement defined to be "no value"
            SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" }
        }
        LIMIT 10
        """
        df = sparql_dataframe.get(self.endpoint, q, post=True)
        # Make sure we get 5 or more labels.
        self.assertTrue(len(df) == 10)
        # Both variables should be of equal length.
        self.assertEqual(len(df['human']), len(df['humanLabel']))


if __name__ == '__main__':
    unittest.main()
