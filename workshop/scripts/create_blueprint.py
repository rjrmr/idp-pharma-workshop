"""Create a BDA blueprint for pharma BMR extraction."""
import boto3
import json

client = boto3.client("bedrock-data-automation", region_name="us-east-1")

schema = json.dumps({
    "class": "Batch Manufacturing Record",
    "description": "Blueprint for extracting fields from handwritten pharmaceutical Batch Manufacturing Records (BMR)",
    "properties": {
        "product_name": {
            "type": "string",
            "inferenceType": "explicit",
            "instruction": "The product name from the batch record. Extract exactly as handwritten."
        },
        "batch_number": {
            "type": "string",
            "inferenceType": "explicit",
            "instruction": "The batch identifier such as BMR-2024-0847. Extract exactly as written."
        },
        "operator_initials": {
            "type": "string",
            "inferenceType": "explicit",
            "instruction": "The operator initials from the signature area of the document."
        },
        "start_timestamp": {
            "type": "string",
            "inferenceType": "explicit",
            "instruction": "The start date and time. Convert to ISO 8601 format YYYY-MM-DDTHH:MM:SS."
        },
        "end_timestamp": {
            "type": "string",
            "inferenceType": "explicit",
            "instruction": "The end date and time. Convert to ISO 8601 format YYYY-MM-DDTHH:MM:SS."
        },
        "equipment_ids": {
            "type": "string",
            "inferenceType": "explicit",
            "instruction": "All equipment IDs listed on the document, comma separated."
        },
        "ingredient_names": {
            "type": "string",
            "inferenceType": "explicit",
            "instruction": "All ingredient names listed on the document, comma separated."
        },
        "ingredient_weights_kg": {
            "type": "string",
            "inferenceType": "explicit",
            "instruction": "All ingredient weights in kilograms, comma separated in same order as ingredient names."
        },
        "ingredient_lot_numbers": {
            "type": "string",
            "inferenceType": "explicit",
            "instruction": "All ingredient lot numbers, comma separated in same order as ingredient names."
        }
    }
})

try:
    resp = client.create_blueprint(
        blueprintName="pharma-bmr-extraction",
        type="DOCUMENT",
        schema=schema,
        blueprintStage="LIVE",
    )
    arn = resp["blueprint"]["blueprintArn"]
    print(f"Blueprint created: {arn}")
except Exception as e:
    print(f"Error: {e}")
