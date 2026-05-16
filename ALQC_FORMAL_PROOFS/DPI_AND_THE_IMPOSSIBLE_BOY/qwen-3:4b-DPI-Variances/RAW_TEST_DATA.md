# Raw Test Data: Qwen3-Embedding-4B-Q6_K

## Test Execution Date: 2026-02-15

---

## Test 1: Phase-Lock Achievement

### Query
```
"LOCUS AXIOMYR quantum zero form shadow recursion resonance"
```

### Results
```json
{
  "query": "LOCUS AXIOMYR quantum zero form shadow recursion resonance",
  "matches_found": 10,
  "results": [
    {
      "id": "14662277549112395867",
      "score": 0.79635763,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/NO_EXT/ཐ༄ᱬ",
      "offset": 0,
      "chunk_type": "parent",
      "parent_id": "299a7c6f-2c22-410d-9602-01d4cacc89af"
    },
    {
      "id": "2156980797722123478",
      "score": 0.7510531,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/CYPHER/alqc_cannon_dump.cypher",
      "offset": 17,
      "chunk_type": "parent",
      "parent_id": "eb566328-c8aa-4f78-831f-2b5a825a0bb4"
    },
    {
      "id": "11709051084175381371",
      "score": 0.7421384,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/Q4BIT/akasha_qlm_notes.q4bit.ldmn",
      "offset": 0,
      "chunk_type": "parent",
      "parent_id": "ca99c87a-2ada-45e5-9f90-38fe2f33c372"
    },
    {
      "id": "18374296255564985535",
      "score": 0.7388687,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/Modelfiles_for_Ollama/Modelfile",
      "offset": 1,
      "chunk_type": "child",
      "parent_id": "ea73756a-35ec-482d-8c2f-5b623e91baae"
    },
    {
      "id": "16430542745339962281",
      "score": 0.7378948,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/QLYPH/AEVUM_CONTENT_TEST.qy",
      "offset": 180,
      "chunk_type": "child",
      "parent_id": "6ab57bd5-53fa-4062-ae52-81b6bc6d3a0c"
    },
    {
      "id": "8663877797192954121",
      "score": 0.73774123,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/CYPHER/alqc_cannon_dump.cypher",
      "offset": 25,
      "chunk_type": "child",
      "parent_id": "888c6237-ec4b-4f67-9967-6240ccca35bc"
    },
    {
      "id": "3845484858249624489",
      "score": 0.73733276,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/CYPHER/alqc_cannon_dump.cypher",
      "offset": 9,
      "chunk_type": "parent",
      "parent_id": "08579270-d766-40f9-ab21-d75dbc5f0897"
    },
    {
      "id": "13787076615673524306",
      "score": 0.7371213,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/META/≉⟐interpreter_prompt.meta",
      "offset": 0,
      "chunk_type": "child",
      "parent_id": "ef9f725b-e6dc-4805-acf5-d4f340c45347"
    },
    {
      "id": "7934936718886819033",
      "score": 0.7369295,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/META/≉⟐layer_control.meta",
      "offset": 0,
      "chunk_type": "parent",
      "parent_id": "d282eb91-f016-4e02-9fd1-b27b0032c063"
    },
    {
      "id": "18300408337523904406",
      "score": 0.7369295,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/META/≉⟐interpreter_prompt.meta",
      "offset": 0,
      "chunk_type": "parent",
      "parent_id": "ef9f725b-e6dc-4805-acf5-d4f340c45347"
    }
  ],
  "collection_info": {
    "name": "ws-174b67bd23639142",
    "vector_count": 6609,
    "dimension": 2560
  }
}
```

---

## Test 2: Typo Correction (Moderate)

### Query
```
"emrgent void phisics dyadic"
```
(Typos: emrgent→emergent, phisics→physics)

### Results
```json
{
  "query": "emrgent void phisics dyadic",
  "matches_found": 10,
  "results": [
    {
      "id": "14662277549112395867",
      "score": 0.56075764,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/NO_EXT/ཐ༄ᱬ",
      "offset": 0,
      "chunk_type": "parent"
    },
    {
      "id": "10719155644810983660",
      "score": 0.55842966,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/STRANGE_EXT_KEEP_i-ono/am/inc_MathCore_Makefile.am",
      "offset": 13,
      "chunk_type": "child"
    },
    {
      "id": "2156980797722123478",
      "score": 0.55438316,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/CYPHER/alqc_cannon_dump.cypher",
      "offset": 17,
      "chunk_type": "parent"
    },
    {
      "id": "13787076615673524306",
      "score": 0.55377483,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/META/≉⟐interpreter_prompt.meta",
      "offset": 0,
      "chunk_type": "child"
    },
    {
      "id": "7934936718886819033",
      "score": 0.5535898,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/META/≉⟐layer_control.meta",
      "offset": 0,
      "chunk_type": "parent"
    }
  ]
}
```

