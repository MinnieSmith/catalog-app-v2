from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, DrugClass, Drug, DrugInformation, NewDrugs, NewDrugInformation

engine = create_engine('sqlite:///drugcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a dummy user
User1 = User(id=1, username="Caspar Smith", email="caspar.melchi@gmail.com", password="happinessis")
session.add(User1)
session.commit()

# Antibiotics
drug_class1 = DrugClass(id=1,name="Antibiotics", user_id=1)

session.add(drug_class1)
session.commit()

# Amoxicillin
drug1 = Drug(name="Amoxicillin", drug_class_id=1, user_id=1, id=1)
session.add(drug1)
session.commit()

drug_info1 = DrugInformation(name="Amoxicillin", drug_class_id=1, user_id=1,
                             information=" ".join([
                                'Amoxicillin is a pencillin antiobiotic used to treat a range of bacterial infections.'
                                'These include pneumonia, tonsillitis, sinusitis, endocarditis, urinary tract, skin,'
                                'and periodontal infections. The standard dose for amoxicillin is 250mg to 500mg every'
                                'eight hours for acute infections and once daily for prophylaxis. Amoxicillin can'
                                'eradicate a lot of beneficial flora in the GI tract causing thrush and diarrhoea'
                                'and probiotics supplementation during and after the course is strongly advised. '
                                'Stop taking amoxicillin if you develop a severe rash or diarrhoea.'
                             ]))
session.add(drug_info1)
session.commit()


# Metronidazole
drug2 = Drug(name="Metronidazole", drug_class_id=1, user_id=1, id=2)
session.add(drug2)
session.commit()

drug_info2 = DrugInformation(name="Metronidazole", drug_class_id="1", user_id=1,
                             information=" ".join([
                                'Metronidazole is a nitromidizole antibiotic used to treat bacterial infections.'
                                'These include anaerobic, dental, protozoal, intra-abdominal infections, aspiration'
                                'pneumonia, lung abscess, PID, and bacterial vaginosis. It is a powerful antibiotic'
                                'that can cause nausea and anorexia. The most important reaction is that it inhibits'
                                'the body\'s ability to metabolise alcohol. No alcohol is to be consumed during and'
                                'for 24 hours after the last dose to prevent nausea, vomiting, flushing, and '
                                'palpitation. Stop taking metronidazole immediately if you have any numbness, pain,'
                                'tingling, or weakness in hands or feet.'
                             ]))
session.add(drug_info2)
session.commit()

# Azithromycin
drug3 = Drug(name="Azithromycin", drug_class_id=1, user_id=1, id=3)
session.add(drug3)
session.commit()

drug_info3 = DrugInformation(name="Azithromycin", drug_class_id=1, user_id=1,
                             information=" ".join([
                                'Azithromycin is macrolide antibiotic used to treat bacterial infections.'
                                'These include chlamydial infections, tonsillitis, pneumonia, MAC, typhoid,'
                                'traveller\'s diarrhoea, and pertusis. Azithromycin is very well tolerated'
                                'antibiotic, with the most common side effects being nausea, vomitting and'
                                'diarrhoea. In infants less than 2 weeks of age, it has been associated with'
                                'hypertrophic pyloric stenosis.'
                             ]))
session.add(drug_info3)
session.commit()

# Antihypertensives
drug_class2 = DrugClass(name="Antihypertensives", user_id=1, id=2)

session.add(drug_class2)
session.commit()

# Atenolol
drug4 = Drug(name="Atenolol", drug_class_id=2, user_id=1, id=4)
session.add(drug4)
session.commit()

drug_info4 = DrugInformation(name="Atenolol", drug_class_id=4, user_id=1,
                             information=" ".join([
                                'Atenolol is an antihypertensive which blocks beta receptors and causes'
                                'a reduction in heart rate, cardiac contractility and BP. It also slows'
                                'conduction through the AV node and prolongs refractory periods. It is'
                                'also used for angina, tachyarrhythmias, MI and migraine prevention. It'
                                'is a well tolerated medication but can sometime cause hypotension, fatigue'
                                'dizziness, abnormal vision and brochospasm.'
                             ]))
session.add(drug_info4)
session.commit()

# Lercanidipine
drug5 = Drug(name="Lercanidipine", drug_class_id=2, user_id=1, id=5)
session.add(drug5)
session.commit()

drug_info5 = DrugInformation(name="Lercanidipine", drug_class_id=2, user_id=1,
                             information=" ".join([
                                'Lercanidipine is a calcium channel blocker antihypertensive works by'
                                'relaxing blood vessels and reducing resistance. Along with being used'
                                'to lower blood pressure it is also used for angina. It is best taken'
                                '15 mins before a meal. It can cause nauseau, headaches (due to the'
                                'vasodilations, hypotension and peripheral oedema especially in the first'
                                'few weeks on this medication.'
                             ]))
session.add(drug_info5)
session.commit()

# Perindopril
drug6 = Drug(name="Perindopril", drug_class_id=2, user_id=1, id=6)
session.add(drug6)
session.commit()

drug_info6 = DrugInformation(name="Perindopril", drug_class_id=2, user_id=1,
                             information=" ".join([
                                'Perindopril is an ACE inhibitor which has a multinodal mechanism of'
                                'action to reduce blood pressure. It is also use for diabetic nephropathy'
                                'and prevention of renal failure. It can cause hypotension, headache,'
                                'dizziness, hyperkalaemia, fatigue, nausea, vomiting. It can also cause'
                                'a rare and persistent non-productive cough which can occur within days'
                                'to months of starting treatment and will stop after 1-4 weeks of stopping'
                                'treatment. It is not safe to use in pregnancy.'
                             ]))
session.add(drug_info6)
session.commit()

# Antihistamines
drug_class3 = DrugClass(name="Antihistamines", user_id=1, id=3)

session.add(drug_class3)
session.commit()

# Fexofenadine
drug7 = Drug(name="Fexofenadine", drug_class_id=3, user_id=1, id=7)
session.add(drug7)
session.commit()

drug_info7 = DrugInformation(name="Fexofenadine", drug_class_id=3, user_id=1,
                             information=" ".join([
                                'Fexofenadine is a less sedating \'second\' generation antihistamine. It'
                                'reduces the effects of histamine by binding to the H1 receptor and stabilising'
                                'it in the inactive form. It is used to treat allergic rhinitis and chronic '
                                'urticaria. It only needs to be taken once daily and is generally well tolerated.'
                                'In the elderly, there is an increase risk of drowsiness and other side effects,'
                                'however, this is still less than sedating antihistamines. It is safe to use in'
                                'pregnancy and breastfeeding.'
                             ]))
session.add(drug_info7)
session.commit()

# Cyproheptadine
drug8 = Drug(name="Cyproheptadine", drug_class_id=3, user_id=1, id=8)
session.add(drug8)
session.commit()

drug_info8 = DrugInformation(name="Cyproheptadine", drug_class_id=3, user_id=1,
                             information=" ".join([
                                'Cyproheptadine is a sedating antihistamine which binds to the H1 receptor'
                                'and reduces the effects of histamine. It also anticholinergic activites'
                                'and antiserotonin activity. It is used for allergic conditions, itch and serotonin'
                                'toxicity. It has also been used \'off label\' for migraine prevention and appetite'
                                'stimulation. It can cause drowsiness, hypotension, confusion, dry mouth and'
                                'constipation. Avoid use in children under 2 years of age. It is safe to use in'
                                'pregnancy.'

                             ]))
session.add(drug_info8)
session.commit()

# Immunomodulators
drug_class4 = DrugClass(name="Immunomodulators", user_id=1, id=4)

session.add(drug_class4)
session.commit()

# Sulfasalazine
drug9 = Drug(name="Sulfasalazine", drug_class_id=4, user_id=1, id=9)
session.add(drug9)
session.commit()

drug_info9 = DrugInformation(name="Sulfasalazine", drug_class_id=4, user_id=1,
                             information=" ".join([
                                'Sulfasalazine is an anti-inflammatory and immunosuppressant. It is used to treat'
                                'ulcerative colitis, Crohn\'s disease and rheumatoid arthritis(RA). In RA it is used'
                                'when NSAID\'s do not provide adequate relief. Sulfasalazine can cause vomiting and'
                                'must be taken with food to reduce stomach upset. It can cause reversible male'
                                'infertility and yellow-orange discolouration of body fluids. Blood count and liver'
                                'and renal monitoring is required on this medication.'
                             ]))
session.add(drug_info9)
session.commit()

# Adalimumab
drug10 = Drug(name="Adalimumab", drug_class_id=4, user_id=1, id=10)
session.add(drug10)
session.commit()

drug_info10 = DrugInformation(name="Adalimumab", drug_class_id=4, user_id=1,
                              information=" ".join([
                                'Adalimumab binds to a cytokine called TNF alpha which is involved in inflammatory'
                                'and immune reponses responsible for the pathogenicity of RA, psoriasis and '
                                'inflammatory bowel disease. It is used to treat RA, psoriatic arthritis, ankylosing'
                                'spondylitis, and plaque psoriasis. The most important side effect of this medication'
                                'is due to its effects on the immune system. Infections are a common side effect and'
                                'may be serious. Blood dyscrasias and malignancies can occur in 0.1-1% of patients.'
                                'Some vaccines cannot be given whilst on Adalimumab and immunisation needs should be'
                                'considered before commencing treatment.'
                             ]))
session.add(drug_info10)
session.commit()


# Antineoplastics Drugs
drug_class5 = DrugClass(name="Antineoplastics", user_id=1, id=5)

session.add(drug_class5)
session.commit()

drug11 = Drug(name="Exemestane", drug_class_id=5, user_id=1, id=11)
session.add(drug11)
session.commit()

drug_info11 = DrugInformation(name="Exemestane", drug_class_id=5, user_id=1,
                              information=" ".join([
                                'Exemestane is an aromatase inhibitor which reduces tissue estrogen concentration.'
                                'It is used to treat hormone receptor positive advanced breast cancer in postmenopausal'
                                'women and in early breast cancer for premenopausal women. Common side effects include'
                                'hot flushes, vaginal dryness, nausea and vomiting, hair loss, and peripheral oedema.'
                                'Exemestane should be taken with food. While on this medication, bone density '
                                'monitoring and calcium and vitamin D supplementation is required. Compared to '
                                'selective oestrogen receptor modulators, Exemestane causes less endometrial'
                                'hyperplasia and VTE but more joint pain, muscle pain, bone fractures and CV problems.'
                               ]))
session.add(drug_info11)
session.commit()

drug12 = Drug(name="Goserelin", drug_class_id=5, user_id=1, id=12)
session.add(drug12)
session.commit()

drug_info12 = DrugInformation(name="Goserelin", drug_class_id=5, user_id=1,
                              information=" ".join([
                                'Goserelin is a Gonadotrophin-releasing hormone (GnRH) agonist. Continuous'
                                'administration of GnRH agonists inhibits gonadotrophin production, reducing'
                                'steroidgenesis by the ovaries and testicles which inhibits the growth of'
                                'certain hormone-dependent tumours. It is used to treat metastatic or locally'
                                'advanced prostate cancer, and early or advanced breast cancer. Goserelin is'
                                'administered as a SB implant into the anterior abdominal wall. It commonly'
                                'caused reduce BMD which needs to be monitored and vitamin D and calcium'
                                'supplementation is recommended. It can also cause a tumour flare in the'
                                'first two weeks of treatment. This can cuase a worsening of symptoms, including'
                                'spinal cord compression. In prostate cancer, acute bladder obstruction or'
                                'renal failure have occurred. To prevent tumour flare, anti-androgens should'
                                'commenced, 1-2 weeks prior to first dose of Goserelin and should continue for '
                                'a month in total.'
                               ]))
session.add(drug_info12)
session.commit()

# New Drugs
# Umeclidinium
drug13 = NewDrugs(name="Umeclidinium", user_id=1, id=13)
session.add(drug13)
session.commit()

drug_info13 = NewDrugInformation(name="Umeclidinium", user_id=1, new_drugs_id=13,
                                information=" ".join([
                                    'Umeclidinium is an anticholinergic which promotes bronchodilation used for COPD.'
                                    'It is used in combination with fluticasone and vilanterol in COPD patients with'
                                    'FEV1 <50% and recurrent exacerbations. It must be used with caution in people with'
                                    'cardiovascular disorders, glaucoma, and bladder obstruction. It is generally a'
                                    'well tolerated medication. Common side effects include dry mouth, nasopharyngitis,'
                                    'taste disturbance and throat irritation. It can less frequently cause blurred '
                                    'vision, dizziness,and urinary retention.'
                                    ]))
session.add(drug_info13)
session.commit()

drug14 = NewDrugs(name="Milnacipran", user_id=1, id=14)
session.add(drug14)
session.commit()

drug_info14 = NewDrugInformation(name="Milnacipran", user_id=1, new_drugs_id=14,
                                information=" ".join([
                                    'Milnacipran is the first drug available in australia for fibromyalgia. It is a'
                                    'noradrenaline-serotonin reuptake inhibitor which can improve the symptoms of'
                                    'fibromyalgia. Other SNRIs are usually used for major depression. Precaution must'
                                    'be taken with other antidepressant and opioids due to the risk of serotonin '
                                    'toxicity. SNRIs may cause palpitations, increase heart rate and BP and '
                                    'stress-induced cardiomyopathy (takotsubo). Patients on Milnacipran should be'
                                    'assessed after a 12-week trial. Milnacipran should be tapered off if there is no'
                                    'improvement. Data from clinical trials suggest that one third of patients get '
                                    'relief due to reduce pain.'
                                    ]))
session.add(drug_info14)
session.commit()

print("drug information added!")