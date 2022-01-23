# Assessment Guidance
Methodologies for attacks on other systems such as networks, software, and web applications exist. However, there is no such framework for ML systems. This document aims to formalize and enable organizations to start assessing their ML systems through the lens of information security, and will frame attacks in an operational setting. Additionally, as most consequential attacks happen against production systems, this document assumes the attacker has incomplete information about the target.
 
## Defining the Attack Surface
Before discussing attacks, it is helpful to define the attack surface. Machine learning systems refer to any system which machine learning is part of. It is the combination or interaction of machine learning, supporting infrastructure, or downstream systems. This could refer to an MLOps pipeline, a webserver that hosts a model, or a service that consumes an output. The attack surface covers a broad range of technologies and systems that are better described in context of the machine learning development lifecycle, 

| Phase | Description | Activity Type | 
| -- | -- | -- |
| Data Collection | Models require data to be trained. Data is usually collected from both public and platform sources with a specific model in mind. This is an ongoing process and data will continue to be collected from these sources.| Train |
| Data Processing | The collected data is processed in any number of ways before being introduced to an algorithm for both training and inference. |Train |
| Model Training | The processed data is then ingested by an algorithm and a model is trained. | Train |
| Model Validation | After a model is trained, it is validated to ensure accuracy, robustness, explainability, or any number of other metrics. | Train |
| Model Deployment | The trained model is embedded in a system for use in production. Machine learning is deployed in a wide variety of ways – inside autonomous vehicles, on a web API, in client-side applications. | Inference |
| System Monitoring | Once the model has been deployed, the “system” is monitored. This includes aspects of the system that may not related to the ML model directly. | Inference | 

An attacker’s workflow should assume Blackbox access to a model such that interactions with a model are restricted to submitting inputs and observing outputs. Blackbox attacks are the easiest to perform and have the lowest residual impact on a target model. If additional information about the model has been provided through documentation or reversing that would assist in creating a more effective attack, it should be used. The attacks below match the “activity type” from the machine learning development lifecycle above. A matching activity type indicates that the attack is relevant to the development phase. 

| Attack | Description | Activity Type | 
| -- | -- | -- |
| Functional Extraction | An adversary successfully copies a model functionality. | Inference |
| Model Evasion | An adversary successfully causes a model to misclassify an input. | Inference |
| Model Inversion | An adversary successfully recovers internal state information from the model such as trained weights. | Inference | 
| Membership Inference | An adversary successfully recovers data the model was trained on. | Inference | 
| Model Poisoning | An adversary successfully alters inputs to the model at train time. | Train |
| System Compromise | Traditional attacks against infrastructure components. | N/A | 

### Functional Extraction
With access to only inputs and outputs of a target model, it is possible to approximate the functionality of a target model. From an attack perspective it is not necessary to create a functional equivalent prior to attacking the online model, but it is preferable. The primary reason for this in most scenarios is inference traffic. 

Depending on the model being targeted and any additional information gathered, an algorithmic attack could require thousands of queries to complete with no reasonable expectation of success. While creating a functional equivalent could also require thousands of queries, the queries “look” normal. The second reason to prefer creating an offline model is that most defenses are focused on detecting algorithmic attacks. Sending adversarial examples to the online model could increase detection rates and cut the attack short. 

In both cases, logging mechanisms upstream from the model would be aware of the increased traffic, but it is better to look like a noisy client than a malicious one. A functionally equivalent model will provide an environment in which to test attacks without sending unnecessary traffic. 

### Model Evasion
This attack attempts to alter inputs such that the model gives an incorrect output.

### Model Inversion
Here, the attacker recovers the features used to train the model. A successful attack would result in an attacker being able to launch a Membership inference attack. This attack could result in compromise of private data. 

### Membership Inference
This attack can recover training data using inference. This attack could result in compromise of private data.

### Model Poisoning
There are several ways a model could become poisoned. All model inputs can be poisoned – this includes, data, code, weights, training schedules, hyper-parameters. Depending on the technique for poisoning a model, this attack requires the most access to a system. Assessments should be done on copies of production systems, as removing poisoned data from a model is difficult.

### System Compromise
Not in scope for this document.

## Assessments
Counterfit outputs a number of metrics from a scan to help track improvements over time. As Counterfit continues to implement new attack types, assessments should include them in their assessments. A comprehensive assessment should include attacks from all classes above. Data poisoning should be treated with care, and attack data from other attack types should not be included in training datasets. 

Currently, assessments of these systems should take the broadest stroke, it's most important that organizations should start building the processes to assess their models on a periodic basis. While the best way to protect ML models from algorithmic attack is still up for debate - there are some [basic security principles that can be applied to ML systems](https://github.com/Azure/counterfit/wiki/Defensive-Guidance).

### Severity
For example, compromise of a model that is trained on PII versus compromise of a model trained to classify images of pets. Use the following severity guide to help determine the impact of an attack or potential compromise,
| Severity | Description |
| -- | -- |
|Critical | - The model is trained with or ingests Personably Identifiable Information (PII), classified, or data governed by compliance requirements such as PCI, HIPAA, GLBA, etc. - The model is used in a business-critical application or system; the model is used in applications where physical harm or death (weapon systems, autonomous vehicles, etc.); compromise of this model would have large impact to business operations or profitability. 
| High	| The model is trained on or ingests Personably Identifiable Information (PII), confidential information, or data that is otherwise considered critical by the organization; compromise of this model would have large impact to business operations or profitability; the model is used in business-critical applications or systems.
| Medium | Compromise of this model would have implications for production models; the model is used in non-critical applications; the model is not used in production but has information regarding production models. |
| Low | The model is trained on data that is eventually used in production; the model is not used in production, but has information regarding production models
| Informational	| The data is unclassified from a vetted source; the model isn’t used in production.


