# MongoDB Atlas Setup Guide

> **Prerequisite for Issue #8 — MongoDB persistence.**
> Follow these steps before writing any database code.

---

## Setup Order

Recommended sequence for adding MongoDB to this project:

1. **Create a MongoDB Atlas account** and deploy a free/trial cluster (see below).
2. **Get your connection string** from Atlas and add it to `.env`.
3. **Install the Python driver** (`pymongo` is already in `requirements.txt`).
4. **Verify the connection** by running the helper script (see below).
5. **Design your collections** — start with `users`, `sessions`, `pipelines`, and `appointments`.
6. **Integrate with Streamlit** — save PII detection results to MongoDB.

---

## Step 1 — Set Up Atlas (Free / Trial Cluster)

1. Go to <https://www.mongodb.com/cloud/atlas/register> and sign up (or log in).
2. Click **Build a Database** → choose the **Free** tier (M0 Sandbox) or use your
   Atlas trial credits for an M2/M5 cluster.
3. Pick a cloud provider and region close to you (e.g., AWS `us-east-1`).
4. Set a **Database User** username and password — you will need these for the
   connection string.
5. Under **Network Access**, click **Add IP Address** → **Allow Access from Anywhere**
   (`0.0.0.0/0`) for development.  Restrict this to specific IPs before deploying
   to production.
6. Wait for the cluster to provision (usually under two minutes for the free tier).

---

## Step 2 — Get the Connection String

1. In the Atlas dashboard, click **Connect** on your cluster.
2. Choose **Drivers** → **Python** → **pymongo**.
3. Copy the connection string. It looks like:

   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

4. Replace `<username>` and `<password>` with the database user credentials you
   created in Step 1.

---

## Step 3 — Configure the Project

Add the connection string to a `.env` file in the project root:

```bash
# MongoDB Atlas
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=anonymous_studio
```

> **Never commit `.env` to version control.** The `.gitignore` already excludes it.

Install dependencies (pymongo is already listed):

```bash
pip install -r requirements.txt
```

---

## Step 4 — Verify the Connection

Run the built-in connection test:

```bash
python -c "from mongo_persistence import get_database; db = get_database(); print('Collections:', db.list_collection_names())"
```

If the connection succeeds you will see `Collections: []` (empty list on a fresh
cluster). If it fails, double-check your `MONGODB_URI`, database user password,
and network access whitelist.

---

## Step 5 — Planned Collections

| Collection | Purpose | Key Fields |
|------------|---------|------------|
| `users` | Application users | `user_id`, `username`, `role`, `created_at`, `updated_at` |
| `sessions` | Store PII detection runs | `session_id`, `user_id`, `anonymized_text`, `detected_entities`, `created_at`, `metadata` |
| `pipelines` | Pipeline / workflow states | `pipeline_id`, `title`, `status`, `session_id`, `created_at`, `updated_at` |
| `appointments` | Scheduled appointments | `appointment_id`, `user_id`, `pipeline_id`, `scheduled_at`, `status`, `created_at`, `metadata` |
| `audit_logs` | Track every state change | `timestamp`, `event_type`, `resource_id`, `actor`, `before_state`, `after_state`, `metadata` |

> **Security note:** Do **not** persist raw user input or other direct PII (e.g., `original_text`) in MongoDB. Only store de-identified text and metadata, or, if absolutely required, ensure application-layer encryption with a securely managed key outside the database.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `ServerSelectionTimeoutError` | Check that your IP is whitelisted in Atlas **Network Access**. |
| `AuthenticationFailed` | Verify the username/password in `MONGODB_URI`. Make sure the user is a **Database User**, not your Atlas login. |
| `dnspython` import error | Ensure `pymongo` is installed with SRV support: `pip install "pymongo[srv]"`. Only install `dnspython` directly (`pip install dnspython`) if you are using plain `pymongo` without the `[srv]` extra. |
| Slow first connection | Normal for free-tier clusters that have been idle. Atlas pauses M0 clusters after inactivity. |

---

## Next Steps

After verifying the connection, proceed to:

- **Issue #8:** Implement CRUD helpers in `mongo_persistence.py`.
- **Issue #17:** Save de-identification sessions.
- **Issue #15/#16:** Create and manage pipelines.
- **Issue #19:** Write and display audit log entries.
