# CertVerify - Certificate Registration & Authenticity Verification

CertVerify is a serverless platform that helps issuers register certificates in a secure registry and allows anyone to verify authenticity later by uploading a certificate PDF.  
It reduces fraud and eliminates manual verification by combining cryptographic hashing with AI-based document extraction.

---

## ✨ Key Features

### ✅ Issuer Portal (Authenticated)

- Secure issuer login via Amazon Cognito
- Upload/register certificate PDFs in the registry
- Automatic extraction of certificate metadata (issuer, recipient, date, etc.)
- Dashboard to view all issued certificates and their status
- Each registered certificate becomes verifiable via the platform

### 🌍 Public Verification (Unauthenticated)

- Anyone can upload a certificate PDF to check authenticity
- Verification is done by computing a SHA-256 hash and matching against registry
- Displays verdict: Authentic / Not Authentic
- Shows extracted certificate details for clarity

---

## 🧭 Workflows

### 1) Issuer: Register a Certificate

1. Issuer logs into Issuer Portal (Cognito)
2. Uploads a certificate PDF
3. UI requests presigned upload URL via API Gateway
4. PDF uploads directly to S3 using presigned URL
5. Parser pipeline processes and stores:
   - SHA-256 hash
   - extracted structured metadata
6. Certificate status becomes `PROCESSED`
7. Certificate can now be verified publicly

### 2) Public: Verify Certificate Authenticity

1. User uploads certificate PDF
2. `verifyCert` lambda computes SHA-256 hash
3. System looks up hash in registry (DynamoDB)
4. Returns authenticity verdict and details

---

## 🏗 Architecture Overview

### Frontend

- Static SPA hosted on S3
- Served globally via CloudFront
- Tailwind CSS UI
- Cognito Hosted UI for issuer authentication

### Backend (Serverless)

- API Gateway — REST endpoints
- Lambda — business logic functions
- S3 — certificate storage
- DynamoDB — certificate registry & metadata
- Textract — OCR/text extraction from PDFs
- Bedrock — structure extracted content into JSON

---

## 🔌 APIs

### `POST /certificates` (Issuer Only)

Creates a presigned upload URL and inserts a DynamoDB record in `PENDING_UPLOAD`.

**Request**

```json
{
  "fileName": "certificate.pdf",
  "contentType": "application/pdf"
}
```

**Response**

```json
{
  "upload": {
    "fileId": "<uuid>",
    "uploadUrl": "<presigned-url>",
    "objectKey": "uploads/<uuid>/certificate.pdf",
    "expiresInSeconds": 300
  }
}
```

---

### `GET /certificates/{certificateId}` (Issuer Only)

Returns certificate status and metadata.

**Statuses**

- `PENDING_UPLOAD`
- `PROCESSING`
- `PROCESSED`
- `FAILED`

---

### `GET /certificates` (Issuer Only)

Returns all certificates registered by the logged-in issuer.

---

### `POST /verify` (Public)

Verifies authenticity of uploaded certificate (hash match against registry).

**Response Example**

```json
{
  "verdict": "AUTHENTIC",
  "match": true,
  "certificateId": "uuid",
  "fileHashSha256": "hash",
  "details": {
    "issuer": "ABC University",
    "recipientName": "John Watson",
    "issuedDate": "2025-01-02"
  }
}
```

**Verdict values**

- `AUTHENTIC`
- `NOT_AUTHENTIC`
- `INVALID_FILE`
- `ERROR`

---

## 🧠 Lambda Functions

### 1) `presignUpload` Lambda

- Validates request payload
- Generates unique `certificateId`
- Stores DynamoDB record (`PENDING_UPLOAD`)
- Returns presigned S3 upload URL

---

### 2) `parser` Lambda (S3 Trigger)

Triggered when a new PDF is uploaded to S3.

Responsibilities:

- Validate PDF file (extension, magic bytes, size)
- Compute SHA-256 hash (streamed from S3)
- Extract text using Textract
- Structure extracted data using Bedrock
- Update DynamoDB with:
  - `status=PROCESSED`
  - `extractedData`
  - `fileHashSha256`
  - `fileSizeBytes`
- On failure:
  - `status=FAILED`
  - `failureReason`

---

### 3) `list_certificates` Lambda

- Extracts `userId` from Cognito JWT token (`sub`)
- Queries DynamoDB GSI (`userId-createdAt-index`)
- Returns issuer’s certificates in reverse chronological order

---

### 4) `verifyCert` Lambda

- Accepts uploaded certificate
- Validates PDF
- Computes SHA-256 hash
- Queries DynamoDB by `fileHashSha256`
- Returns verdict:
  - `AUTHENTIC` if hash exists in registry
  - `NOT_AUTHENTIC` otherwise

---

## 🗃 DynamoDB Data Model

### Table: `certificates`

Primary Key:

- `certificateId` (Partition Key)

Attributes:

- `userId` (issuer Cognito `sub`)
- `fileName`
- `s3Key`
- `status`
- `createdAt`, `processedAt`
- `fileHashSha256`
- `fileSizeBytes`
- `extractedData` (JSON string or Map)
- `failureReason`

---

### GSIs

#### 1) `userId-createdAt-index`

Used for issuer dashboard listing.

- PK: `userId`
- SK: `createdAt`

---

## 🖥 UI Hosting (S3 + CloudFront)

Hosting Setup:

1. Upload UI build to S3 bucket
2. Create CloudFront distribution pointing to the S3 origin
3. Set **Default Root Object**: `index.html`
4. Configure SPA routing:
   - CloudFront custom error response:
     - `403` / `404` → `/index.html` with HTTP `200`

---

## ⚙ Environment Variables

Lambda variables:

- `CERTIFICATE_TABLE`
- `CERTIFICATE_BUCKET`
- `USER_INDEX_NAME` (default `userId-createdAt-index`)
- `HASH_INDEX_NAME` (default `fileHashSha256-index`)

---

## 🔐 Security

Issuer Portal:

- Cognito authentication required
- Token passed to API Gateway as:
  - `Authorization: Bearer <id_token>`
- Issuers can only access their own records

Public Verify:

- No authentication required
- Only returns safe metadata

---

## 📈 Observability

- Lambda logs in CloudWatch
- Debugging points:
  - presign URL generation
  - parsing errors (Textract/Bedrock)
  - hash verification match/no-match
  - GSI query issues

---

## 🚀 Roadmap

- Public presign/verify flow
- Download endpoint for issuers (secure presigned GET)
- Stronger fraud checks (hash + extracted field matching)
- QR code `certificateId` lookup

---