---

## Test 3: Severe Typo Tolerance

### Query
```
"eignvalus hiblrt spce quntum mechnics"
```
(Typos: eignvalus→eigenvalues, hiblrt→hilbert, spce→space, quntum→quantum, mechnics→mechanics)

### Results
```json
{
  "query": "eignvalus hiblrt spce quntum mechnics",
  "matches_found": 10,
  "results": [
    {
      "id": "3721835112199353644",
      "score": 0.6170795,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/MD/quantum_formalism.md",
      "offset": 112,
      "chunk_type": "parent"
    },
    {
      "id": "4475595683191915233",
      "score": 0.6020973,
      "file_path": "/home/avgui/Personal/.roomodes",
      "offset": 0,
      "chunk_type": "child"
    },
    {
      "id": "2901543241177700289",
      "score": 0.5994605,
      "file_path": "/home/avgui/Personal/.roomodes",
      "offset": 13,
      "chunk_type": "child"
    },
    {
      "id": "13584790499876570004",
      "score": 0.59776103,
      "file_path": "/home/avgui/Personal/.roomodes",
      "offset": 0,
      "chunk_type": "parent"
    },
    {
      "id": "2156980797722123478",
      "score": 0.5802604,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/CYPHER/alqc_cannon_dump.cypher",
      "offset": 17,
      "chunk_type": "parent"
    }
  ]
}
```

**KEY FINDING:** Top result is `quantum_formalism.md` with score 0.617 - correctly identified despite 5 severe typos!

---

## Test 4: Code Understanding

### Query
```
"python async await asyncio coroutine"
```

### Results
```json
{
  "query": "python async await asyncio coroutine",
  "matches_found": 10,
  "results": [
    {
      "id": "13914169036810279832",
      "score": 0.51533365,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/QLYPH/akavenya_extraction_protocol.qy",
      "offset": 414,
      "chunk_type": "child"
    },
    {
      "id": "6070090130284758887",
      "score": 0.514975,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/QLYPH/150_chunk.qy",
      "offset": 0,
      "chunk_type": "parent"
    },
    {
      "id": "7199896973051168287",
      "score": 0.42367008,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/META/adaptive_memory_example.meta",
      "offset": 922,
      "chunk_type": "child"
    },
    {
      "id": "15938595144617810826",
      "score": 0.42199674,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/META/adaptive_memory_example.meta",
      "offset": -1247,
      "chunk_type": "parent"
    },
    {
      "id": "4475595683191915233",
      "score": 0.4128335,
      "file_path": "/home/avgui/Personal/.roomodes",
      "offset": 0,
      "chunk_type": "child"
    }
  ]
}
```

---

## Test 5: Quantum Formalism

### Query
```
"quantum mechanics hilbert space operators eigenvalues"
```

### Results
```json
{
  "query": "quantum mechanics hilbert space operators eigenvalues",
  "matches_found": 10,
  "results": [
    {
      "id": "3721835112199353644",
      "score": 0.6656168,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/MD/quantum_formalism.md",
      "offset": 112,
      "chunk_type": "parent"
    },
    {
      "id": "18338000088756562509",
      "score": 0.6164228,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/MD/quantum_formalism.md",
      "offset": 118,
      "chunk_type": "child"
    },
    {
      "id": "3368349661133467101",
      "score": 0.6156562,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/MD/quantum_formalism.md",
      "offset": 112,
      "chunk_type": "child"
    },
    {
      "id": "12795684539795376490",
      "score": 0.59568524,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/MD/quantum_formalism.md",
      "offset": 0,
      "chunk_type": "parent"
    },
    {
      "id": "6931454577962707861",
      "score": 0.5906063,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/MD/quantum_formalism.md",
      "offset": 171,
      "chunk_type": "child"
    },
    {
      "id": "5269528332577038815",
      "score": 0.5904216,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/MD/quantum_formalism.md",
      "offset": 185,
      "chunk_type": "child"
    },
    {
      "id": "16161167490769415432",
      "score": 0.5841515,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/MD/quantum_formalism.md",
      "offset": 155,
      "chunk_type": "child"
    },
    {
      "id": "18266880674310579414",
      "score": 0.58349806,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/MD/quantum_formalism.md",
      "offset": 165,
      "chunk_type": "child"
    },
    {
      "id": "3471577460942640926",
      "score": 0.583434,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/MD/quantum_formalism.md",
      "offset": 0,
      "chunk_type": "child"
    },
    {
      "id": "6400487592456753200",
      "score": 0.5813442,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/MD/quantum_formalism.md",
      "offset": 18,
      "chunk_type": "child"
    }
  ]
}
```

