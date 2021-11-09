# MI-1 Product Critical Path

Signs to help you get around:  

- 🟢 Directly on critical path 
- 🟡 Ancillary to critical path  
- 🚦 Dependency marker
- 🔁 Part of iteration loop
- ☑️ Done

## Knowledge graph
---
- ☑️ Prove that GPT3 can extract relationships accurately
- 🟢 Engineer a knowledge model to enable a simple, flexible reasoning framework to operate on it to fulfill use cases (🔁Iterate with reasoning framework and use cases)
- 🟢 Fine-tune GPT3 to extract knowledge according to the knowledge model
- 🟢 Peform extraction from key sources:
    - 🟢 PubMed
    - 🟡 UpToDate (🚦Partner with UpToDate)
    - 🟡 Internal Medicine textbooks (🚦Partner with a publisher like Elsevier)

## Connected patient-level data
---
- ☑️ MIMIC-III Labs to UMLS Concepts (LOINC-AUI)
- ☑️ MIMIC-III Prescriptions to UMLS Concepts (NCD-AUI)
- 🟢 MIMIC-III Problems to UMLS concepts (NLP-AUI)
    - 🟢 Improve quality of NLP
- 🟡 MIMIC-III ICD diagnoses to UMLS concepts
- 🟡 MIMIC-III procedures to UMLS concepts (e.g. EKG)
- 🟡 MIMIC-III imaging to UMLS concepts

## Virtualized Population
---
- 🟡 Develop model to accurately and precisely represent populations
    - 🟡 Include temporal information
- 🟡 Apply the model to virtualize MIMIC-III
- 🟡 Adapt use case code to run on virtual population
- 🟡 Update virtual population from new incoming patient data
- 🟡 Update a global virtual population from a local version
- 🟡 Automate updates as part of an MLOps process
  
## Reasoning Framework
---
- 🟢 Design a set of reasoning methods that can flexibly interact with the knowledge graph and patient data to fulfill use cases (🔁 with knowledge graph and use cases)

    | Status | Process      | Output |
    | :---: | :---- |:---|  
    |🟢| Find association between a patient-connected starting concept and the outcome concept you wish to avoid      | Path-defining start and end nodes       |
    |🟢| Find all shortest paths between the patient and outcome concept through the knowledge graph   | Pathologic paths relevant to this patient        |
    |🟢| Push out from pathologic path to find concepts which are known to disrupt elements of the pathologic path | Theoretical treatments with explanations |  
    |🟢| Find associations between outcome concepts and possible treatments, ordered by strongest association first | Empiric treatments and other associations |  
    |🟢| Find shortest paths between possible treatments and the pathologic path | Rationalizations for empiric treatment |

  
## Use Cases
---

- 🟢 "I have a patient with AFib. Should I anticoagulate?" Contributed by Dr. Stein, Scripps CMIO-Inpatient
