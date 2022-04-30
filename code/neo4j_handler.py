import pandas as pd
from neo4j import GraphDatabase


class neob:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.session = self.driver.session(database="academicworld")
        self.keywords = list(pd.DataFrame(self.session.run("match  (k:KEYWORD) return distinct(k.name) as name order by name")).iloc[:,0])
        self.universities = list(pd.DataFrame(self.session.run("match  (u:INSTITUTE) return distinct(u.name) as name order by name")).iloc[:,0])
    def close(self):
        self.session.close()
        self.driver.close()


#def setup():
 #   driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "ko8kmx5rost5"))
  #  session = driver.session(database="academicworld")
  #  return session

def univ_keyword_pub_comp(session,unv,keyword):
    query = ("match(unv:INSTITUTE{name:'"+ unv +
             "' })-[:AFFILIATION_WITH]-(f1:FACULTY)"+
             "-[:PUBLISH]-(p:PUBLICATION)-[:LABEL_BY]-"+
             "(k:KEYWORD {name:'"+keyword+
             "'}) return f1.name as name, count(p) as pub_count order by pub_count desc")
    res = session.run(query)
    res = pd.DataFrame(res)
    return res


