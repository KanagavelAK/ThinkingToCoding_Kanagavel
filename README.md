# ThinkingToCoding_Kanagavel
## The Decision Maker – Smart Number Checker
## Logic Summary

This program takes a number from the user and checks two conditions using nested and multi-branch logic:

Whether the number is positive, negative, or zero.

Whether the number is even or odd.

It uses nested if–elif–else statements to make decisions step by step.

## Code Summary

Input: Takes an integer value from the user.

Process:
   1. First, checks if the number > 0, < 0, or = 0.
   2. Inside each branch, another condition checks if the number is even or odd using number % 2 == 0.

Output: Displays a clean sentence like:
   1. “Positive and Even”
   2. “Negative and Odd”
   3. “Zero and Even”

## What I Learned

How to use nested if-else statements effectively.

The difference between multi-branch and simple conditional logic.

How to combine multiple logical checks to produce a single clean output.

Importance of code clarity, comments, and structure when using decision-making constructs.

## MongoDB Connection

The application connects to MongoDB using the pymongo library and environment variables stored securely in a configuration file.

It creates a MongoDB client using the connection string (MONGO_URI), then accesses the specified database (DB_NAME) and collection (COLLECTION_NAME).

After analyzing the numbers, the application prepares a document containing:

The list of input numbers

The analysis result for each number

The timestamp of submission

This document is inserted into the MongoDB collection using the insert_one() method.
## Execution 

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/fffc8af2-2bc9-417e-86ad-66a9fb65fa1e" />

<img width="1919" height="1078" alt="image" src="https://github.com/user-attachments/assets/24c19024-f826-44c8-9a68-c39e6e971325" />
