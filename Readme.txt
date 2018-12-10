Information Retrieval Systems:
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Overview:
---------
Phase 1:
Task1:
We have implemented the following retrieval models:
1. BM25
2. tf-idf
3. JM Smoothed Query Likelihood
4. Lucene's default retreival model

Task2:
We also performed query enrichment using psuedo relevance faadback and used the BM25 Model to then rank the documents with based on the enriched query.

Task3:
First, performed stopping on the corpus with no stemming, and then ranked documents using BM25, tf-idf, and JM Smoothed Querylikelihood models in three seprate runs.


Phase 2:
Implemented snippet generation with query term highlighting.


Phase 3:
Performed evaluation of our results using the relvance information provided to us in cacm.rel.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

This Readme contains steps about how to install and run this project on Windows.

These installation steps are pertinent to Windows OS, but the source is good for all other operating systems as well.


System Reuirements:
-------------------

1. Python 2.7, you can download and install it from: https://www.python.org/download/releases/2.7/
2. Lucene 4.7.2, you can download and install lucene from: https://lucene.apache.org/  
                                                           https://archive.apache.org/dist/lucene/java/4.7.2/
3. BeautifulSoup, you can download it from: https://www.crummy.com/software/BeautifulSoup/
   To install BeautifulSoup, go to the directory in which you unzipped BeautifulSoup and run the following command on command prompt:
			"python setup.py install"

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Execution:
----------
Unzip the solution at a certain location in your system and take note of that location. All the source code files have now been unzipped.

Perform the following steps to run the various source code files:

Task 1:
-------

To execute the four Baseline runs perform the following steps:
	1. Open a command prompt instance.
	2. On the command prompt, navigate to the directory in which you unzipped the project.
	3. Navigate to the Task1 folder and execute the following command to use BM25 as the retrieval model:
		"python BM25.py"
	4. The results for the BM25 model will be generated in a folder named "BM_Output".
	5. To use tf-idf as the retrieval model, execute the following command:
		"python tfidf.py"
	6. The results for the tf-idf model will be generated in a folder named "TF-IDF_output".
	7. To use JM Smoothed Query Likelihood Model as the retrieval model, execute the following command:
		"python JM_Retreiver.py"
	8. The results for the JM Smoothed Query Likelihood Model will be generated in a folder named "JM_output".
	9. For Lucene:
		A. Make a new project in Java and use the Lucene.java file provided.
		   Create this project in the same directory and set the path in inputLocation to the path containing Lucene.java.		   
		B. Add the three following jars into your project's list of referenced libraries:
			1. lucene-core-VERSION.jar
			2. lucene-queryparser-VERSION.jar
			3. lucene-analyzers-common-VERSION.jar
		C. TokenizedFile and queries.txt should be in the same directory, and the path should be set for them in the program.
	   	   It will take the documents from TokenizedFile and index them and rank them based on the queries, 
	           the output generated will be in the prog folder with the name LuceneOutput folder where there will be 64 files, one per query
		D. Run the java program.

Task 2:
-------

For Task 2, we chose the BM25 run, to execute the BM25 Model on an enriched query, perform the following steps:
	1. Open a command prompt instance.
	2. On the command prompt, navigate to the directory in which you unzipped the project.
	3. Navigate to the Task2 folder and execute the following command:
		"python BM25WithFeedback.py"
	4. The results will be generated in a folder named "BM_OutputWithFeedback".

Task 3:
-------

The three baseline runs that we chose for task 3 were: BM25, tf-idf, JM Smoothed Querylikelihood model.

	Task 3A:
	-------
	To execute the three runs of Task 3A, perform the following steps:
		1. Open a command prompt instance.
		2. On the command prompt, navigate to the directory in which you unzipped the project.
		3. Navigate to the Task3 folder and then to the Task3A folder inside that.
		4. Then, to use BM25 as the retrieval model, execute the following command:
			"python bm25_stopping.py"
		5. The results will be generated in a folder named "BM_Output_Stopping".
		6. To use tf-idf as the retrieval model, execute the following command:
			"python tfidf_stopping.py"
		7. The results for the tf-idf model will be generated in a folder named "TF-IDF_Output_Stopping".
		8. To use JM Smoothed Query Likelihood Model as the retrieval model, execute the following command:
			"python jm_stopping.py"
		9. The results for the JM Smoothed Query Likelihood Model will be generated in a folder named "JM_Output_Stopping".


	Task 3B:
	-------
	To execute the three runs of Task 3B, perform the following steps:
		1. Open a command prompt instance.
		2. On the command prompt, navigate to the directory in which you unzipped the project.
		3. Navigate to the Task3 folder and then to the Task3B folder inside that.
		4. Then, to use BM25 as the retrieval model, execute the following command:
			"python BM25.py"
		5. The results will be generated in a folder named "BM_Output_Stemming".
		6. To use tf-idf as the retrieval model, execute the following command:
			"python tfidf_stemming.py"
		7. The results for the tf-idf model will be generated in a folder named "TF-IDF_Output_Stemming".
		8. To use JM Smoothed Query Likelihood Model as the retrieval model, execute the following command:
			"python JM_Retreiver.py"
		9. The results for the JM Smoothed Query Likelihood Model will be generated in a folder named "JM_Output_Stemming".


Phase 2:
--------
Displaying Results:
To view the various snippets generated, perform the following steps:
	1. Open a command prompt instance.
	2. On the command prompt, navigate to the directory in which you unzipped the project.
	3. Navigate to the "Snippet generation" folder.
	4. Then, execute the following command:
		"python SnippetGeneration.py"
	5. The results will be generated in a folder named "snippet_output".



Phase 3:
--------
Evaluation:
To view the various snippets generated, perform the following steps:
	1. Open a command prompt instance.
	2. On the command prompt, navigate to the directory in which you unzipped the project.
	3. Navigate to the Phase3 folder.
	4. Then, execute the following command:
		"python Evaluation.py"
	5. The results will be generated in the following folders:
		for BM25 : 				BM_EvaluationOutput
		for BM25 with stopping : 		BM_Evaluation_Stopping_Output
		for BM25 with query enrichment :	BM_QueryEnrichmentEvaluationOutput
		for JM smoothed Querylikelihood :	JM_EvaluationOutput
		for JM with stopping :			JM_Evaluation_Stopping_Output
		for Lucene :				Lucene_EvaluationOutput
		for tf-idf :				TF-IDF_EvaluationOutput
		for tf-idf with stopping :		TF-IDF_Evaluation_Stopping_Output
	6. The Recall-Precision curve is present with the name Recall-Precision Curve.png


Extra Credit:
-------------

To run the extra credit part of our source code:
	1. Open a command prompt instance.
	2. On the command prompt, navigate to the directory in which you unzipped the project.
	3. Navigate to the Extra folder.
	4. Then, execute the following command:
		"python query_runner.py"
	5. You'll see the following message:
		"Enter Query:"
	6. Enter the query here in double quotes, for example: "operating system"
	7. Next, you'll see the following message:
		"Enter 1 for exact match 2 for best match 3 for best match ordered"
	8. Here, enter 1 if you to run Exact match for your query, 2 for Best match, and 3 for Ordered best match within proximity N.
	9. Then, you'll see an ordered list of documents for the query you entered, the format of one result will look something like this:
		"Query" Q0 docId rank score BM25 "Name of retriever system used"