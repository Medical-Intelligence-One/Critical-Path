# MI-1 Product Critical Path
![Scottish Highlands](https://bikepacking.com/wp-content/uploads/2016/07/highland-trail-550-00.jpg)

### Mission
Develop a flexible framework for applying AI in healthcare and a set of use cases that prove value as defined by key stakeholders. 

### Current top priorities
- Fulfill Dr. Stein's use case
    - 🔁 Develop a reasoning framework
    - 🔁 Develop a knowledge model
    - Fine-tune GPT3 for the knowledge model
    - ☑️ Collect all relevant literature
    - Extract relationships from relevant literature
    - Import GPT-extracted relationships into the graph
    - Test the system on MIMIC-III patients
    - Demo for Dr. Stein

### Immediate next steps:
- Add 2-3 more use cases 
- Share Neo4j's embedding webinar with Nikesh
- Reformat the knowledge graph to have all synonyms point to a central "preferred term" (☑️ UMLS_test, 🟢 MIMIC-III_v1.4_MI-1)
- 🔁 Develop pathologic pathfinding methods using existing `CAUSE_OF` relationships from UMLS
- 🔁 Develop intervention pathfinding methods using pathologic paths and `MAY_TREAT` or `MAY_PREVENT` relationships
- ☑️ set up the annotator to display UMLS concept capture for each sentence
- ☑️ pull all the literature relevant to atrial fibrillation, stroke, anticoagulation, and hemorrhage/bleeding ([UseCase_AntiCoag_AF.ipynb](UseCase_AntiCoag_AF.ipynb))
- ☑️ create a csv of sentences that have causal relationships from the Afib literature
- 🔁 create a knowledge model that anchors on UMLS terms or their existance-state opposites (e.g. "no atrial fibrillation") connected to literature-provided terms with `STATE_OF` relationships
- develop methods to weight relationships based on number of publications and quality of publications
- import human-annotated relationships into the graph to test pathologic and treatment pathfinding
- fine-tune GPT3 on the new knowledge model to import more literature


### Trail markers 
  
🟢 Directly on critical path   
🟡 Ancillary to critical path    
🚦 Dependency marker  
🔁 Part of iteration loop  
☑️ Done  
🔗 Link to notebook or website  

### Contents:  
[Knowledge Graph](#kg)  
[Connected patient-level data](#cpld)  
[Virtualized Population](#vp)  
[Reasoning Framework](#rf)  
[Use Cases](#uc)  

<a id='kg'></a>
## Knowledge graph
---
### Basic knowledge
- ☑️ Develop method to use GPT3 to extract conceptual relationships from the medical literature [🔗](GPT_fine-tuning.ipynb#performance_assessment)
- 🟢 Engineer a knowledge model on which a simple, flexible reasoning framework can operate to fulfill use cases (🔁Iterate with reasoning framework and use cases)
- 🟢 Fine-tune GPT3 to extract knowledge according to the knowledge model 
    - Manually annotate training data for fine-tuning [🔗](Annotation_Tool.ipynb#annotator_tool)
    - Perform fine-tuning [🔗](Annotation_Tool.ipynb#GPT3_fine_tuner)
- 🟢 Peform extraction from key sources:
    - 🟢 PubMed
    - 🟡 UpToDate (🚦Partner with UpToDate)
    - 🟡 Medical textbooks (🚦Partners with a publisher like Elsevier)

<a id='cpld'></a>
### Clinical Practice Guidelines
- 🟡 Consider partnering with [EvidenceCare](https://apporchard.epic.com/Gallery?id=1594), who have already started to build this integration for Epic
- 🟡 Identify guidelines of interest to users (e.g. [Anticoagulation guidelines for patients with atrial fibrillation](https://www.jacc.org/doi/pdf/10.1016/j.jacc.2019.01.011))
- 🟡 Develop patient data queries that retrieve all necessary data for a clinical decision-making process from the EHR
- 🟡 Manually write the guidelines into executable code that produces recommendations, explanations, and evidence. Consider automating the code generation with:
    - [Retrieval-based NLP](http://ai.stanford.edu/blog/retrieval-based-NLP/) or
    - Fine-tuned transformer language models
- 🟡 Present the data for verification to the clinician/patient
- 🟡 Execute the decision-making process to produce a recommendation
- 🟡 Present the guideline recommendations with links to the evidence behind the recommendation

## Connected patient-level data
---
- ☑️ Import MIMIC-III into graph [🔗](MIMIC-III_v1.4_MI1_import.ipynb)
- ☑️ Import UMLS concepts and relationships into graph [🔗](UMLS_import.ipynb)
- ☑️ MIMIC-III Labs to UMLS Concepts (LOINC-AUI) [🔗](MIMIC-III_v1.4_MI1_import.ipynb#MIMIC_labs_to_UMLS)
- ☑️ MIMIC-III Prescriptions to UMLS Concepts [🔗](MIMIC-III_v1.4_MI1_import.ipynb#MIMIC_Rx_to_UMLS)
- ☑️ MIMIC-III Problems to UMLS concepts [🔗](MIMIC-III_v1.4_MI1_import.ipynb#UMLS_problem_creation)
    - 🟢 Improve quality of NLP? - it seemed to work poorly for atrial fibrillation
- 🟢 MIMIC-III ICD diagnoses to UMLS concepts [🔗](MIMIC-III_v1.4_MI1_import.ipynb#MIMIC_ICD_Dx_to_UMLS)
- 🟡 MIMIC-III procedures to UMLS concepts (e.g. EKG)
- 🟡 MIMIC-III imaging to UMLS concepts

<a id='vp'></a>
## Virtualized Population
---
- 🟡 Develop model to accurately and precisely represent populations
    - 🟡 Include temporal information
- 🟡 Apply the model to virtualize MIMIC-III
- 🟡 Adapt use case code to run on virtual population
- 🟡 Update virtual population from new incoming patient data
- 🟡 Update a global virtual population from a local version
- 🟡 Automate updates as part of an MLOps process
  
<a id='rf'></a>
## Reasoning Framework
---
- 🟢 Design a set of reasoning methods that can flexibly interact with the knowledge graph and patient data to fulfill use cases [🔗](Reasoning_Framework.ipynb) (🔁 with knowledge graph and use cases)

    | Status | Process      | Output |
    | :---: | :---- |:---|  
    |🟢| Find association between a patient-connected starting concept and the outcome concept you wish to avoid      | Path-defining start and end nodes       |
    |🟢| Find all shortest paths between the patient and outcome concept through the knowledge graph   | Pathologic paths relevant to this patient        |
    |🟢| Push out from pathologic path to find concepts which are known to disrupt elements of the pathologic path | Theoretical treatments with explanations |  
    |🟢| Find associations between outcome concepts and possible treatments, ordered by strongest association first | Empiric treatments and other associations |  
    |🟢| Find shortest paths between possible treatments and the pathologic path | Rationalizations for empiric treatment |

Consider using [Max De Marzi's methods to create dynamic rule-based decision trees in Neo4j.](https://maxdemarzi.com/2018/01/14/dynamic-rule-based-decision-trees-in-neo4j/#more-4189) 

<a id='uc'></a>
## Use Cases
---

- Mock-up the workflow from MIS global summit in an environment like EvidenceCare's Epic App. Due January 1.
    - List content for our app (Due by Nov 23) TJM
    - Define the workflow between user, website, and service (Due by Nov 23) TJM & NS workshop session
    - Define interface between UI and service (Due by Nov 30) TJM & NS workshop session
    - Make a webpage that looks like an Epic screen (Due by Dec 7) TJM
    - Flask configuration (due by Nov 30) TJM (Nikesh's static IP: 122:169:102:165)
    - Port configuration (due by Dec 7) TJM & NS
    - Write & test the code (Due by Dec 23) TJM & NS
    - Provide instructions, documentation, supporting information to make it (Due by Dec 23) BED
  
- 🟢 "I have a patient with AFib. Should I anticoagulate?" Contributed by Dr. Stein, Scripps CMIO-Inpatient. [🔗](UseCase_AntiCoag_AF.ipynb)