from fastapi import FastAPI, UploadFile
import hashlib

app = FastAPI()
document_cache = {}


@app.post("/hackrx/run")
async def process(request: dict, file: UploadFile):
    # Document processing (cached)
    file_bytes = await file.read()
    file_hash = hashlib.sha256(file_bytes).hexdigest()

    if file_hash not in document_cache:
        clauses = extract_atomic_clauses(file_bytes)
        document_cache[file_hash] = {
            "store": QuantumStore(clauses),
            "clauses": clauses
        }

    results = []
    for q in request["questions"]:
        # Query processing (8 tokens)
        params = decode_query(q)

        # Retrieval (≈50ms)
        clauses = document_cache[file_hash]["store"].retrieve(q)

        # Decision (≈1ms)
        decision = RuleEngine().execute(params, clauses)

        # Verification
        proof = ProofValidator().validate(decision, file_bytes)
        decision["proof"] = proof

        results.append(decision)

    return {"answers": results}