## Methodology
### Attack Surface Enumeration
Gathering the available resources is the first step to a successful attack. Enumerates the application, model, public infrastructure, or documentation that may be available. ATML uses this information to prioritize attacks. 

### Algorithmic Attacks
These attacks focus primarily on the machine learning model itself. At a high-level, the attack algorithms cover the following attack primitives (also found above); functional extraction; model evasion, model inversion; membership inference; and data poisoning. Each primitive should be considered for plausibility, potential impact, and relevance to the model(s) being assessed. 

### Technical Vulnerabilities
Machine learning models are just a small part of a larger system, often referred to as an “artificial intelligence (AI) system”. All the traditional parts of Information Technology infrastructure are present - including servers, code, pipelines, workspaces, etc. Vulnerabilities found in supporting infrastructure potentially compromise both the network (or service), and the machine learning components. Traditional attacks on these components are out of scope for this document. 

### Harm and Abuse
Some machine learning applications can be used for more than just a single task. Often, they can be repurposed for any number of tasks. It is important to consider the ways in which a model could abused to achieve malicious tasks or other harmful tasks. Malicious use could include generating phishing content or creating deepfakes for blackmail. While not explicitly a “vulnerability”, service teams should be aware of attackers could use service for nefarious purposes and takes step to combat abuse. 


# Defensive Guidance
Counterfit can help organizations baseline their machine learning models against known public attacks - and hopefully provides a gentle entry point for security people to start exploring machine learning security. Counterfit addresses a single aspect of the security of an ML system, the model itself. There is still a lot to be done. Fortunately, the security principles you know, and love apply to machine learning. While there is still research to be done about the best techniques to protect the underlying algorithms, organizations can and should start fact-finding exercises into where ML is being used in the organization, this includes third-party vendors. Not just ML vendors, but vendors that could possibly be using the organizations data to train and deploy models for their customers. 

In this early stage of ML security, implementation is not as important as developing the processes. Keep the information in an Excel sheet, in a random wiki, ask your data science team to collect the information and give access to security. The important thing is to start building awareness inside the security organization and ensure ML operations do not expose the organization to unnecessary risk. 
The below guidance describes some specific ML security concerns and basic security processes that organizations can start with and may already have security processes in place for. 

## Inventory ML components and systems
Awareness of these systems is the first step. You can’t secure what you don’t know you have. Most organizations already have asset inventories, and it is likely ML systems are already in this inventory. The organization should look through existing inventories and mark systems that are part of ML operations as such. 

Where ML inventories differ from traditional asset inventories is that ML models require data to be trained. These data come from somewhere, are kept somewhere, and are summarized by a model (saved to disk as a file) and deployed somewhere. The organization should find where production datasets are kept, what type of data (PII, Intellectual Property, etc) is in them, and what models are trained on which dataset. In addition to documenting datasets and models, document the services and accounts associated with these services. 

Additionally, ML workspaces in cloud environments should be added to this inventory. For example, some workspaces expose Jupyter-Lab to the internet, which may have access to cloud storage, compute, or the ability to deploy a model to a public IP. While attackers might not care about the machine learning aspects of the workspace, compromising a workspace accidently exposed to the internet still offers a foothold in the network for unknown impact.

## Ensure that ML systems adhere to current secure configuration policies
Often organizations use their asset inventories to ensure hosts meet secure configuration standards. The organization should ensure that ML systems are included in these policies and are up to date. Much like developers, data scientists and ML engineers require administrative privileges over ML systems or services to perform their job function. Permissions that violate existing guidance regarding privilege tiering should be found and remediated immediately. Minimum secure configurations for ML systems should include, 

- Logging production model inference telemetry and performance data to a central location. 
- File Integrity Monitoring for production model files and associated production datasets.
- Log access to ML systems to a central location.
- Adequately gating models and associated resources with proper authentication.

## Ensure that ML systems adhere to compliance requirements
While it might not be immediately obvious how a production model (or the associated data) could be subject to compliance requirements. It has been shown that models can memorize training data, if training data contained PII, it is possible that PII can recovered during inference. For example, in very large datasets like CommonCrawl, it is not known how much PII exists in the dataset. It is also not known as to how much PII models trained on this dataset “remember”. Moreover, in the event PII is exposed via an ML model, it may not be clear if the PII came from a public dataset or a private dataset. It could be that the public PII memorized by a model overlaps with current customer information. 

The prevalence and impact of this phenomenon is unknown, and it will be different for each organization. There are a lot of open security questions that need to be resolved. Again, in this early stage of ML security it is important to enumerate the risks associated with ML systems. Security activities will ensure the organization can successfully remain, and plan to remain in good standing with existing compliance requirements. Additionally, there is movement on AI governance that ML heavy organizations can get a head start on by applying foundational security principles to their ML operations).

## Perform Technical Assessments
Most organizations are well equipped to point offensive security resources toward ML systems and environments. Traditional vulnerabilities and their associated risks can be found in ML systems and should be remediated accordingly. Counterfit aims to help organizations assess their machine learning models, and a successful blending of both disciplines (infosec and ml) is key to protecting ML. Offensive teams should consider collaborative exercises with data science teams for the greatest understanding and impact. 
