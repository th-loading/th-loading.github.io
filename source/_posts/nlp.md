---
title: CS224N NLP
date: 2023-07-20 16:24:14 
tags: NLP
---

# 前置知识

## Encode 

### embedding 

将词汇表示出来 one-hot  每个词都是正交向量，如何表示相似性。

dense vector: a word meaning is given by the words that frequently appear close-by 

word embedding  - similiar contexts  vector length (dimention) 维度

word2vec： framework in 2013 for learning word vectors
借助中间词预测context，通过极大似然求解最优的word vectors。定义center work 和 context word 两个vector，基于相似度的权重。指数化可以避免小于0的值 - softmax。 参数为所有词的所有向量。
