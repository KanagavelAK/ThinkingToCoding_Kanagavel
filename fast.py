from fastapi import FastAPI, HTTPException, Query
import re
from pymongo import MongoClient, errors
from datetime import datetime
from bson import ObjectId
from config import MONGO_URI, DB_NAME, COLLECTION_NAME


# -----------------------------
# FastAPI Initialization
# -----------------------------
app = FastAPI(title="Simple Number Analyzer")


# -----------------------------
# MongoDB Connection Function
# -----------------------------
def init_connection():
    try:
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000
        )

        # Force connection check
        client.admin.command('ping')
        return client

    except errors.ConfigurationError as e:
        raise HTTPException(status_code=500, detail=f"MongoDB Configuration Error: {e}")

    except errors.ServerSelectionTimeoutError:
        raise HTTPException(status_code=500, detail="Could not connect to MongoDB server. Check your internet or URI.")

    except errors.ConnectionFailure:
        raise HTTPException(status_code=500, detail="MongoDB Connection Failed.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected MongoDB Error: {e}")


# -----------------------------
# POST Endpoint: Create new analysis
# -----------------------------
@app.post("/analyze")
def create_analysis(nums: list[int] = Query(..., description="List of numbers to analyze")):
    try:
        client = init_connection()
        try:
            db = client[DB_NAME]
            collection = db[COLLECTION_NAME]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database access error: {e}")

        if not nums:
            raise HTTPException(status_code=400, detail="Please enter at least one number.")

        num_list = nums

        results = []
        for num in num_list:
            try:
                if num > 0:
                    result = "Positive and Even" if num % 2 == 0 else "Positive and Odd"
                elif num < 0:
                    result = "Negative and Even" if num % 2 == 0 else "Negative and Odd"
                else:
                    result = "Zero"

                results.append({
                    "number": num,
                    "analysis": result
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error analyzing number {num}: {e}")

        document = {
            "input_numbers": num_list,
            "results": results,
            "created_at": datetime.utcnow()
        }

        try:
            insert_result = collection.insert_one(document)
            if not insert_result.inserted_id:
                raise HTTPException(status_code=500, detail="Data was not inserted.")
        except errors.PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"MongoDB Insert Error: {e}")

        return {
            "message": "Data saved successfully",
            "inserted_id": str(insert_result.inserted_id),
            "results": results
        }

    except HTTPException:
        raise
    except Exception as main_error:
        raise HTTPException(status_code=500, detail=f"Application Error: {main_error}")


# -----------------------------
# GET Endpoint: Retrieve all analyses
# -----------------------------
@app.get("/analyze")
def get_all_analyses():
    try:
        client = init_connection()
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Retrieve all documents, sorted by newest first
        documents = list(collection.find().sort("_id", -1))

        # Convert ObjectId to string for JSON serialization
        for doc in documents:
            doc["_id"] = str(doc["_id"])

        return {
            "message": "Data retrieved successfully",
            "count": len(documents),
            "data": documents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Read Error: {e}")


# -----------------------------
# GET Endpoint: Retrieve a specific analysis by ID
# -----------------------------
@app.get("/analyze/{record_id}")
def get_analysis_by_id(record_id: str):
    try:
        if not ObjectId.is_valid(record_id):
            raise HTTPException(status_code=400, detail="Invalid ID format.")

        client = init_connection()
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        document = collection.find_one({"_id": ObjectId(record_id)})

        if not document:
            raise HTTPException(status_code=404, detail="Record not found.")

        document["_id"] = str(document["_id"])

        return {
            "message": "Record retrieved successfully",
            "data": document
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Read Error: {e}")


# -----------------------------
# PUT Endpoint: Update an existing analysis
# -----------------------------
@app.put("/analyze/{object_id}")
def update_analysis(object_id: str, new_nums: list[int] = Query(..., description="New list of numbers to analyze")):
    try:
        if not ObjectId.is_valid(object_id):
            raise HTTPException(status_code=400, detail="Invalid ID format.")

        client = init_connection()
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Fetch existing document to check length constraints
        existing_doc = collection.find_one({"_id": ObjectId(object_id)})
        if not existing_doc:
            raise HTTPException(status_code=404, detail="Record not found.")

        if not new_nums:
            raise HTTPException(status_code=400, detail="Please enter at least one number.")

        # Ensure the length matches
        original_nums = existing_doc.get("input_numbers", [])
        if len(new_nums) != len(original_nums):
            raise HTTPException(
                status_code=400,
                detail=f"You can only update exactly {len(original_nums)} items. You provided {len(new_nums)} items."
            )

        num_list = new_nums

        results = []
        for num in num_list:
            if num > 0:
                result = "Positive and Even" if num % 2 == 0 else "Positive and Odd"
            elif num < 0:
                result = "Negative and Even" if num % 2 == 0 else "Negative and Odd"
            else:
                result = "Zero"
            results.append({"number": num, "analysis": result})

        update_data = {
            "input_numbers": num_list,
            "results": results,
            "updated_at": datetime.utcnow()
        }

        # Update the document in MongoDB
        update_result = collection.update_one(
            {"_id": ObjectId(object_id)},
            {"$set": update_data}
        )

        return {
            "message": "Record updated successfully",
            "data": update_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Update Error: {e}")


# -----------------------------
# DELETE Endpoint: Delete an analysis
# -----------------------------
@app.delete("/analyze/{record_id}")
def delete_analysis(record_id: str):
    try:
        if not ObjectId.is_valid(record_id):
            raise HTTPException(status_code=400, detail="Invalid ID format.")

        client = init_connection()
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        delete_result = collection.delete_one({"_id": ObjectId(record_id)})

        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Record not found.")

        return {
            "message": f"Record {record_id} deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Delete Error: {e}")