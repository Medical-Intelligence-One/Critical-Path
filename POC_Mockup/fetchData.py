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
    WITH round(r.co_occurrence_probability, 5) AS Score, ord, r, c
    RETURN c.cui AS `Known_CUI`, c.term AS `Known_Problem`, ord.cui AS `CUI`, ord.term AS `Problem`, Score
    ORDER BY r.co_occurrence_probability DESC
    LIMIT 10
    '''.format(cui_prob_list=cui_prob_list)
    data = session.run(query)
    likely_comorbidities = pd.DataFrame([dict(record) for record in data])
    
    return likely_comorbidities.head(10)

def LikelyOrders(cui_prob_list):
    
    # Find prescriptions associated with the input problem    
    query = '''
    MATCH p=(ord:Concept)-[r:OCCURS_WITH]->(c:Concept) 
    WHERE c.cui IN {cui_prob_list} AND ord.semantic_type IN ["['Clinical Drug']"]
    WITH round(r.co_occurrence_probability, 5) AS Score, ord, r
    RETURN ord.cui AS `Code`, ord.term AS `Order`, Score
    ORDER BY r.co_occurrence_probability DESC
    LIMIT 10
    '''.format(cui_prob_list=cui_prob_list)
    data = session.run(query)
    orders_likely_rx = pd.DataFrame([dict(record) for record in data]).head(10)
    
    # Find abnormal labs associated with the input problem
    query = '''
    MATCH p=(ord:Concept)-[r:OCCURS_WITH]->(c:Concept) 
    WHERE c.cui IN {cui_prob_list} AND ord.semantic_type IN ["['Clinical Attribute']"]
    WITH round(r.co_occurrence_probability, 5) AS Score, ord, r
    RETURN ord.cui AS `Code`, ord.description AS `Order`, Score
    ORDER BY r.co_occurrence_probability DESC
    LIMIT 10
    '''.format(cui_prob_list=cui_prob_list)
    data = session.run(query)
    orders_likely_lab = pd.DataFrame([dict(record) for record in data]).head(10)
    
    # Find procedures associated with the input problem
    query = '''
    MATCH p=(ord:D_Icd_Procedures)-[r:OCCURS_WITH]->(c:Concept) 
    WHERE c.cui IN {cui_prob_list}
    WITH round(r.co_occurrence_probability, 5) AS Score, ord, r
    RETURN ord.icd9_code AS `Code`, ord.long_title AS `Order`, Score
    ORDER BY r.co_occurrence_probability DESC
    LIMIT 10
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

def graphdisplay(kp, p, code, type):
    #NEO4J_CREDS = {'uri': 'neo4j+s://1d23f23f.databases.neo4j.io:7687', 'auth': ('neo4j', 'FUjaBMKHBigyHtjaD9il71GV4GVGAsi7YBWtIBn-Cyo')}
    NEO4J_CREDS = {'uri': 'bolt://76.251.77.235:7687', 'auth': ('neo4j', 'NikeshIsCool')}
    graphistry.register(bolt=GraphDatabase.driver(**NEO4J_CREDS))
    
    g = graphistry.cypher("""
    WITH '{p}' as p, '{code}' as code
    MATCH path = (stroke:Concept)-[*..4]-(af:Concept) 
    WHERE stroke.cui = p AND af.cui = code
    RETURN path
    LIMIT 20
    """.format(p=p, code=code))
    
    g = g.bind(edge_title="type")
    g = g.bind(point_title="term")
    g = g.settings(url_params={
    'play': 2000, 'showPointsOfInterest': True, 'showPointsOfInterestLabel': True, 'showLabelPropertiesOnHover': False,
    'pointsOfInterestMax': 50
    })
    g = g.layout_settings(strong_gravity=True, gravity=0.75)
    g = g.addStyle(logo={'url': 'https://upload.wikimedia.org/wikipedia/commons/4/48/BLANK_ICON.png'})
    iframe_url = g.plot(render=False)
    return iframe_url