**Python for Data Engineering**

Think of Python in data engineering like a Swiss Army knife for messy data. You use it to grab data, clean it, reshape it, and send it where it needs to go. The job is usually less about fancy code and more about writing reliable little scripts that do boring things really well.

A data engineer often does this:
1. Pull data from somewhere.
2. Clean it up.
3. Save it in a better format.
4. Make sure it doesn’t break tomorrow.

Most Python work in DE is just helping data move from “messy” to “useful.”

**Key ideas:**

1 Lists and dictionaries for rows, records, and nested API responses.

2 Functions for reusable steps like parsing, cleaning, and loading.

3 Exceptions for handling bad files, missing fields, and API failures.

4 Context managers (with) for safe file handling.

5 Logging instead of print() for pipeline visibility.

**File handling: the data mailbox**

Files are everywhere in DE. CSVs, JSONs, logs, exports, backups — basically data mail. Python helps you open the mailbox, sort the letters, and put them in neat folders.

Use the with open(...) as file: statement to ensure files are automatically closed, preventing memory leaks or file locks.

Main idea💡

Use with open(...) so Python closes the file for you. That way you don’t leave the door open and forget about it.

Example:

```
from pathlib import Path

path = Path("data/raw/customers.csv")

with path.open("r", encoding="utf-8") as f:
    content = f.read()
```

- Useful patterns:

   - Use pathlib.Path instead of hardcoding path strings.

   - Check whether a file exists before reading it.

   - Write outputs to a new file, not back over the raw file.

   - Keep raw, staged, and curated files in separate folders.

Fun way to remember it 🤓

Read = “What came in?”

Clean = “What is this chaos?”

Write = “Put it somewhere useful.”

**CSV: the spreadsheet with trust issues**

CSV (Comma seperated values) is just rows and columns pretending to be simple. It looks friendly, but it can still be messy with extra spaces, missing values, and weird formatting.

The built-in csv module is ideal for flat, tabular data while pandas is common when you need faster manipulation or easier transformation. 

For production-grade pipelines, streaming through rows is preferred over loading the entire file into memory to avoid performance bottlenecks.

Example

```
import csv

with open("input.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

cleaned = []
for row in rows:
    cleaned.append({
        "customer_id": row["customer_id"].strip(),
        "email": row["email"].strip().lower(),
        "age": row["age"] or None
    })

with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["customer_id", "email", "age"])
    writer.writeheader()
    writer.writerows(cleaned)
```

What’s happening❓

DictReader turns each row into a dictionary.

strip() removes annoying spaces.

lower() makes emails consistent.

None is better than fake empty junk when you want clean data.

- Practical DE habits:

   - Use DictReader so columns are named.

   - Normalize strings with strip() and lower().

   - Handle blanks as None or empty values consistently.

   - Validate required columns before processing.

Memory trick🧠

CSV says: “I’m just tabular data.”

Reality says: “I may still ruin your afternoon.”

**JSON: the nested onion**

JSON is great because it can hold structured data, but it also loves hiding things inside other things. You often have to peel it like an onion until you get the exact fields you need.

This is crucial for APIs and hierarchical data. 

Example

```
import json

with open("events.json", "r", encoding="utf-8") as f:
    data = json.load(f)

flat = []
for event in data["events"]:
    flat.append({
        "event_id": event["id"],
        "user_id": event["user"]["id"],
        "event_type": event["type"]
    })

with open("events_flat.json", "w", encoding="utf-8") as f:
    json.dump(flat, f, indent=2)
```

What’s happening❓

json.load() reads the file into Python.

Nested objects become dictionaries and lists.

You usually flatten only what downstream systems actually need.

- Useful patterns:

   - Use json.load() for files and json.loads() for strings.

   - Expect nested dictionaries and lists.

   - Flatten only the fields you need.

   - Keep raw JSON if you may need to reprocess later.

   - Use libraries like ijson or streaming patterns for massive, nested JSON payloads to keep memory usage low

Memory trick🧠

JSON is like a backpack. CSV is like a table. One is organized for humans, the other is organized for machines that pretend to be human-friendly.

**APIs: asking for data politely**

APIs are how Python often talks to other systems. Your script sends a request, waits for a response, and then translates the answer into something useful.

They are a major source of data ingestion, and Python is widely used to call them in pipelines. A solid pattern is to make the request, check status, parse JSON, and handle failures cleanly.

Example

```
import requests

url = "https://api.example.com/v1/orders"
headers = {"Authorization": "Bearer YOUR_TOKEN"}

try:
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()
except requests.Timeout:
    print("The API took too long.")
except requests.HTTPError as e:
    print(f"API returned an error: {e}")
except ValueError:
    print("Response was not valid JSON.")
```

- Pipeline habits to follow:

   - Always set a timeout.

   - Use raise_for_status() to fail fast on bad responses.

   - Expect pagination for large datasets.

   - Store the raw API response before transforming it.
    
What to remember💡

Always set a timeout.

Always check for bad responses.

Always expect the API to be dramatic sometimes.

Memory trick 🧠 

Calling an API is like asking a busy coworker for a file:

Be clear.

Be polite.

Don’t wait forever.

Expect excuses.

**Error handling: expect chaos, stay calm**

Data pipelines break for normal reasons: missing files, bad data, API downtime, network failures, and weird formats. 

Good Python code doesn’t panic — it handles the problem and keeps moving when possible.

Example

```
def safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
```

- Good error-handling patterns:

   - Catch specific exceptions, not just except Exception.

   - Structured Logging: Log the error with context, such as file name or record id, ETL ID, timestamps, and error levels. This method is essential when debugging hundreds of concurrent pipelines.

   - Dead Letter Queues: Decide whether the job/pipeline should continue or stop. Instead of letting a pipeline crash on a single malformed record, capture the "failed" data into a separate location (Dead Letter Queue) for later manual inspection while letting the rest of the job finish.

   - Retry Mechanisms: Use retries for transient API/network issues. Implement exponential backoff (increasing wait times between retries) for transient errors like timeouts (HTTP 500, 502, 504) or rate limits (HTTP 429). Libraries like Tenacity make this pattern much cleaner.

   - Idempotency: Design operations so they can be retried multiple times without creating duplicate data or side effects. Use unique identifiers and checkpoints to track progress.


DE mindset:

If the problem is small, skip the bad record.

If the problem is big, stop the job.

If the problem might go away, retry it.

If the problem matters, log it.

Memory trick🧠

Bad data is not a surprise. It’s part of the job description.

- Pipeline thinking: the 5-step dance 🧠 A lot of DE work follows the same rhythm:

  - Extract data from a file, API, or database. aka Read raw input.

  - Validate it so you know it isn’t nonsense. aka Validate expected columns or keys.

  - Transform it into a useful shape. aka Clean and standardize values.

  - Load it into a warehouse, table, or file. aka Write to an output file or database table.

  - Observe it, so you know it worked. aka Log row counts and errors.

Example

```
def transform_customer(row):
    return {
        "customer_id": row["customer_id"].strip(),
        "name": row["name"].strip().title(),
        "country": row["country"].strip().upper()
    }
```

This is where Python shines: small, readable functions that do one thing well.

<!-- Credits from: 
https://www.google.com/, https://www.perplexity.ai/, <br/>

-->