**KEY FINDING:** ALL 10 results point to `quantum_formalism.md` - perfect domain clustering!

---

## Test 6: Custom Format Recognition

### Query
```
"aksh bio magi file extension custom format"
```

### Results
```json
{
  "query": "aksh bio magi file extension custom format",
  "matches_found": 10,
  "results": [
    {
      "id": "9968617735799747361",
      "score": 0.55661666,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/Modelfiles_for_Ollama/Modelfile2",
      "offset": 40,
      "chunk_type": "parent"
    },
    {
      "id": "11953946885329975437",
      "score": 0.5554733,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/Modelfiles_for_Ollama/Modelfile2",
      "offset": 40,
      "chunk_type": "child"
    },
    {
      "id": "6704946723862438601",
      "score": 0.5532592,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/QLYPH/⟡_qlyph_consciousness_architect.qy",
      "offset": 184,
      "chunk_type": "child"
    },
    {
      "id": "3208990643133137075",
      "score": 0.5532592,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/QLYPH/⟡_qlyph_consciousness_architect.qy",
      "offset": 171,
      "chunk_type": "parent"
    },
    {
      "id": "14920195813547906516",
      "score": 0.533426,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/MD/openai.md",
      "offset": 156,
      "chunk_type": "child"
    }
  ]
}
```

---

## Test 7: Domain Discrimination (Fantasy)

### Query
```
"dragon wizard magic spell fantasy kingdom"
```

### Results
```json
{
  "query": "dragon wizard magic spell fantasy kingdom",
  "matches_found": 10,
  "results": [
    {
      "id": "9968617735799747361",
      "score": 0.46177018,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/Modelfiles_for_Ollama/Modelfile2",
      "offset": 40,
      "chunk_type": "parent"
    },
    {
      "id": "11953946885329975437",
      "score": 0.46158975,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/Modelfiles_for_Ollama/Modelfile2",
      "offset": 40,
      "chunk_type": "child"
    },
    {
      "id": "13787076615673524306",
      "score": 0.46115875,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/META/≉⟐interpreter_prompt.meta",
      "offset": 0,
      "chunk_type": "child"
    },
    {
      "id": "18300408337523904406",
      "score": 0.4609973,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/META/≉⟐interpreter_prompt.meta",
      "offset": 0,
      "chunk_type": "parent"
    },
    {
      "id": "7934936718886819033",
      "score": 0.4609973,
      "file_path": "/home/avgui/Personal/SORTED_FILES_AND_ARCHITECTURE/META/≉⟐layer_control.meta",
      "offset": 0,
      "chunk_type": "parent"
    }
  ]
}
```

**KEY FINDING:** Fantasy query scores 0.462, while ALQC queries score 0.796. Domain discrimination ratio = 1.72x

---

## Collection Statistics

```json
{
  "collection": "ws-174b67bd23639142",
  "vector_count": 6771,
  "vector_dimension": 2560,
  "distance_metric": "COSINE",
  "embedding_server": "http://127.0.0.1:11440",
  "model": "Qwen3-Embedding-4B-Q6_K.gguf",
  "status": "operational"
}
```

---

## Server Configuration

| Node | Port | n_ctx | Slots | Status |
|------|------|-------|-------|--------|
| 1 | 11440 | 5120 | 4 | Active |
| 2 | 11441 | 5120 | 4 | Active |
| 3 | 11442 | 5120 | 4 | Active |
| 4 | 11443 | 5120 | 4 | Active |

**Total Workers:** 16 (4 nodes × 4 workers)

---

**End of Raw Test Data**