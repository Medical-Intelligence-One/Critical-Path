import pandas as pd
from neo4j import GraphDatabase

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