# dropKeys

**dropKeys** is a high-performance, secure web application designed for sharing environment variables, API keys, and sensitive documents with ease. Built with a "security-first" mindset, it combines ephemeral storage with robust encryption to ensure your secrets never stay around longer than they need to.

![Login Page](screenshots/login.png)

## Features

- **End-to-End Encryption**: Every secret is encrypted using AES-256 with a unique, randomly generated key before storage.
- **Self-Destructing Secrets**: Set expiration based on the number of reads or a specific time-to-live (TTL).
- **Direct & Recipient Sharing**: Share via a secure composite link or restrict access to specific Google-authenticated users.
- **Activity Dashboard**: Monitor your sent and received secrets. A blue "new" indicator lets you know when a document hasn't been unsealed yet.
- **Premium Aesthetics**: A sleek, dark-mode interface with snappy transitions and real-time loading feedback.

---

## Getting Started

### 1. Prerequisites
- **Python 3.12+**
- A **PostgreSQL** database (e.g., Neon.tech)
- An **Upstash Redis** instance
- **Google Cloud Console** credentials (for OAuth)

### 2. Installation
Clone the repository and install the dependencies:

```bash
git clone https://github.com/felixLandlord/dropKeys.git
cd dropKeys
# Using uv (recommended)
uv sync
# Or using pip
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory and populate it with your credentials:

```env
GOOGLE_CLIENT_ID="your_google_client_id"
GOOGLE_CLIENT_SECRET="your_google_client_secret"
GOOGLE_REDIRECT_URI="http://localhost:3000"
DATABASE_URL="postgresql://user:pass@host/db"
UPSTASH_REDIS_REST_URL="https://your-redis-url.upstash.io"
UPSTASH_REDIS_REST_TOKEN="your_redis_token"
```

### 4. Database Setup
Initialize the database tables:
```bash
uv run python -c "from dropKeys.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### 5. Running the App
Start the Reflex development server:
```bash
uv run reflex run
```
The app will be available at `http://localhost:3000`.

---

## 🛠️ How It Works

### Sharing a Secret
Enter your secret content, set the project name, and define the expiration rules. You can also add specific recipient emails to restrict access.

![Sharing Interface](screenshots/share.png)

Once shared, you'll receive a unique "Composite Key" URL. This key contains the document ID and the decryption key itself—**the server never stores the decryption key**, meaning only those with the link can ever see the content.

![Share Result](screenshots/share-link.png)

### Unsealing
When a recipient opens a link or clicks "Unseal" in their activity feed, they are prompted to unseal the document.

![Unseal Input](screenshots/unseal.png)

The app then fetches the encrypted payload from Redis, decrypts it locally in the session, and displays the plaintext content.

![Unseal Results](screenshots/unseal-results.png)

### Managing Activity
The dashboard provides a central hub to see everything you've shared or received. New documents are clearly marked with a blue indicator.

![Activity Feed](screenshots/activities.png)

---

## 🛡️ Security Architecture

1.  **Transport**: All communication is secured via HTTPS/WSS.
2.  **Encryption**: Uses `pycryptodome` for AES-256-GCM encryption.
3.  **Storage Isolation**: Metadata (names, dates, recipients) is stored in Postgres, while the encrypted blobs are stored in Upstash Redis with a hardware-enforced TTL.
4.  **Zero-Knowledge Keys**: The encryption keys are included in the URL fragments (hashes) and are never logged or stored in the database.

---

Built using [Reflex](https://reflex.dev)

*Inspired by the original [envshare](https://github.com/chronark/envshare) by chronark.*
