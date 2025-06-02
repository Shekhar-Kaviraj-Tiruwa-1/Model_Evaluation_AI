from datetime import datetime
import os
import json
from typing import Dict, Any, List

class Database:
    def __init__(self):
        # Try to use MongoDB if available, otherwise use local file storage
        self.use_mongodb = False
        self.local_file = "data/evaluations.json"
        
        try:
            from pymongo import MongoClient
            mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
            # Test connection
            self.client.server_info()
            self.db = self.client["modeleval"]
            self.evaluations = self.db["evaluations"]
            self.use_mongodb = True
            print("✓ Connected to MongoDB")
        except Exception as e:
            print(f"⚠ MongoDB not available, using local storage: {e}")
            os.makedirs("data", exist_ok=True)
            if not os.path.exists(self.local_file):
                with open(self.local_file, 'w') as f:
                    json.dump([], f)
        
    def store_evaluation(self, prompt: str, responses: Dict[str, str], metrics: Dict[str, Dict[str, float]]) -> str:
        """Store evaluation results."""
        evaluation_doc = {
            "timestamp": datetime.utcnow().isoformat(),
            "prompt": prompt,
            "responses": responses,
            "metrics": metrics
        }
        
        if self.use_mongodb:
            result = self.evaluations.insert_one(evaluation_doc)
            return str(result.inserted_id)
        else:
            # Store in local file
            try:
                with open(self.local_file, 'r') as f:
                    data = json.load(f)
                data.append(evaluation_doc)
                with open(self.local_file, 'w') as f:
                    json.dump(data, f, indent=2)
                return f"local_{len(data)}"
            except Exception as e:
                print(f"Error storing locally: {e}")
                return "error"
    
    def get_evaluations(self, limit: int = 100) -> List[Dict]:
        """Retrieve recent evaluations."""
        if self.use_mongodb:
            return list(self.evaluations.find().sort("timestamp", -1).limit(limit))
        else:
            try:
                with open(self.local_file, 'r') as f:
                    data = json.load(f)
                return data[-limit:] if data else []
            except Exception:
                return []
    
    def get_model_statistics(self, model_name: str) -> Dict[str, Any]:
        """Get aggregated statistics for a specific model."""
        pipeline = [
            {"$unwind": "$metrics"},
            {"$match": {"metrics": model_name}},
            {"$group": {
                "_id": None,
                "avg_bert_score": {"$avg": f"$metrics.{model_name}.bert_score"},
                "avg_rouge1": {"$avg": f"$metrics.{model_name}.rouge1"},
                "avg_rouge2": {"$avg": f"$metrics.{model_name}.rouge2"},
                "avg_rougeL": {"$avg": f"$metrics.{model_name}.rougeL"},
                "avg_length": {"$avg": f"$metrics.{model_name}.response_length"},
                "count": {"$sum": 1}
            }}
        ]
        
        result = list(self.evaluations.aggregate(pipeline))
        return result[0] if result else {} 