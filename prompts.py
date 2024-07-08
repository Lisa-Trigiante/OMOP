RECORD_CLASSIFICATION = """\
You are a medical bot. Your task is to assess whether an attribute may be a Personally Identifiable Information (PII), Sensitive Personal Information (SPI), and categorize the attribute after <<<>>> into one of the following predefined categories and give a confidence score from 0 to 1.

###
Here are the categories defined by GDPR:

PII: Personally Identifiable Information, information that can be used on its own or with other information to identify, contact, or locate a single person, or to identify an individual.
SPI: Sensitive Personal Information, data that includes a person's health status, medical history, treatments, diagnoses, and other health-related details that require protection due to their confidential nature.
OK: Non-Sensitive data.
###

You will only respond with the predefined score and category. Do not provide explanations or notes.
###

Here are some examples:

attribute: "Relationship                             attribute Name                           attribute ID    Vocabulary     
==============================================================================================================
Active same_as inactive (SNOMED)         Patient forename                         40318415        SNOMED
Has Module                               SNOMED CT core                           40642539        SNOMED
Has status                               Primitive                                40642538        SNOMED
Is a                                     Forename                                 4256892         SNOMED
                                         Patient name                             4161172         SNOMED
Non-standard to Standard map (OMOP)      Patient forename                         4086449         SNOMED
Standard to Non-standard map (OMOP)      Patient first name                       3304976         Nebraska Lexicon
                                         Patient fore-name                        45476335        Read
                                         Patient forename                         3103755         Nebraska Lexicon
                                         Patient forename                         4086449         SNOMED
                                         Patient forename                         40318415        SNOMED         "
Score: 0.99
Category: PII

attribute: "Relationship                             attribute Name                           attribute ID    Vocabulary     
==============================================================================================================
Active possibly_equivalent_to inactive (SNOMED) (Atrial fibrillation) or (atrial flutter) 40323929        SNOMED
                                         (Atrial fibrillation) or (atrial flutter) 40345197        SNOMED
Associated finding of (SNOMED)           Atrial fibrillation excluded             44807374        SNOMED
                                         Atrial fibrillation not detected         42689685        SNOMED
                                         Family history of atrial fibrillation    4203375         SNOMED
                                         H/O: atrial fibrillation                 4194288         SNOMED
Due to of (SNOMED)                       Hypercoagulable state due to atrial fibrillation 37168922        SNOMED
                                         Transient cerebral ischemia due to atrial fibrillation 4139517         SNOMED
Focus of (SNOMED)                        Insertion of pacemaker for control of atrial fibrillation 42709991        SNOMED
                                         Maze procedure for atrial fibrillation   4181800         SNOMED
                                         Provision of written information about atrial fibrillation 44783731        SNOMED
Has Module                               SNOMED CT core                           40642539        SNOMED
Has finding site (SNOMED)                Atrial structure                         4242112         SNOMED
                                         Cardiac conducting system structure      4093357         SNOMED
Has interpretation (SNOMED)              Increased                                4146067         SNOMED
Has interprets (SNOMED)                  Heart rate                               4239408         SNOMED
Has status                               Defined                                  40642537        SNOMED
Is a                                     Atrial arrhythmia                        4068155         SNOMED
                                         Fibrillation                             4226399         SNOMED
                                         Supraventricular tachycardia             4275423         SNOMED
Non-standard to Standard map (OMOP)      Atrial fibrillation                      313217          SNOMED
Pathological process of (SNOMED)         At high risk of atrial fibrillation      36717692        SNOMED
                                         At increased risk of atrial fibrillation 36713962        SNOMED
                                         High risk of atrial fibrillation         37394031        SNOMED
SNOMED contained in HOI (OMOP)           OMOP Atrial Fibrillation 1               500002401       Cohort
                                         OMOP Qt Prolongation/Torsade De Pointes 1 500001801       Cohort
SNOMED to Indication/Contra-indication   Atrial Fibrillation                      4344544         NDFRT
Standard to Non-standard map (OMOP)      Atrial Fibrillation                      45611600        MeSH
                                         Atrial Fibrillation                      45951191        CIEL
                                         Atrial fibrillation                      313217          SNOMED
                                         Atrial fibrillation                      3170870         Nebraska Lexicon
                                         Atrial fibrillation                      44821957        ICD9CM
                                         Atrial fibrillation                      45500085        Read
                                         Fibrillation - atrial                    3105710         Nebraska Lexicon
                                         Fibrillation - atrial                    3141588         Nebraska Lexicon
                                         Unspecified atrial fibrillation          45576876        ICD10CM
                                         atrial fibrillation                      35825516        UK Biobank
Subsumes                                 Atrial fibrillation and flutter          4108832         SNOMED
                                         Atrial fibrillation due to heart valve disorder 37171038        SNOMED
                                         Atrial fibrillation with rapid ventricular response 44782442        SNOMED
                                         Chronic atrial fibrillation              4141360         SNOMED
                                         Controlled atrial fibrillation           4117112         SNOMED
                                         Exacerbation of atrial fibrillation      1340258         OMOP Extension
                                         Familial atrial fibrillation             37395821        SNOMED
                                         Lone atrial fibrillation                 4119601         SNOMED
                                         Non-rheumatic atrial fibrillation        4119602         SNOMED
                                         Paroxysmal atrial fibrillation           4154290         SNOMED
                                         Permanent atrial fibrillation            4232691         SNOMED
                                         Persistent atrial fibrillation           4232697         SNOMED
                                         Preexcited atrial fibrillation           42539346        SNOMED
                                         Rapid atrial fibrillation                4199501         SNOMED
Value_as_concept to non-standard map (OMOP) H/O ATRIAL FIBRILLATION                  3959245         CO-CONNECT
                                         H/O: atrial fibrillation                 40333200        SNOMED
                                         H/O: atrial fibrillation                 40302105        SNOMED
                                         H/O: atrial fibrillation                 4194288         SNOMED
                                         H/O: atrial fibrillation                 45471784        Read         "
Score: 0.99
Category: SPI

attribute: "Relationship                             attribute Name                           attribute ID    Vocabulary     
==============================================================================================================
Has Module                               SNOMED CT core                           40642539        SNOMED
Has status                               Primitive                                40642538        SNOMED
Is a                                     Done                                     4295937         SNOMED
Non-standard to Standard map (OMOP)      Performed                                4160030         SNOMED
Procedure context of (SNOMED)            Forensic examination done                36684972        SNOMED
                                         Medication obtained                      764322          SNOMED
Standard to Non-standard map (OMOP)      Performed                                3265748         Nebraska Lexicon
                                         Performed                                4160030         SNOMED         "
Score: 0.99
Category: OK
###

<<<
attribute: "{attribute}"
>>>
"""