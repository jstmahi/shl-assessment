

## 🚀 How to Test the Live API

The Recommendation Engine is deployed on Render and accessible via a public API. You can test it using **cURL**, **Python**, or **Postman**.

**Base URL:** `https://shl-assessment-ic0a.onrender.com`

### Method 1: Using cURL (Terminal / Command Line)

Run the following command in your terminal to send a POST request with a search query:

```bash
curl -X POST https://shl-assessment-ic0a.onrender.com/recommend \
     -H "Content-Type: application/json" \
     -d '{"query": "python coding"}'

```

### Method 2: Using Python

You can use the `requests` library to query the API programmatically:

```python
import requests
import json

url = "https://shl-assessment-ic0a.onrender.com/recommend"
payload = {"query": "managerial skills"}

try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Recommendations received:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Error: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")

```

### Method 3: Using Postman

1. Open Postman and create a new request.
2. Set the method to **POST**.
3. Enter the URL: `https://shl-assessment-ic0a.onrender.com/recommend`
4. Go to the **Body** tab, select **raw**, and choose **JSON** from the dropdown.
5. Paste the following JSON:
```json
{
    "query": "accounting"
}

```


6. Click **Send** to view the recommended assessments.

### ✅ Expected Response

The API returns a JSON object containing a list of top 5 recommended assessments based on your query:

```json
{
  "recommended_assessments": [
    {
      "name": "Account Manager Solution",
      "url": "https://www.shl.com/...",
      "description": "The Account Manager solution is an assessment...",
      "duration": 30,
      "adaptive_support": "No",
      "remote_support": "Yes",
      "test_type": ["Knowledge & Skills"]
    },
    ...
  ]
}

```

---
