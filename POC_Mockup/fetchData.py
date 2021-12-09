import pandas as pd
from neo4j import GraphDatabase

driver=GraphDatabase.driver(uri="bolt://76.251.77.235:7687", auth=('neo4j', 'NikeshIsCool')) 
session=driver.session() 
    
def PotentialComorbidities(cui_prob_list):
    
    query = '''
    MATCH (prob1:Problem)<-[:HAD_PROBLEM]-(pt:Patients)
    WHERE prob1.cui in {cui_prob_list}
    WITH distinct(pt) AS patients
    MATCH (patients)-[:HAD_PROBLEM]->(prob2:Problem)
    WITH prob2.cui AS CUIs, count(prob2) AS Number
    MATCH (c:Concept)
    WHERE c.cui IN CUIs AND c.cui_pref_term IS NOT NULL 
    RETURN c.term as `PotentialProblem`, c.cui AS CUI, Number
    ORDER BY Number DESC
    '''.format(cui_prob_list=cui_prob_list)
    comorbidities = session.run(query)
    comorbidities = pd.DataFrame([dict(record) for record in comorbidities])
    
    query = '''
    MATCH (excluded:Problem)
    WHERE excluded.cui in {cui_prob_list}
    WITH collect(excluded) as excluded
    MATCH (pt:Patients)-[:HAD_PROBLEM]->(prob:Problem)
    WITH excluded, pt, collect(prob) as problems
    WHERE NONE (prob in problems where prob in excluded)
    MATCH (pt)-[:HAD_PROBLEM]-(prob2:Problem)
    WITH prob2.cui AS CUIs, count(prob2) AS Number
    MATCH (c:Concept)
    WHERE c.cui IN CUIs AND c.cui_pref_term IS NOT NULL 
    RETURN c.term as `PotentialProblem`, c.cui AS CUI, Number
    ORDER BY Number DESC
    '''.format(cui_prob_list=cui_prob_list)
    gen_problems = session.run(query)
    gen_problems = pd.DataFrame([dict(record) for record in gen_problems])
    
    gen_pop_total = sum(gen_problems['Number'])
    gen_problems['Gen_pop_proportion'] = gen_problems['Number']/gen_pop_total
    
    gen_problems = gen_problems[gen_problems['Number'] > 25]
    
    comorb_total = sum(comorbidities['Number'])
    comorbidities['Comorbidities_proportion'] = comorbidities['Number']/comorb_total
    
    comorbidities = comorbidities[comorbidities['Number'] > 75/len(cui_prob_list)]
    
    # Merge the "Gen_pop_proportion" column from gen_problems into comorbidities
    comorbidities = pd.merge(comorbidities, gen_problems, on=['CUI', 'PotentialProblem'])
    
    comorbidities.head()
    
    comorbidities['OddsRatio'] = (comorbidities['Comorbidities_proportion']/comorbidities['Gen_pop_proportion'])
    comorbidities.sort_values(by='OddsRatio', ascending=False, inplace=True)
    
    return comorbidities.loc[:,['CUI','PotentialProblem', 'OddsRatio']].head(10)

def LikelyOrders(cui_prob_list):
        
    query = '''
    MATCH p=(ord:Concept)-[r:OCCURS_WITH]->(c:Concept) 
    WHERE c.cui IN {cui_prob_list}
    WITH round(r.co_occurrance_probability, 3)*1000 AS Score, ord, r
    WHERE Score > 20
    RETURN ord.term AS `Order`, ord.description AS AlternateDescription, Score
    ORDER BY r.co_occurrance_probability DESC
    '''.format(cui_prob_list=cui_prob_list)
    data = session.run(query)
    LikelyOrders = pd.DataFrame([dict(record) for record in data])
    
    # Assign prescriptions to a dataframe
    orders_likely_rx = LikelyOrders[LikelyOrders.AlternateDescription.isnull()]
    orders_likely_rx = orders_likely_rx.loc[:,['Order', 'Score']]
    
    # Assign labs likely to be abnormal to a dataframe
    orders_likely_lab = LikelyOrders[LikelyOrders.AlternateDescription.notnull()]
    orders_likely_lab = orders_likely_lab.loc[:,['AlternateDescription', 'Score']]
    orders_likely_lab.columns = ['Order', 'Score']
    
    return orders_likely_rx, orders_likely_lab