# ThinkingToCoding_Kanagavel  
## The Decision Maker – FastAPI Number Analyzer API

---

##  Project Overview

This project is a **FastAPI-based backend application** that analyzes numbers using decision-making logic and stores results in **MongoDB**.

It evaluates each number based on two conditions:

- Whether the number is **positive, negative, or zero**
- Whether the number is **even or odd**

The application exposes **RESTful APIs** to perform **CRUD operations** on number analysis data.

---

##  Logic Summary

The application uses conditional logic to determine:

- **Positive / Negative / Zero**
- **Even / Odd (using `number % 2 == 0`)**

### Example Outputs:
-  `Positive and Even`
-  `Negative and Odd`
-  `Zero`

---

##  Tech Stack

- **FastAPI** – API framework  
- **MongoDB** – NoSQL database  
- **PyMongo** – MongoDB driver  
- **Python** – Core programming language  

---

##  API Endpoints

### 🔹 1. Create Analysis  
**POST** `/analyze`

- **Description:** Analyze a list of numbers and store results  
- **Query Parameter:**  
  `nums: list[int]`

####  Example:
<img width="882" height="731" alt="image" src="https://github.com/user-attachments/assets/ce9c6593-95c3-4c11-9ef4-414303853509" />


### 🔹 2. Get All Analyses

**GET** `/analyze`

**Description:** Retrieve all stored analyses

**Returns:** List of all records (latest first)

#### Example: 
<img width="1322" height="916" alt="image" src="https://github.com/user-attachments/assets/b1dc669e-7fc4-40b2-af58-25ffdb80c252" />


### 🔹 3. Get Analysis by ID

**GET** `/analyze/{record_id}`

**Description:** Retrieve a specific record

**Validation:** Checks for valid MongoDB ObjectId

#### Example:
<img width="1184" height="905" alt="image" src="https://github.com/user-attachments/assets/7fe3de7a-1750-4cd1-8369-edce3d950fdd" />


### 🔹 4. Update Analysis

**PUT** `/analyze/{object_id}`

**Description:** Update an existing analysis

**Condition:** Number of new inputs must match original input length

#### Example:
<img width="893" height="867" alt="image" src="https://github.com/user-attachments/assets/87ab3fef-b7ff-40ce-93c6-dd2154d35d6e" />


### 🔹 5. Delete Analysis

**DELETE** `/analyze/{record_id}`

**Description:** Delete a specific record

#### Example: 
<img width="1331" height="863" alt="image" src="https://github.com/user-attachments/assets/9fe351ae-9133-457d-93c6-d68a925b06dc" />

