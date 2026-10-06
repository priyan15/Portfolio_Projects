## Project Ramanujan

A Retrieval-Augmented Generation (RAG) API that enables semantic search and question-answering across technical books, notes, and computer science research papers.

### Motivation

While studying technical topics, information is often scattered across books, documentation, notes, and reference materials.

Traditional search requires manually locating relevant chapters and sections.

Project Ramanujan allows users to ask natural language questions and receive context-aware answers grounded in the source material.

### Features

* Natural Language Question Answering
* Multi document retrieval
* Multi type document ingestion
* REST API built with FastAPI
* Vector Search using embeddings

### Supported Sources

#### Books
* Artificial-Intelligence-A-Modern-Approach-4th-Edition
* Hands-on-Machine-Learning
* Introduction to Machine Learning - Ethem Alpaydin
* math4ml
* mathematics_for_ml-book
* ML Machine Learning-A Probabilistic Perspective
* The Hundred-Page Machine Learning Book
* Fluent-Python-Clear_-Concise-and-Effective-Programming
* Fundamentals of Data Engineering Plan and Build Robust Data
* Spark-The Definitive Guide
* SQL Performance Explained
* Deep Learning with Python - François Chollet - Manning (2018)
* Ian Goodfellow, Yoshua Bengio, Aaron Courville
* UnderstandingDeepLearning_02_09_26_C
* skienathealgorithmdesignmanual
* Build a Large Language Model (From Scratch)
* Reinforcement Learning An Introduction
* Designing_ML_Systems

### Architecture

 PDF Books
      |
      V
 Document Loader
      |
      V
 Text Chunking
      |
      V
 Embedding Model
      |
      V
 ChromaDB
      |
      V
 FastAPI
      |
      V
 Question
      |
      V
 Similarity Search
      |
      V
 Top 5 Chunks
      |
      V
 Qwen 2.5
      |
      V
 Answer + Sources


### API Endpoints
* POST Ingest: Ingest and index documents.
* POST Summarize: Generate summaries from indexed documents.
* POST Ask: Ask natural language questions.
* Get Documents: View indexed knowledge sources.

### Technology Stack

#### Backend:
* FastAPI
* Python

#### Document Processing:
* LangChain

#### Vector Store:
* ChromaDB

#### LLM:
* Qwen 2.5

#### Embeddings:
* BAAI/bge-base-en-v1.5

#### Testing:
* PyTest

#### Chunking Strategy:
Semantic Hybrid Chunking

## Future Enhancements:
LangGraph Exploration--> Some way to incorporate it



## Why Ramanujan?
The project is named after Srinivasa Ramanujan, whose ability to uncover deep relationships from seemingly disconnected information mirrors the goal of Retrieval-Augmented Generation: discovering relevant knowledge from vast collections of documents and synthesizing meaningful answers.


