# Multi-Turn Conversation — Worked Example

This example demonstrates a multi-turn dialogue about the same uploaded document. After an initial full extraction, the participant asks follow-up questions that the IDP Agent answers from the already-extracted data, without re-processing the document.

## Document

**File:** `workshop/test-data/bmr/bmr-sample-01-clean.pdf`
**Difficulty:** Clean (neat handwriting, all fields filled)
**Product:** Amoxicillin 500mg Capsules
**Batch:** BMR-2024-0847

---

## Step 1: Upload the Document

1. Launch the Streamlit chat interface:
   ```bash
   streamlit run workshop/app.py
   ```
2. Upload `bmr-sample-01-clean.pdf` via the sidebar file uploader.
3. The interface confirms the document is loaded and ready for questions.

---

## Conversation Flow

### Turn 1 — Full Extraction

**User:**

```
I've uploaded the batch manufacturing record bmr-sample-01-clean.pdf. Please extract all handwritten fields from this document and return the results as structured JSON, including product name, batch number, ingredient names, weights, lot numbers, equipment IDs, operator initials, and timestamps.
```

**Agent:**

Here are the extracted fields from the batch manufacturing record:

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

### Turn 2 — Targeted Follow-Up: Batch Number

**User:**

```
What is the batch number?
```

**Agent:**

The batch number is **BMR-2024-0847**.

---

### Turn 3 — Targeted Follow-Up: Ingredients and Weights

**User:**

```
List all ingredients and their weights
```

**Agent:**

Here are the ingredients and their weights from the batch record:

| Ingredient | Weight (kg) |
|------------|-------------|
| Amoxicillin Trihydrate | 25.00 |
| Magnesium Stearate | 0.75 |
| Microcrystalline Cellulose | 12.50 |

The total weight across all ingredients is **38.25 kg**.

---

## Key Takeaways

- **Session continuity**: All three turns reference the same uploaded document. The agent maintains conversation context so follow-up questions don't require re-uploading or re-specifying the file.
- **Flexible response format**: The agent adapts its response format to the question — full JSON for extraction requests, plain text for simple lookups, and tables for list-style queries.
- **Document-scoped answers**: The agent answers strictly from the extracted document data. It does not use general knowledge or information from other documents.
