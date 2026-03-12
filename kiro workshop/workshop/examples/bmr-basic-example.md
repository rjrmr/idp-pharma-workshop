# BMR Basic Extraction — Worked Example

This example walks through the complete end-to-end flow for extracting structured data from a clean Batch Manufacturing Record using the IDP Agent.

## Document

**File:** `workshop/test-data/bmr/bmr-sample-01-clean.pdf`
**Difficulty:** Clean (neat handwriting, all fields filled)
**Product:** Amoxicillin 500mg Capsules
**Batch:** BMR-2024-0847

---

## Step 1: Select the Test Data File

Navigate to the `workshop/test-data/bmr/` directory and locate `bmr-sample-01-clean.pdf`. This is a clean batch manufacturing record with neat handwriting and all fields filled in.

## Step 2: Upload via the Chat Interface

1. Launch the Streamlit chat interface:
   ```bash
   streamlit run workshop/app.py
   ```
2. In the sidebar, use the file uploader to select `bmr-sample-01-clean.pdf`.
3. The interface will display a confirmation that the document has been loaded and is ready for questions.

## Step 3: Submit the Basic Extraction Prompt

Copy and paste the following prompt into the chat input:

```
I've uploaded the batch manufacturing record bmr-sample-01-clean.pdf. Please extract all handwritten fields from this document and return the results as structured JSON, including product name, batch number, ingredient names, weights, lot numbers, equipment IDs, operator initials, and timestamps.
```

## Step 4: Review the Extracted JSON

The IDP Agent processes the handwritten document through the BDA MCP Server and returns the following structured JSON with all BMR fields populated:

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

The Chat Interface renders this JSON in a formatted, readable view using `st.json()`.

### Field Summary

| Field | Extracted Value |
|-------|----------------|
| Product Name | Amoxicillin 500mg Capsules |
| Batch Number | BMR-2024-0847 |
| Ingredients | 3 items (Amoxicillin Trihydrate, Magnesium Stearate, Microcrystalline Cellulose) |
| Equipment IDs | MIX-401, GRAN-205, PRESS-112 |
| Operator Initials | JKL |
| Start Timestamp | 2024-03-15T06:30:00 |
| End Timestamp | 2024-03-15T14:45:00 |

## Step 5: Verify Against the Reference JSON

Save the agent's JSON output to a file (e.g., `output.json`), then run the validation script to compare it against the reference:

```bash
python workshop/scripts/validate_output.py \
  --actual output.json \
  --expected workshop/reference/bmr-sample-01-clean-expected.json
```

**Expected validation output:**

```
Field                                    | Expected              | Actual                | Match
-----------------------------------------|-----------------------|-----------------------|------
document_type                            | batch_manufacturing.. | batch_manufacturing.. | ✓
source_file                              | bmr-sample-01-clea.. | bmr-sample-01-clea.. | ✓
extracted_fields.product_name            | Amoxicillin 500mg .. | Amoxicillin 500mg .. | ✓
extracted_fields.batch_number            | BMR-2024-0847        | BMR-2024-0847        | ✓
extracted_fields.ingredients[0].ingredi..| Amoxicillin Trihyd.. | Amoxicillin Trihyd.. | ✓
extracted_fields.ingredients[0].weight_kg| 25.0                 | 25.0                 | ✓
extracted_fields.ingredients[0].lot_num..| LOT-AM-20240115      | LOT-AM-20240115      | ✓
extracted_fields.ingredients[1].ingredi..| Magnesium Stearate   | Magnesium Stearate   | ✓
extracted_fields.ingredients[1].weight_kg| 0.75                 | 0.75                 | ✓
extracted_fields.ingredients[1].lot_num..| LOT-MG-20240203      | LOT-MG-20240203      | ✓
extracted_fields.ingredients[2].ingredi..| Microcrystalline C.. | Microcrystalline C.. | ✓
extracted_fields.ingredients[2].weight_kg| 12.5                 | 12.5                 | ✓
extracted_fields.ingredients[2].lot_num..| LOT-MC-20240118      | LOT-MC-20240118      | ✓
extracted_fields.equipment_ids[0]        | MIX-401              | MIX-401              | ✓
extracted_fields.equipment_ids[1]        | GRAN-205             | GRAN-205             | ✓
extracted_fields.equipment_ids[2]        | PRESS-112            | PRESS-112            | ✓
extracted_fields.operator_initials       | JKL                  | JKL                  | ✓
extracted_fields.start_timestamp         | 2024-03-15T06:30:00  | 2024-03-15T06:30:00  | ✓
extracted_fields.end_timestamp           | 2024-03-15T14:45:00  | 2024-03-15T14:45:00  | ✓

Total fields: 19
Matched:      19
Mismatched:   0
Result:       PASS
```

All 19 fields match the reference — the extraction is complete and accurate.
