# Batch Manufacturing Record (BMR) Sample Prompts

This file contains ready-to-use sample prompts for interacting with the IDP Agent using Batch Manufacturing Record test data. Prompts are organized into three categories: basic extraction, targeted extraction, and validation.

---

## 1. Basic Extraction

**Target file:** `bmr-sample-01-clean.pdf`

**Prompt:**

```
I've uploaded the batch manufacturing record bmr-sample-01-clean.pdf. Please extract all handwritten fields from this document and return the results as structured JSON, including product name, batch number, ingredient names, weights, lot numbers, equipment IDs, operator initials, and timestamps.
```

**Expected response:** The agent extracts all handwritten fields from the batch manufacturing record and returns a complete JSON object with all BMR fields populated, including product name, batch number, a list of ingredients with their weights and lot numbers, equipment IDs, operator initials, and start/end timestamps.

**Example expected JSON output:**

```json
{
  "product_name": "Amoxicillin 500mg Capsules",
  "batch_number": "BMR-2024-0847",
  "ingredients": [
    {
      "ingredient_name": "Amoxicillin Trihydrate",
      "weight_kg": 25.00,
      "lot_number": "LOT-AM-20240115"
    },
    {
      "ingredient_name": "Magnesium Stearate",
      "weight_kg": 0.75,
      "lot_number": "LOT-MG-20240203"
    },
    {
      "ingredient_name": "Microcrystalline Cellulose",
      "weight_kg": 12.50,
      "lot_number": "LOT-MC-20240118"
    }
  ],
  "equipment_ids": ["MIX-401", "GRAN-205", "PRESS-112"],
  "operator_initials": "JKL",
  "start_timestamp": "2024-03-15T06:30:00",
  "end_timestamp": "2024-03-15T14:45:00"
}
```

---

## 2. Targeted Extraction

**Target file:** `bmr-sample-01-clean.pdf`

**Prompt:**

```
From the uploaded batch record bmr-sample-01-clean.pdf, extract only the ingredient names and their corresponding weights in kg. Return the results as a JSON array of objects with 'ingredient_name' and 'weight_kg' fields.
```

**Expected response:** The agent extracts only the ingredient names and their corresponding weights from the batch record, returning a focused JSON array containing objects with just the two requested fields.

**Example expected JSON output:**

```json
[
  {"ingredient_name": "Amoxicillin Trihydrate", "weight_kg": 25.00},
  {"ingredient_name": "Magnesium Stearate", "weight_kg": 0.75},
  {"ingredient_name": "Microcrystalline Cellulose", "weight_kg": 12.50}
]
```

---

## 3. Validation

**Target file:** `bmr-sample-01-clean.pdf`

**Prompt:**

```
Extract the batch number and operator initials from bmr-sample-01-clean.pdf. The expected batch number is 'BMR-2024-0847' and the expected operator initials are 'JKL'. Compare your extracted values against these expected values and report whether each field matches.
```

**Expected response:** The agent extracts the batch number and operator initials from the document, compares each extracted value against the provided expected values, and returns a validation report indicating whether each field matches.

**Example expected JSON output:**

```json
{
  "validation_results": [
    {
      "field": "batch_number",
      "extracted": "BMR-2024-0847",
      "expected": "BMR-2024-0847",
      "match": true
    },
    {
      "field": "operator_initials",
      "extracted": "JKL",
      "expected": "JKL",
      "match": true
    }
  ],
  "overall_match": true
}
```
