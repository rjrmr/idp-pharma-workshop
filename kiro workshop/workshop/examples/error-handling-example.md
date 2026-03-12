# Error Handling — Partial Document Worked Example

This example demonstrates how the IDP Agent handles a partially filled document where some fields are missing or unreadable. The agent reports missing data as `null` values in the JSON output rather than guessing or failing entirely.

## Document

**File:** `workshop/test-data/bmr/bmr-sample-03-partial.pdf`
**Difficulty:** Partial (some fields left blank, incomplete entries)
**Product:** Ibuprofen 200mg Tablets
**Batch:** BMR-2024-0592

---

## Step 1: Upload the Partial Document

1. Launch the Streamlit chat interface:
   ```bash
   streamlit run workshop/app.py
   ```
2. Upload `bmr-sample-03-partial.pdf` via the sidebar file uploader.
3. The interface confirms the document is loaded. Note that this document has intentionally missing fields to simulate a real-world incomplete batch record.

## Step 2: Submit the Extraction Prompt

Copy and paste the following prompt into the chat input:

```
I've uploaded the batch manufacturing record bmr-sample-03-partial.pdf. Please extract all handwritten fields from this document and return the results as structured JSON, including product name, batch number, ingredient names, weights, lot numbers, equipment IDs, operator initials, and timestamps.
```

## Step 3: Review the JSON Output with Null Values

The IDP Agent extracts what it can read and returns `null` for fields that are missing or unreadable in the document:

```json
{
  "product_name": "Ibuprofen 200mg Tablets",
  "batch_number": "BMR-2024-0592",
  "ingredients": [
    {
      "ingredient_name": "Ibuprofen",
      "weight_kg": 20.00,
      "lot_number": "LOT-IB-20240410"
    },
    {
      "ingredient_name": "Croscarmellose Sodium",
      "weight_kg": null,
      "lot_number": "LOT-CS-20240405"
    }
  ],
  "equipment_ids": null,
  "operator_initials": "TNB",
  "start_timestamp": null,
  "end_timestamp": null
}
```

### Understanding Null Values

The `null` values in the output indicate fields that the agent could not extract from the document:

| Field | Value | Reason |
|-------|-------|--------|
| `product_name` | `"Ibuprofen 200mg Tablets"` | Present and readable |
| `batch_number` | `"BMR-2024-0592"` | Present and readable |
| `ingredients[0].weight_kg` | `20.00` | Present and readable |
| `ingredients[1].weight_kg` | `null` | Weight field was left blank on the form |
| `equipment_ids` | `null` | Equipment ID section was entirely blank |
| `operator_initials` | `"TNB"` | Present and readable |
| `start_timestamp` | `null` | Timestamp field was left blank on the form |
| `end_timestamp` | `null` | Timestamp field was left blank on the form |

The agent does not guess or fabricate values for missing fields. Instead, it returns `null` to clearly indicate that the data was not present or not readable in the source document. This is critical for pharmaceutical compliance — it is better to flag missing data than to introduce incorrect values.

## Step 4: Validate Against the Reference

Run the validation script to confirm the output matches the expected partial reference:

```bash
python workshop/scripts/validate_output.py \
  --actual output.json \
  --expected workshop/reference/bmr-sample-03-partial-expected.json
```

The validation script handles `null` values gracefully — a `null` in the actual output matching a `null` in the reference is reported as a match. This confirms the agent correctly identified which fields were missing.

**Expected validation output:**

```
Field                                    | Expected              | Actual                | Match
-----------------------------------------|-----------------------|-----------------------|------
document_type                            | batch_manufacturing.. | batch_manufacturing.. | ✓
source_file                              | bmr-sample-03-part.. | bmr-sample-03-part.. | ✓
extracted_fields.product_name            | Ibuprofen 200mg Ta.. | Ibuprofen 200mg Ta.. | ✓
extracted_fields.batch_number            | BMR-2024-0592        | BMR-2024-0592        | ✓
extracted_fields.ingredients[0].ingredi..| Ibuprofen            | Ibuprofen            | ✓
extracted_fields.ingredients[0].weight_kg| 20.0                 | 20.0                 | ✓
extracted_fields.ingredients[0].lot_num..| LOT-IB-20240410      | LOT-IB-20240410      | ✓
extracted_fields.ingredients[1].ingredi..| Croscarmellose Sod.. | Croscarmellose Sod.. | ✓
extracted_fields.ingredients[1].weight_kg| null                 | null                 | ✓
extracted_fields.ingredients[1].lot_num..| LOT-CS-20240405      | LOT-CS-20240405      | ✓
extracted_fields.equipment_ids           | null                 | null                 | ✓
extracted_fields.operator_initials       | TNB                  | TNB                  | ✓
extracted_fields.start_timestamp         | null                 | null                 | ✓
extracted_fields.end_timestamp           | null                 | null                 | ✓

Total fields: 14
Matched:      14
Mismatched:   0
Result:       PASS
```

All 14 fields match — including the `null` values for missing data.

## Key Takeaways

- **Null means missing, not error**: The agent uses `null` to indicate data that was not present or not readable in the source document. This is distinct from an extraction error.
- **Partial extraction is valid**: The agent extracts as much as it can and clearly marks what it could not find. It does not fail entirely when some fields are missing.
- **Compliance-safe behavior**: In pharmaceutical manufacturing, reporting missing data as `null` is preferable to guessing. This aligns with ALCOA+ data integrity principles — data should be attributable, legible, contemporaneous, original, and accurate.
- **Validation handles nulls**: The validation script treats `null` values as valid data points and compares them correctly against the reference.
