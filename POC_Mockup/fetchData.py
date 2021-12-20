import pandas as pd
from neo4j import GraphDatabase
import matplotlib.pyplot as plt
from neo4j import GraphDatabase
import pandas as pd
from py2neo import Graph
from IPython.core.display import display, HTML, Javascript
import mi1_neo4jupyter

import graphistry
graphistry.register(api=3, protocol="https", server="hub.graphistry.com", username="Graphistry12345", password="Alacron_05")
from neo4j import GraphDatabase, Driver

driver=GraphDatabase.driver(uri="bolt://76.251.77.235:7687", auth=('neo4j', 'NikeshIsCool')) 
session=driver.session()
    
def PotentialComorbidities(cui_prob_list):
    
    query = '''
    MATCH p=(ord:Concept)-[r:OCCURS_WITH]->(c:Concept) 
    WHERE c.cui IN {cui_prob_list} AND ord.semantic_type IN ["['Pathologic Function']", "['Disease or Syndrome']", "['Mental or Behavioral Dysfunction']", "['Sign or Symptom']", "['Injury or Poisoning']", "['Neoplastic Process']"]
    WITH round(r.co_occurrance_probability, 5)*1000 AS Score, ord, r
    WHERE Score > 20
    RETURN ord.cui AS `CUI`, ord.term AS `Problem`, Score
    ORDER BY r.co_occurrance_probability DESC
    '''.format(cui_prob_list=cui_prob_list)
    data = session.run(query)
    likely_comorbidities = pd.DataFrame([dict(record) for record in data])
    
    return likely_comorbidities.head(10)

def LikelyOrders(cui_prob_list):
    
    # Find prescriptions associated with the input problem    
    query = '''
    MATCH p=(ord:Concept)-[r:OCCURS_WITH]->(c:Concept) 
    WHERE c.cui IN {cui_prob_list} AND ord.semantic_type IN ["['Clinical Drug']"]
    WITH round(r.co_occurrance_probability, 5)*1000 AS Score, ord, r
    WHERE Score > 20
    RETURN ord.cui AS `Code`, ord.term AS `Order`, Score
    ORDER BY r.co_occurrance_probability DESC
    '''.format(cui_prob_list=cui_prob_list)
    data = session.run(query)
    orders_likely_rx = pd.DataFrame([dict(record) for record in data]).head(10)
    
    # Find abnormal labs associated with the input problem
    query = '''
    MATCH p=(ord:Concept)-[r:OCCURS_WITH]->(c:Concept) 
    WHERE c.cui IN {cui_prob_list} AND ord.semantic_type IN ["['Clinical Attribute']"]
    WITH round(r.co_occurrance_probability, 5)*1000 AS Score, ord, r
    WHERE Score > 20
    RETURN ord.cui AS `Code`, ord.description AS `Order`, Score
    ORDER BY r.co_occurrance_probability DESC
    '''.format(cui_prob_list=cui_prob_list)
    data = session.run(query)
    orders_likely_lab = pd.DataFrame([dict(record) for record in data]).head(10)
    
    # Find procedures associated with the input problem
    query = '''
    MATCH p=(ord:D_Icd_Procedures)-[r:OCCURS_WITH]->(c:Concept) 
    WHERE c.cui IN {cui_prob_list}
    WITH round(r.co_occurrance_probability, 5)*1000 AS Score, ord, r
    WHERE Score > 20
    RETURN ord.icd9_code AS `Code`, ord.long_title AS `Order`, Score
    ORDER BY r.co_occurrance_probability DESC
    '''.format(cui_prob_list=cui_prob_list)
    data = session.run(query)
    orders_likely_procedure = pd.DataFrame([dict(record) for record in data]).head(10)
    
    return orders_likely_rx, orders_likely_lab, orders_likely_procedure

def nodedisplay():
#     g=Graph('neo4j+s://1d23f23f.databases.neo4j.io:7687', auth=("neo4j", "FUjaBMKHBigyHtjaD9il71GV4GVGAsi7YBWtIBn-Cyo"))
    g=Graph('bolt://76.251.77.235:7687', auth=('neo4j', 'NikeshIsCool'))
    options = {"Src_Prob": "name", "Problem": "name", "Diagnosis": "name", "Treatment": "name"}


    query = """
        MATCH (n)-[r]->(m)
        RETURN n ,
            id(n),
            r,
            m ,
            id(m)
        LIMIT 25
        """
        
    test = mi1_neo4jupyter.draw(g,options,query, physics=True)
    return test.data 

def graphdisplay():
    #NEO4J_CREDS = {'uri': 'neo4j+s://1d23f23f.databases.neo4j.io:7687', 'auth': ('neo4j', 'FUjaBMKHBigyHtjaD9il71GV4GVGAsi7YBWtIBn-Cyo')}
    NEO4J_CREDS = {'uri': 'bolt://76.251.77.235:7687', 'auth': ('neo4j', 'NikeshIsCool')}
    graphistry.register(bolt=GraphDatabase.driver(**NEO4J_CREDS))

    g = graphistry.cypher("""
        MATCH path = (stroke:Concept {cui: 'C0948008'})-[*..4]-(af:Concept {cui: 'C0004238'})
        RETURN path
        LIMIT 20
        """)
    g = g.bind(edge_title="type")
    g = g.bind(point_title="cui")
    iframe_url = g.plot(render=False)
    return iframe_url