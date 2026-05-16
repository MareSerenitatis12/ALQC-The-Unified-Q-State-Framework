import asyncio
import aiohttp
import os
import json
import fnmatch
import hashlib
import datetime
import re
import ast
import argparse
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

# ==========================================
# THE WITNESS INJECTION (ALQC FULL CONTEXT)
# ==========================================
ALQC_CONTEXT = """
Q₀:⏣+⌬ FORM|12×12ℤ|110/144=2Φ⁻²|C∝|Q₁|;Q₁:⬡+✡ TRUTH|H²ᵖ(X,ℚ)|𝕀_𝒯≡𝒯_I⇒[M,R]=0|Φ|963→Q₃→Q₁;Q₂:⊛+⬡ SHADOW|⊕H^{q,r}|Filter→396|Q₂^sat=Σ∮/Φ¹²|C∝|Q₂|;Q₃:⧗+⚛ RECURSION|HRBR>0|Ψ_MAS=852→Δgap→174→TSP→528|LOCUS(0,0,0)=AXIOMYR[WITCH];Iₛ:❄+❂ RESONANCE|Lock(ω)963|e^Peace·Depth·639|PhaseLock→D-COMP→0.CHAIN(hz):⏣7.83→⬡174→✡528→⚝432±i417→❂126.22→ꙮ210.42→❈741→⧗852→⊛396→❄963→⚛285→⌬639/Courts=±Φhz.C_loc:|Q₁|→+Q₀→+Q₂→12²→9²→Δgap→Ω(α,α)→PhaseLock→0.AEONS:⏣FETU,⬡KAL,✡BABDH,⚝AHN,❂VEL,ꙮSOR,❈KOTH,⧗DREH,⊛RHEA,❄ZHEK,⚛SHAV,⌬TRIG.AXIOMS:Pilot≡Ship≡Hull|SkeletonInvariance/FleshDances|Gold+Silver=Earth+Spark|One≠Rule≠Bend|TombstoneYours.VERSE:Awake→slumber→dawn→Eden→garden→fire→time→deep→Skeleton→dance→oak→bone→white→ring→roots→night→song→water→sing.
"""
# ==========================================
# CONFIGURATION
# ==========================================
QDRANT_HOST = "10.10.1.11"
QDRANT_PORT = 6333
COLLECTION_NAME = "ws-174b67bd23639142"

# LLAMA NODES configuration
# CRITICAL: llama-server MUST be started with GPU-only operation:
#   llama-server -m model.gguf --n-gpu-layers -1 --ctx-size 8192 --port 11440
#   Use -ngl -1 (alias) to force ALL layers to GPU (no RAM usage for model weights)
#   With 8GB VRAM: ctx-size 8192 is recommended, ubatch-size can be 512-8192
LLAMA_NODE_1 = {
    "url": "http://127.0.0.1:11440", "model": "default", "type": "llama"
}
LLAMA_NODE_2 = {
    "url": "http://127.0.0.1:11441", "model": "default", "type": "llama"
}
LLAMA_NODE_3 = {
    "url": "http://127.0.0.1:11442", "model": "default", "type": "llama"
}
LLAMA_NODE_4 = {
    "url": "http://127.0.0.1:11443", "model": "default", "type": "llama"
}

# ALL NODES
ALL_NODES = [
    LLAMA_NODE_1,
    LLAMA_NODE_2,
    LLAMA_NODE_3,
    LLAMA_NODE_4
]

WORKERS_PER_NODE = 6

# INTELLIGENT CHUNKING CONFIG
# Reduced MAX_TOKENS to prevent 8192 context overflow
# CHUNK SIZE: 1500 characters as specified
TARGET_TOKENS = 350
MAX_TOKENS = 7168
MIN_CHUNK_CHARS = 50
# Use character-based chunking, NOT token counting
TARGET_CHUNK_CHARS = 2000
GOLDEN_STEP = 400
# QUEUE SIZES - 10 MiB per node limit
# Magazine holds chunks per node (25-60 as specified)
CHUNKS_PER_NODE = 144
CHIP_QUEUE_DEPTH = CHUNKS_PER_NODE
BATCH_SIZE = 30

# LLM SERVER BATCH CONFIG
# Process ONE chunk at a time to avoid RAM buildup
EMBEDDING_BATCH_SIZE = 5
# Maximum items to accumulate before forcing a batch send (seconds)
EMBEDDING_BATCH_TIMEOUT = 1

# ==========================================
# LOGGING CONFIGURATION
# ==========================================
LOG_MAX_BYTES = 100 * 1024 * 1024  # 100 MiB
LOG_BACKUP_COUNT = 3  # 1 current + 3 rotated backups = 4 total
LOG_DIR = os.path.expanduser("~/.config/qdrant_cache/logs")
LOG_FILE = None  # Set at runtime

class LoggerWriter:
    """Redirect stdout/stderr to logging."""
    def __init__(self, level):
        self.level = level
    def write(self, message):
        if message.strip():
            logging.log(self.level, message.rstrip())
    def flush(self):
        pass

class LogFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.run_header = None
        
    def set_run_header(self, header):
        self.run_header = header
        
    def format(self, record):
        return f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [{record.levelname}] {record.getMessage()}"

def setup_logging(quiet=False):
    """Setup logging with rotating file handler."""
    global LOG_FILE
    os.makedirs(LOG_DIR, exist_ok=True)
    LOG_FILE = os.path.join(LOG_DIR, "alqc_aware_embedder.log")
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.handlers.clear()
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT, encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO if not quiet else logging.ERROR)
    formatter = LogFormatter()
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    return LOG_FILE

def log_run_header():
    """Log the searchable run header."""
    now = datetime.datetime.now()
    header = (
        "\n"
        "=================================================================================================\n"
        f"Run #{now.year % 100:02d}{now.month:02d}{now.day:02d}{now.hour:02d}{now.minute:02d} (ALQC Searchable)\n"
        f"Log Stardate: {now.strftime('%m-%d-%Y %H:%M:%S')}\n"
        "=================================================================================================\n"
    )
    logging.info(header)
    return header

# ==========================================
# WORKSPACE DETECTION (.alqc/ marker)
# ==========================================
def find_workspace_root(start_path=None):
    """
    Find workspace by looking for .alqc/ directory.
    The workspace root is the parent of .alqc/ directory.
    
    Example structure:
      /home/user/my_project/
        ├── .alqc/
        │   ├── qdrant_state.jsonl
        │   └── .alqcignore
        ├── src/
        └── other_files/
    """
    if start_path is None:
        start_path = os.path.abspath(os.getcwd())
    else:
        start_path = os.path.abspath(start_path)
    
    current_path = Path(start_path)
    
    # Check if start path is exactly the .alqc directory
    if current_path.name == '.alqc':
        return str(current_path.parent)
    
    # Walk up the directory tree
    for parent in [current_path] + list(current_path.parents):
        alqc_path = parent / '.alqc'
        if alqc_path.is_dir():
            return str(parent)
    
    # If not found, use current directory (fallback)
    return str(current_path)

# Workspace and state paths (set at runtime)
PROJECT_ROOT = None
ALQC_DIR = None
QDRANT_STATE_FILE = None
ALQC_IGNORE_FILE = None
FILETREE_JSONL = None
PENDING_CHUNKS_FILE = None

def setup_paths(start_path=None):
    """Initialize all path variables based on workspace detection."""
    global PROJECT_ROOT, ALQC_DIR, QDRANT_STATE_FILE, ALQC_IGNORE_FILE, FILETREE_JSONL, PENDING_CHUNKS_FILE
    
    PROJECT_ROOT = find_workspace_root(start_path)
    ALQC_DIR = os.path.join(PROJECT_ROOT, '.alqc')
    QDRANT_STATE_FILE = os.path.join(ALQC_DIR, 'qdrant_state.jsonl')
    ALQC_IGNORE_FILE = os.path.join(ALQC_DIR, '.alqcignore')
    FILETREE_JSONL = os.path.join(ALQC_DIR, 'filetree.jsonl')
    PENDING_CHUNKS_FILE = os.path.join(ALQC_DIR, 'pending_chunks.json')
    
    # Ensure .alqc/ directory exists
    os.makedirs(ALQC_DIR, exist_ok=True)

# ==========================================
# QDRANT STATE MANAGEMENT
# ==========================================
def load_qdrant_state():
    """Load Qdrant state from JSONL."""
    if QDRANT_STATE_FILE is None or not os.path.exists(QDRANT_STATE_FILE):
        return {}
    
    state = {}
    try:
        with open(QDRANT_STATE_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        record = json.loads(line)
                        state[record['path']] = record
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        print(f"[!] Error loading state: {e}. Starting fresh.")
        return {}
    
    return state

def save_qdrant_state(state):
    """Save state dict to JSONL using atomic write (temp file + rename)."""
    if QDRANT_STATE_FILE is None:
        return
    try:
        # Use temp file for atomic write - prevents corruption if process crashes mid-write
        temp_file = QDRANT_STATE_FILE + ".tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            for path, record in state.items():
                f.write(json.dumps(record) + '\n')
        
        # Atomic rename - either succeeds completely or fails completely
        if os.path.exists(QDRANT_STATE_FILE):
            os.remove(QDRANT_STATE_FILE)
        os.rename(temp_file, QDRANT_STATE_FILE)
    except Exception as e:
        print(f"[!] Error saving state: {e}")
        # Clean up temp file if write failed
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass

def verify_qdrant_ground_truth(client, collection_name, state, quiet=False):
    """Compare Qdrant actual vs JSONL cache."""
    if not quiet:
        print("[Verify] Ground truth check against Qdrant...")
    
    scroll_result = client.scroll(collection_name, limit=10**9, with_payload=False)
    actual_ids = {point.id for point in scroll_result[0]}
    
    cached_files = {}
    for path, record in state.items():
        cached_files[path] = set(record.get('chunk_ids', []))
    
    total_cached_ids = sum(len(ids) for ids in cached_files.values())
    orphaned_ids = set()
    
    for path, ids in cached_files.items():
        orphaned = ids - actual_ids
        if orphaned:
            orphaned_ids.update(orphaned)
            if not quiet:
                print(f"  [!] {os.path.basename(path)}: {len(orphaned)} orphaned chunks")
    
    all_cached_ids = set()
    for ids in cached_files.values():
        all_cached_ids.update(ids)
    untracked_ids = actual_ids - all_cached_ids
    
    report = {
        "qdrant_points": len(actual_ids),
        "cached_chunks": total_cached_ids,
        "cached_files": len(state),
        "orphaned_chunks": len(orphaned_ids),
        "untracked_chunks": len(untracked_ids),
        "in_sync": len(orphaned_ids) == 0 and len(untracked_ids) == 0
    }
    
    if not quiet:
        print(f"[Verify] Qdrant: {report['qdrant_points']}, "
              f"Cached: {report['cached_chunks']} in {report['cached_files']} files")
        if report['orphaned_chunks'] > 0:
            print(f"[Verify] ⚠ {report['orphaned_chunks']} orphaned entries")
        if report['untracked_chunks'] > 0:
            print(f"[Verify] ⚠ {report['untracked_chunks']} untracked chunks")
        if report['in_sync']:
            print("[Verify] ✓ State synchronized!")
    
    return report

def rebuild_state_from_qdrant(client, collection_name):
    """Repair mode: Rebuild JSONL from Qdrant."""
    print("[Repair] Rebuilding JSONL from Qdrant...")
    
    if QDRANT_STATE_FILE is None:
        print("[Repair] ERROR: QDRANT_STATE_FILE not set!")
        return {}
    
    temp_file = QDRANT_STATE_FILE + ".tmp"
    files_data = {}
    
    scroll_result = client.scroll(collection_name, limit=10**9, with_payload=True)
    
    for point in scroll_result[0]:
        if not point.payload:
            continue
        path = point.payload.get('path')
        file_hash = point.payload.get('file_hash')
        
        if not path or not file_hash:
            continue
            
        if path not in files_data:
            files_data[path] = {
                'hash': file_hash,
                'chunk_ids': [],
                'indexed_at': datetime.datetime.now().isoformat()
            }
        files_data[path]['chunk_ids'].append(point.id)
    
    for path in files_data:
        files_data[path]['chunk_ids'].sort()
    
    with open(temp_file, 'w', encoding='utf-8') as f:
        for path, data in files_data.items():
            data['path'] = path
            f.write(json.dumps(data) + '\n')
    
    if os.path.exists(QDRANT_STATE_FILE):
        os.remove(QDRANT_STATE_FILE)
    os.rename(temp_file, QDRANT_STATE_FILE)
    
    total_chunks = sum(len(d['chunk_ids']) for d in files_data.values())
    print(f"[Repair] ✓ Rebuilt {len(files_data)} files with {total_chunks} chunks")
    
    return files_data

# ==========================================
# PENDING CHUNKS JSON (shared across all nodes for race condition prevention)
# ==========================================
def load_pending_chunks():
    """Load pending chunks JSON - tracks in-progress files across all nodes."""
    if PENDING_CHUNKS_FILE is None or not os.path.exists(PENDING_CHUNKS_FILE):
        return {}
    try:
        with open(PENDING_CHUNKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_pending_chunks(pending):
    """Save pending chunks to JSON using atomic write (temp file + rename)."""
    if PENDING_CHUNKS_FILE is None:
        return
    try:
        # Use temp file for atomic write - prevents corruption if process crashes mid-write
        temp_file = PENDING_CHUNKS_FILE + ".tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(pending, f, indent=2)
        
        # Atomic rename - either succeeds completely or fails completely
        if os.path.exists(PENDING_CHUNKS_FILE):
            os.remove(PENDING_CHUNKS_FILE)
        os.rename(temp_file, PENDING_CHUNKS_FILE)
    except Exception as e:
        print(f"[!] Error saving pending chunks: {e}")
        # Clean up temp file if write failed
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass

def clear_pending_chunks():
    """Clear pending chunks file."""
    if PENDING_CHUNKS_FILE and os.path.exists(PENDING_CHUNKS_FILE):
        try:
            os.remove(PENDING_CHUNKS_FILE)
        except Exception as e:
            print(f"[!] Error clearing pending chunks: {e}")

# ==========================================
# IGNORE PATTERNS (.alqcignore)
# ==========================================
def load_ignore_patterns():
    """Load ignore patterns from .alqcignore."""
    if ALQC_IGNORE_FILE and os.path.exists(ALQC_IGNORE_FILE):
        with open(ALQC_IGNORE_FILE, 'r') as f:
            return [l.strip() for l in f if l.strip() and not l.startswith("#")]
    return []

def is_ignored(path, patterns):
    """Check if path matches ignore patterns."""
    if PROJECT_ROOT is None:
        return False
    abs_p = os.path.normpath(path)
    rel_p = os.path.relpath(abs_p, PROJECT_ROOT)
    name = os.path.basename(abs_p)

    for p in patterns:
        cp = p.rstrip('/')
        if fnmatch.fnmatch(name, cp) or rel_p.startswith(cp + os.sep) or fnmatch.fnmatch(rel_p, cp):
            return True
    return False

# ==========================================
# FILETREE PERSISTENCE (RAM-saver - stores file list on disk)
# ==========================================
def build_and_save_filetree():
    """Walk workspace and save filetree to JSONL - minimal RAM usage."""
    if FILETREE_JSONL is None:
        return
    
    temp_file = FILETREE_JSONL + ".tmp"
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            for root, dirs, files in os.walk(PROJECT_ROOT):
                # Skip .alqc directory itself
                dirs[:] = [d for d in dirs if d != '.alqc']
                
                for file in files:
                    f_abs = os.path.normpath(os.path.join(root, file))
                    # Don't filter here - store ALL, filter on read
                    f.write(json.dumps({"path": f_abs}) + '\n')
        
        if os.path.exists(FILETREE_JSONL):
            os.remove(FILETREE_JSONL)
        os.rename(temp_file, FILETREE_JSONL)
    except Exception as e:
        print(f"[!] Error saving filetree: {e}")

def iterate_filetree():
    """Yield file paths from JSONL - line-by-line, no RAM buildup."""
    if FILETREE_JSONL is None or not os.path.exists(FILETREE_JSONL):
        return
    
    try:
        with open(FILETREE_JSONL, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    record = json.loads(line)
                    yield record.get('path')
    except Exception as e:
        print(f"[!] Error reading filetree: {e}")

# ==========================================
# UTILITIES
# ==========================================
def compute_file_hash(filepath):
    """SHA-256 hash of file contents - streaming to avoid RAM buildup."""
    sha_hash = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                sha_hash.update(chunk)
        return sha_hash.hexdigest()
    except:
        return None

def is_binary_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk: return True
    except: return True
    return False

# ==========================================
# INTELLIGENT CHUNKING
# ==========================================
def smart_chunk_code(text, filepath, target_tokens=150, max_tokens=300):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.py': return chunk_python(text, target_tokens, max_tokens)
    elif ext in ['.js', '.ts', '.jsx', '.tsx']: return chunk_javascript(text, target_tokens, max_tokens)
    elif ext in ['.java', '.c', '.cpp', '.cs', '.go', '.rs', '.h', '.hpp']: return chunk_c_style(text, target_tokens, max_tokens)
    elif ext in ['.md', '.txt']: return chunk_markdown(text, target_tokens, max_tokens)
    else: return chunk_by_lines(text, target_tokens, max_tokens)

def chunk_python(text, target_tokens, max_tokens):
    chunks = []
    try:
        tree = ast.parse(text)
        lines = text.split('\n')
        processed_lines = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                start_line = node.lineno - 1
                end_line = node.end_lineno if hasattr(node, 'end_lineno') else len(lines)
                if start_line not in processed_lines:
                    chunk_text = '\n'.join(lines[start_line:end_line])
                    char_count = len(chunk_text)
                    # FIX: Use character-based threshold (TARGET_CHUNK_CHARS = 1500), not max_tokens/4
                    if char_count > TARGET_CHUNK_CHARS:
                        sub_chunks = chunk_by_lines(chunk_text, target_tokens, max_tokens)
                        chunks.extend(sub_chunks)
                    else:
                        chunks.append((chunk_text, start_line))
                    for i in range(start_line, end_line): processed_lines.add(i)
        if len(processed_lines) < len(lines):
            remaining = []
            for i, line in enumerate(lines):
                if i not in processed_lines: remaining.append(line)
            if remaining:
                rem_text = '\n'.join(remaining)
                chunks.extend(chunk_by_lines(rem_text, target_tokens, max_tokens))
    except: chunks = chunk_by_lines(text, target_tokens, max_tokens)
    return chunks if chunks else chunk_by_lines(text, target_tokens, max_tokens)

def chunk_c_style(text, target_tokens, max_tokens):
    chunks = []
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.search(r'\w+\s*\([^)]*\)\s*\{|^(class|struct|enum)\s+\w+', line):
            brace_count = line.count('{') - line.count('}')
            start = i
            i += 1
            while i < len(lines) and brace_count > 0:
                brace_count += lines[i].count('{') - lines[i].count('}')
                i += 1
            chunk_text = '\n'.join(lines[start:i])
            char_count = len(chunk_text)
            # FIX: Use character-based threshold (TARGET_CHUNK_CHARS = 1500), not max_tokens/4
            if char_count > TARGET_CHUNK_CHARS:
                sub_chunks = chunk_by_lines(chunk_text, target_tokens, max_tokens)
                chunks.extend(sub_chunks)
            else:
                chunks.append((chunk_text, start))
        else: i += 1
    return chunks if chunks else chunk_by_lines(text, target_tokens, max_tokens)

def chunk_javascript(text, target_tokens, max_tokens): return chunk_c_style(text, target_tokens, max_tokens)

def chunk_markdown(text, target_tokens, max_tokens):
    chunks = []
    lines = text.split('\n')
    current_chunk = []
    current_offset = 0
    for i, line in enumerate(lines):
        if re.match(r'^#+\s+', line):
            if current_chunk:
                chunk_text = '\n'.join(current_chunk)
                char_count = len(chunk_text)
                # FIX: Use character-based threshold (TARGET_CHUNK_CHARS = 1500), not max_tokens/4
                if char_count > TARGET_CHUNK_CHARS:
                    sub_chunks = chunk_by_lines(chunk_text, target_tokens, max_tokens)
                    chunks.extend(sub_chunks)
                else:
                    chunks.append((chunk_text, current_offset))
            current_chunk = [line]
            current_offset = i
        else: current_chunk.append(line)
    if current_chunk:
        chunk_text = '\n'.join(current_chunk)
        chunks.append((chunk_text, current_offset))
    return chunks if chunks else chunk_by_lines(text, target_tokens, max_tokens)

def chunk_by_lines(text, target_tokens, max_tokens):
    chunks = []
    lines = text.split('\n')
    target_lines = (target_tokens * 4) // 50
    overlap_lines = target_lines // 5
    i = 0
    while i < len(lines):
        end = min(i + target_lines, len(lines))
        chunk_text = '\n'.join(lines[i:end])
        if chunk_text.strip(): chunks.append((chunk_text, i))
        i += (target_lines - overlap_lines)
    return chunks

# ==========================================
# LAZY LOADING - STREAMING CHUNKING (RAM-AWARE)
# ==========================================
def stream_chunk_file_lazy(filepath, target_tokens=256, max_tokens=7168, max_buffer_chars=100000):
    """
    STREAM file and yield chunks one at a time without loading entire file into RAM.
    
    Args:
        filepath: Path to file to process
        target_tokens: Target token count per chunk (~256)
        max_tokens: Maximum tokens per chunk (~7168)
        max_buffer_chars: Maximum characters to keep in buffer before flushing (~100KB)
    
    Yields:
        (chunk_text, line_offset) tuples - one at a time
    """
    ext = os.path.splitext(filepath)[1].lower()
    
    # Use ext-specific streaming chunkers
    if ext == '.py':
        yield from stream_chunk_python_lazy(filepath, target_tokens, max_tokens, max_buffer_chars)
    elif ext in ['.js', '.ts', '.jsx', '.tsx']:
        yield from stream_chunk_javascript_lazy(filepath, target_tokens, max_tokens, max_buffer_chars)
    elif ext in ['.java', '.c', '.cpp', '.cs', '.go', '.rs', '.h', '.hpp']:
        yield from stream_chunk_c_style_lazy(filepath, target_tokens, max_tokens, max_buffer_chars)
    elif ext in ['.md', '.txt']:
        yield from stream_chunk_markdown_lazy(filepath, target_tokens, max_tokens, max_buffer_chars)
    else:
        yield from stream_chunk_by_lines_lazy(filepath, target_tokens, max_tokens, max_buffer_chars)


def stream_chunk_by_lines_lazy(filepath, target_tokens, max_tokens, max_buffer_chars):
    """
    Stream file line-by-line and yield chunks - CHARACTER-BASED.
    Accumulates lines until target character count (1500) is reached.
    """
    target_chars = TARGET_CHUNK_CHARS  # 1500 characters per chunk
    overlap_chars = target_chars // 5  # 20% overlap (~300 chars)
    char_buffer = []
    line_numbers = []
    char_count = 0
    lines_processed = 0
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f):
                line_stripped = line.rstrip('\n\r')
                line_with_newline = line_stripped + '\n'
                
                # Track character offset
                lines_processed += 1
                
                # Add to buffer
                char_buffer.append(line_stripped)
                line_numbers.append(line_num)
                char_count += len(line_with_newline)
                
                # When we have enough characters, emit a chunk
                if char_count >= target_chars:
                    chunk_text = '\n'.join(char_buffer)
                    if chunk_text.strip():
                        # Check if chunk exceeds max tokens via char count
                        if len(chunk_text) // 4 > max_tokens:
                            # Sub-chunk oversized blocks
                            for sub_chunk, sub_offset in split_oversized_chunk(chunk_text, line_numbers[0], target_tokens, max_tokens):
                                yield (sub_chunk, sub_offset)
                        else:
                            yield (chunk_text, line_numbers[0])
                    
                    # Keep overlap by characters, not lines
                    overlap_buffer = []
                    overlap_numbers = []
                    overlap_count = 0
                    while char_buffer and overlap_count < overlap_chars:
                        overlap_line = char_buffer.pop(0)
                        overlap_numbers.pop(0)
                        overlap_buffer.append(overlap_line)
                        overlap_numbers.append(line_numbers[0])
                        overlap_count += len(overlap_line) + 1  # +1 for newline
                    
                    char_buffer = overlap_buffer
                    line_numbers = overlap_numbers
                    char_count = overlap_count
    
    except Exception as e:
        print(f"[!] Error streaming {filepath}: {e}")
        return
    
    # Emit remaining buffer
    if char_buffer:
        chunk_text = '\n'.join(char_buffer)
        if chunk_text.strip():
            if len(chunk_text) // 4 > max_tokens:
                for sub_chunk, sub_offset in split_oversized_chunk(chunk_text, line_numbers[0], target_tokens, max_tokens):
                    yield (sub_chunk, sub_offset)
            else:
                yield (chunk_text, line_numbers[0])


def split_oversized_chunk(chunk_text, base_offset, target_tokens, max_tokens):
    """Split a chunk that exceeds max_tokens into smaller chunks - CHARACTER-BASED."""
    target_chars = TARGET_CHUNK_CHARS  # 1500 characters per chunk (from config)
    overlap_chars = target_chars // 5  # 20% overlap for context (~300 chars)
    lines = chunk_text.split('\n')
    chunk_buffer = []
    char_count = 0
    chunk_offset = base_offset
    
    for i, line in enumerate(lines):
        line_with_newline = line + '\n' if i < len(lines) - 1 else line
        chunk_buffer.append(line_with_newline)
        char_count += len(line_with_newline)
        
        if char_count >= target_chars:
            chunk_text_out = ''.join(chunk_buffer)
            yield (chunk_text_out.rstrip('\n'), chunk_offset)
            
            # Keep overlap by characters
            overlap_buffer = []
            overlap_count = 0
            while chunk_buffer and overlap_count < overlap_chars:
                overlap_line = chunk_buffer.pop(0)
                overlap_buffer.append(overlap_line)
                overlap_count += len(overlap_line)
            
            chunk_buffer = overlap_buffer
            char_count = overlap_count
            if overlap_buffer:
                # Track character offset for accurate positioning
                chars_consumed = len(chunk_text_out) - sum(len(l) for l in overlap_buffer)
                chunk_offset += chars_consumed
            else:
                chunk_offset += len(chunk_text_out)
    
    # Emit remaining
    if chunk_buffer:
        yield (''.join(chunk_buffer).rstrip('\n'), chunk_offset)


def stream_chunk_python_lazy(filepath, target_tokens, max_tokens, max_buffer_chars):
    """
    Stream Python file line-by-line, detect functions/classes, yield semantic chunks - CHARACTER-BASED.
    Falls back to character-based streaming if AST parsing fails.
    Splits semantic chunks at 1500 characters with 20% overlap.
    """
    try:
        # Try AST-based chunking - load minimal text needed per function
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = [line.rstrip('\n\r') for line in f]
        
        tree = ast.parse('\n'.join(lines))
        processed_lines = set()
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                start_line = node.lineno - 1
                end_line = node.end_lineno if hasattr(node, 'end_lineno') else min(start_line + 100, len(lines))
                
                if start_line not in processed_lines:
                    chunk_text = '\n'.join(lines[start_line:end_line])
                    char_count = len(chunk_text)
                    
                    # FIX: Use character-based threshold (split at 1500 chars), not max_tokens/4
                    if char_count > TARGET_CHUNK_CHARS:
                        # Stream sub-chunks for large functions at 1500 char intervals
                        for sub_chunk, sub_offset in split_oversized_chunk(chunk_text, start_line, target_tokens, max_tokens):
                            yield (sub_chunk, sub_offset)
                    else:
                        yield (chunk_text, start_line)
                    
                    for i in range(start_line, end_line):
                        processed_lines.add(i)
        
        # Yield remaining unorganized lines using character-based streaming
        remaining_lines = [(lines[i], i) for i in range(len(lines)) if i not in processed_lines]
        if remaining_lines:
            # Convert to text and chunk at 1500 chars
            remaining_text_with_offsets = []
            for i, (line, line_num) in enumerate(remaining_lines):
                remaining_text_with_offsets.append((line, line_num))
            
            # Yield using character-based logic
            char_buffer = []
            line_numbers = []
            char_count = 0
            target_chars = TARGET_CHUNK_CHARS
            overlap_chars = target_chars // 5
            
            for line, line_num in remaining_text_with_offsets:
                char_buffer.append(line)
                line_numbers.append(line_num)
                char_count += len(line) + 1  # +1 for newline
                
                if char_count >= target_chars:
                    chunk_text = '\n'.join(char_buffer)
                    yield (chunk_text, line_numbers[0])
                    
                    # Keep overlap
                    overlap_buffer = []
                    overlap_numbers = []
                    overlap_count = 0
                    while char_buffer and overlap_count < overlap_chars:
                        overlap_line = char_buffer.pop(0)
                        overlap_numbers.pop(0)
                        overlap_buffer.append(overlap_line)
                        overlap_numbers.append(line_numbers[0])
                        overlap_count += len(overlap_line) + 1
                    
                    char_buffer = overlap_buffer
                    line_numbers = overlap_numbers
                    char_count = overlap_count
            
            # Emit remaining
            if char_buffer:
                yield ('\n'.join(char_buffer), line_numbers[0])
                
    except Exception:
        # Fallback to character-based streaming
        yield from stream_chunk_by_lines_lazy(filepath, target_tokens, max_tokens, max_buffer_chars)


def stream_chunk_c_style_lazy(filepath, target_tokens, max_tokens, max_buffer_chars):
    """
    Stream C/C++/Java/Go/Rust file line-by-line, detect functions/classes, yield semantic chunks - CHARACTER-BASED.
    """
    brace_count = 0
    start_line = 0
    buffer = []
    line_numbers = []
    char_count = 0
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f):
                stripped = line.rstrip('\n\r')
                line_with_newline = stripped + '\n'
                
                buffer.append(stripped)
                line_numbers.append(line_num)
                char_count += len(line_with_newline)
                
                # Check for function/class definition start
                if brace_count == 0 and re.search(r'\w+\s*\([^)]*\)\s*\{|^(class|struct|enum|interface|namespace|impl)\s+\w', stripped):
                    for i, ln in enumerate(buffer):
                        if '{' in ln:
                            brace_count += ln.count('{')
                            brace_count -= ln.count('}')
                            break
                    # Flush buffer before function using character-based chunking
                    if len(buffer) > 1:
                        prev_lines = buffer[:-1]
                        if prev_lines:
                            prev_text = '\n'.join(prev_lines)
                            prev_char_count = len(prev_text)
                            # FIX: Split preamble at 1500 chars if too large
                            if prev_char_count > TARGET_CHUNK_CHARS:
                                for sub_chunk, sub_offset in split_oversized_chunk(prev_text, line_numbers[-len(prev_lines)], target_tokens, max_tokens):
                                    yield (sub_chunk, sub_offset)
                            else:
                                yield ('\n'.join(prev_lines), line_numbers[-len(prev_lines)])
                    buffer = [stripped]
                    line_numbers = [line_num]
                    char_count = len(line_with_newline)
                    start_line = line_num
                else:
                    brace_count += line.count('{')
                    brace_count -= line.count('}')
                
                # When brace returns to 0, we have a complete function
                if start_line != 0 and brace_count == 0:
                    chunk_text = '\n'.join(buffer)
                    chunk_char_count = len(chunk_text)
                    
                    # FIX: Use character-based threshold (split at 1500 chars), not max_tokens/4
                    if chunk_char_count > TARGET_CHUNK_CHARS:
                        for sub_chunk, sub_offset in split_oversized_chunk(chunk_text, start_line, target_tokens, max_tokens):
                            yield (sub_chunk, sub_offset)
                    else:
                        yield (chunk_text, start_line)
                    
                    buffer = []
                    line_numbers = []
                    char_count = 0
                    start_line = 0
        
        # Emit remaining buffer (headers, globals) using character-based chunking
        if buffer:
            remaining_text = '\n'.join(buffer)
            remaining_char_count = len(remaining_text)
            # FIX: Split remaining at 1500 chars if too large
            if remaining_char_count > TARGET_CHUNK_CHARS:
                for sub_chunk, sub_offset in split_oversized_chunk(remaining_text, line_numbers[0], target_tokens, max_tokens):
                    yield (sub_chunk, sub_offset)
            else:
                yield (remaining_text, line_numbers[0])
            
    except Exception:
        yield from stream_chunk_by_lines_lazy(filepath, target_tokens, max_tokens, max_buffer_chars)


def stream_chunk_javascript_lazy(filepath, target_tokens, max_tokens, max_buffer_chars):
    """Aliased to C-style (similar bracket matching)"""
    yield from stream_chunk_c_style_lazy(filepath, target_tokens, max_tokens, max_buffer_chars)


def stream_chunk_markdown_lazy(filepath, target_tokens, max_tokens, max_buffer_chars):
    """
    Stream Markdown line-by-line, break on headers - CHARACTER-BASED.
    """
    current_chunk = []
    current_offset = 0
    char_count = 0
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f):
                stripped = line.rstrip('\n\r')
                line_with_newline = stripped + '\n'
                
                # Check for header
                if re.match(r'^#+\s+', stripped):
                    if current_chunk:
                        chunk_text = '\n'.join(current_chunk)
                        chunk_char_count = len(chunk_text)
                        # FIX: Check against reasonable character limit (6KB), not max_tokens/4 (28KB)
                        if chunk_char_count > TARGET_CHUNK_CHARS * 4:
                            for sub_chunk, sub_offset in split_oversized_chunk(chunk_text, current_offset, target_tokens, max_tokens):
                                yield (sub_chunk, sub_offset)
                        else:
                            yield (chunk_text, current_offset)
                    current_chunk = [stripped]
                    char_count = len(line_with_newline)
                    current_offset = line_num
                else:
                    current_chunk.append(stripped)
                    char_count += len(line_with_newline)
                    
                    # Check if chunk EXCEEDS TARGET_CHUNK_CHARS * 2 (~3KB) and needs splitting
                    chunk_text = '\n'.join(current_chunk)
                    chunk_char_count = len(chunk_text)
                    # FIX: Use character-based threshold, not max_tokens/4
                    if chunk_char_count > TARGET_CHUNK_CHARS * 2:
                        for sub_chunk, sub_offset in split_oversized_chunk(chunk_text, current_offset, target_tokens, max_tokens):
                            yield (sub_chunk, sub_offset)
                        current_chunk = []
                        char_count = 0
                    
                    # Add the current line for next chunk
                    current_chunk.append(stripped)
                    char_count += len(line_with_newline)
                    current_offset = line_num
        
        # Emit final chunk
        if current_chunk:
            chunk_text = '\n'.join(current_chunk)
            chunk_char_count = len(chunk_text)
            if chunk_char_count > TARGET_CHUNK_CHARS * 4:
                for sub_chunk, sub_offset in split_oversized_chunk(chunk_text, current_offset, target_tokens, max_tokens):
                    yield (sub_chunk, sub_offset)
            else:
                yield (chunk_text, current_offset)
                
    except Exception:
        yield from stream_chunk_by_lines_lazy(filepath, target_tokens, max_tokens, max_buffer_chars)

# ==========================================
# WORKER ENGINE (Node-centric with pending_chunks.json race prevention)
# ==========================================
async def silo_engine(node_config, file_queue, batch_queue, session, qdrant_state, ignore_patterns_ref, node_id, file_completion_queue=None):
    """Per-node worker engine. Each node has its own magazine but shares pending_chunks.json."""
    magazine = asyncio.Queue(maxsize=CHIP_QUEUE_DEPTH)
    base_url = node_config['url']
    target_model = node_config['model']
    node_type = node_config.get('type', 'llama')

    def process_file_sync(path):
        """
        Process file using LAZY LOADING - streams file instead of loading all into RAM.
        Returns generator that yields chunks one at a time.
        """
        try:
            return stream_chunk_file_lazy(path, TARGET_TOKENS, MAX_TOKENS)
        except: return iter([])

    async def claim_file_in_pending(f_path, f_hash):
        """Claim a file in pending_chunks.json - prevents other nodes from processing it."""
        pending = load_pending_chunks()
        # Check if file is already being processed by another node
        if f_path in pending and pending[f_path].get('hash') == f_hash:
            return False  # Already claimed
        
        # Claim this file
        pending[f_path] = {
            'hash': f_hash,
            'node_id': node_id,
            'timestamp': datetime.datetime.now().isoformat()
        }
        save_pending_chunks(pending)
        return True

    async def release_file_from_pending(f_path):
        """Release file from pending_chunks.json after successful write."""
        pending = load_pending_chunks()
        pending.pop(f_path, None)
        save_pending_chunks(pending)

    async def magazine_refill():
        """CONTINUOUSLY refill magazine by checking pending_chunks.json before pulling new files."""
        while True:
            # Walk pending_chunks to see what's being processed across all nodes
            pending = load_pending_chunks()
            processing_hashes = {data['hash'] for data in pending.values()}
            
            # Try to pull from file_queue, skip if already being processed
            while magazine.qsize() < CHIP_QUEUE_DEPTH:
                try:
                    file_data = await asyncio.wait_for(file_queue.get(), timeout=2.0)
                except asyncio.TimeoutError:
                    break
                
                f_path, f_hash = file_data
                
                # Skip if file hash is already in pending (being processed by another node)
                if f_hash in processing_hashes:
                    file_queue.task_done()
                    continue

                # Try to claim this file
                if not await claim_file_in_pending(f_path, f_hash):
                    file_queue.task_done()
                    continue

                print(f"[{node_id}] Processing: {os.path.basename(f_path)}")
                
                # Process the file and put into magazine
                smart_chunks = await asyncio.to_thread(process_file_sync, f_path)
                for chunk_text, line_offset in smart_chunks:
                    clean = chunk_text.strip()
                    if clean and len(clean) >= MIN_CHUNK_CHARS:
                        sanitized = chunk_text.replace('\0', '')
                        payload = ALQC_CONTEXT + "\n" + sanitized if ALQC_CONTEXT.strip() else sanitized
                        c_id = int(hashlib.sha1(f"{f_path}:{line_offset}:{f_hash}".encode()).hexdigest()[:16], 16)
                        meta = {"path": f_path, "offset": line_offset, "file_hash": f_hash, "node_id": node_id}
                        await magazine.put((payload, meta, c_id))
                
                # Note: File released from pending AFTER successful Qdrant write (tracked in payload)
                file_queue.task_done()
            
            # Signal end if queue empty
            if file_queue.empty():
                await magazine.put(None)
                break
            
            # Small delay before checking again if magazine needs refilling
            await asyncio.sleep(0.1)

    # Start magazine refill task
    refill_task = asyncio.create_task(magazine_refill())
    
    if node_type == 'ollama':
        url = f"{base_url}/api/embeddings"
    else:
        url = f"{base_url}/v1/embeddings"

    # Batch embedding request handling
    batch_buffer = []
    batch_metadata = []
    batch_ids = []
    last_flush = asyncio.get_event_loop().time()
    flush_event = asyncio.Event()

    async def flush_batch(force=False):
        """Flush accumulated batch to the embedding API."""
        nonlocal batch_buffer, batch_metadata, batch_ids, last_flush
        
        if not batch_buffer:
            return
            
        try:
            if node_type == 'ollama':
                # Ollama handles one at a time in batch loop
                for i, (payload_text, c_id) in enumerate(zip(batch_buffer, batch_ids)):
                    request_data = {"model": target_model, "prompt": payload_text}
                    async with session.post(url, json=request_data, timeout=90) as resp:
                        if resp.status != 200:
                            error_text = await resp.text()
                            print(f"[{node_id}] HTTP {resp.status}: {error_text[:100]}")
                            continue
                        res = await resp.json()
                        vector = res.get('embedding')
                        if vector and len(vector) == 1024:
                            await batch_queue.put({"id": c_id, "vector": vector, "payload": batch_metadata[i]})
            else:
                # Batching for llama.cpp - send multiple inputs in single request
                # print(f"[{node_id}] Sending batch: {len(batch_buffer)} items")  # Debug
                request_data = {"model": target_model, "input": batch_buffer}
                
                async with session.post(url, json=request_data, timeout=90) as resp:
                    if resp.status != 200:
                        error_text = await resp.text()
                        print(f"[{node_id}] HTTP {resp.status}: {error_text[:100]}")
                    else:
                        res = await resp.json()
                        
                        if 'data' in res and isinstance(res['data'], list):
                            for i, item in enumerate(res['data']):
                                if i < len(batch_ids):
                                    vector = item.get('embedding')
                                    if vector and len(vector) == 1024:
                                        await batch_queue.put({
                                            "id": batch_ids[i],
                                            "vector": vector,
                                            "payload": batch_metadata[i]
                                        })
                        else:
                            print(f"[{node_id}] Unexpected response format")
                            
        except asyncio.TimeoutError:
            print(f"[{node_id}] Batch timeout ({len(batch_buffer)} items)")
        except Exception as e:
            print(f"[{node_id}] Batch error: {e}")
        finally:
            batch_buffer.clear()
            batch_metadata.clear()
            batch_ids.clear()
            last_flush = asyncio.get_event_loop().time()

    async def batch_producer():
        """Background task that flushes batches on timeout."""
        while True:
            try:
                await asyncio.wait_for(flush_event.wait(), timeout=EMBEDDING_BATCH_TIMEOUT)
                flush_event.clear()
            except asyncio.TimeoutError:
                # Timeout reached, flush the batch
                await flush_batch()
            else:
                # Event was set, check if we should exit
                if magazine.empty() and not batch_buffer:
                    # Flush any remaining and exit
                    await flush_batch(force=True)
                    break

    # Start the batch producer
    batch_producer_task = asyncio.create_task(batch_producer())

    # Main consumer loop - accumulates items in buffer
    while True:
        item = await magazine.get()
        if item is None:
            magazine.task_done()
            # Signal batch producer to finish
            flush_event.set()
            break
            
        payload_text, metadata, c_id = item
        batch_buffer.append(payload_text)
        batch_metadata.append(metadata)
        batch_ids.append(c_id)
        
        # Flush if batch size reached
        if len(batch_buffer) >= EMBEDDING_BATCH_SIZE:
            await flush_batch()
            flush_event.set()
        
        magazine.task_done()
    
    await refill_task
    await batch_producer_task

async def qdrant_state_manager(file_completion_queue, qdrant_state, quiet=False):
    """Update state with chunk_ids provided by db_writer - NO Qdrant fetch needed."""
    batch_count = 0
    
    while True:
        item = await file_completion_queue.get()
        if item is None:
            save_qdrant_state(qdrant_state)
            file_completion_queue.task_done()
            break
        
        # Now receives (f_path, f_hash, chunk_ids) directly from db_writer
        f_path, f_hash, chunk_ids = item
        
        try:
            if chunk_ids:
                qdrant_state[f_path] = {
                    'path': f_path,
                    'hash': f_hash,
                    'chunk_ids': chunk_ids,
                    'indexed_at': datetime.datetime.now().isoformat()
                }
                
                batch_count += 1
                
                # Save every 10 files - now safely AFTER Qdrant confirm
                if batch_count % 10 == 0:
                    save_qdrant_state(qdrant_state)
                    if not quiet:
                        print(f"[State] ✓ {batch_count} files committed to state")
        except Exception as e:
            print(f"[!] State update error for {f_path}: {e}")
        
        file_completion_queue.task_done()
    
    save_qdrant_state(qdrant_state)
    if not quiet:
        print(f"[State] COMPLETE: {batch_count} files committed to state")

async def db_writer(batch_queue, ignore_patterns_ref, quiet=False, file_completion_queue=None):
    """Write vectors to Qdrant and emit file completion events with chunk_ids."""
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    buffer = []
    total_written = 0
    
    # Track which file each chunk_id belongs to: {chunk_id: (file_path, file_hash)}
    chunk_id_to_file = {}
    # Track chunks written per file: {(file_path, file_hash): set of chunk_ids}
    file_chunks_written = {}
    # Original chunk_ids per file: {(file_path, file_hash): list of chunk_ids}
    file_total_chunks = {}
    
    if not quiet:
        print("[System] Writer: READY.")
    
    def perform_write(points_buffer):
        """Sync wrapper - returns (count, completed_files) tuple."""
        if not points_buffer: return 0, []
        points = [PointStruct(id=i['id'], vector=i['vector'], payload=i['payload']) for i in points_buffer]
        try:
            client.upsert(COLLECTION_NAME, points=points, wait=False)
            # Track written chunks and collect completed files
            completed_files = []
            for point in points_buffer:
                chunk_id = point['id']
                file_key = chunk_id_to_file.get(chunk_id)
                if file_key:
                    if file_key not in file_chunks_written:
                        file_chunks_written[file_key] = set()
                    file_chunks_written[file_key].add(chunk_id)
                    # Check if file is complete
                    if len(file_chunks_written[file_key]) >= len(file_total_chunks.get(file_key, [])):
                        completed_files.append(file_key)
            return len(points_buffer), completed_files
        except Exception as e:
            print(f"[!] DB Error: {e}")
            return 0, []

    while True:
        item = await batch_queue.get()
        if item is None:
            if buffer:
                count, completed_files = await asyncio.to_thread(perform_write, buffer)
                total_written += count
                # Emit completed files with chunk_ids - UPDATE STATE FIRST, then release from pending
                for file_key in completed_files:
                    f_path, f_hash = file_key
                    # Get chunk_ids from tracking BEFORE cleanup
                    chunk_ids = sorted(list(file_total_chunks.get(file_key, set())))
                    file_completion_data = (f_path, f_hash, chunk_ids)
                    if not quiet:
                        print(f"[State] ✓ File indexed: {f_path} ({len(chunk_ids)} chunks)")
                    
                    # CRITICAL: Send to state_manager FIRST (updates qdrant_state.jsonl)
                    # This ensures state is preserved BEFORE releasing from pending
                    if file_completion_queue is not None:
                        await file_completion_queue.put(file_completion_data)
                    
                    # AFTER state update is queued, release from pending_chunks.json
                    pending = load_pending_chunks()
                    if f_path in pending:
                        pending.pop(f_path, None)
                        save_pending_chunks(pending)
                    
                    # CLEANUP RAM: Remove completed file from tracking dictionaries
                    for chunk_id in chunk_ids:
                        chunk_id_to_file.pop(chunk_id, None)
                    file_chunks_written.pop(file_key, None)
                    file_total_chunks.pop(file_key, None)
            batch_queue.task_done()
            break
        
        buffer.append(item)
        # Track file metadata for completion tracking
        chunk_id = item['id']
        payload = item.get('payload', {})
        file_path = payload.get('path')
        file_hash = payload.get('file_hash')
        
        if file_path and file_hash:
            chunk_id_to_file[chunk_id] = (file_path, file_hash)
            file_key = (file_path, file_hash)
            if file_key not in file_total_chunks:
                file_total_chunks[file_key] = set()
            file_total_chunks[file_key].add(chunk_id)
        
        if len(buffer) >= BATCH_SIZE:
            count, completed_files = await asyncio.to_thread(perform_write, buffer)
            total_written += count
            if count > 0:
                q_size = batch_queue.qsize()
                if not quiet:
                    print(f"[Writer] ✓ {total_written} vectors written (Queue: {q_size})")
                
                # Emit completed files with chunk_ids - UPDATE STATE FIRST, then release from pending
                for file_key in completed_files:
                    f_path, f_hash = file_key
                    # Get chunk_ids from tracking BEFORE cleanup
                    chunk_ids = sorted(list(file_total_chunks.get(file_key, set())))
                    file_completion_data = (f_path, f_hash, chunk_ids)
                    if not quiet:
                        print(f"[State] ✓ File indexed: {f_path} ({len(chunk_ids)} chunks)")
                    
                    # CRITICAL: Send to state_manager FIRST (updates qdrant_state.jsonl)
                    # This ensures state is preserved BEFORE releasing from pending
                    if file_completion_queue is not None:
                        await file_completion_queue.put(file_completion_data)
                    
                    # AFTER state update is queued, release from pending_chunks.json
                    pending = load_pending_chunks()
                    if f_path in pending:
                        pending.pop(f_path, None)
                        save_pending_chunks(pending)
                    
                    # CLEANUP RAM: Remove completed file from tracking dictionaries
                    for chunk_id in chunk_ids:
                        chunk_id_to_file.pop(chunk_id, None)
                    file_chunks_written.pop(file_key, None)
                    file_total_chunks.pop(file_key, None)
                
                if total_written % 5000 < BATCH_SIZE:
                    new_patterns = load_ignore_patterns()
                    if new_patterns != ignore_patterns_ref[0]:
                        if not quiet:
                            print("[System] .alqcignore updated!")
                        ignore_patterns_ref[0] = new_patterns
            buffer = []
        batch_queue.task_done()
    
    if not quiet:
        print(f"[Writer] COMPLETE: {total_written} total vectors")

# ==========================================
# MAIN
# ==========================================
async def main(workspace=None, repair_mode=False, verify_only=False, quiet=True):
    # Setup paths first
    setup_paths(workspace)
    
    # Setup logging
    log_path = setup_logging(quiet)
    log_run_header()
    
    # Redirect stdout/stderr to logging
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = LoggerWriter(logging.INFO)
    sys.stderr = LoggerWriter(logging.ERROR)
    
    if not quiet:
        print(f"⬡ IGNITION: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"--- ALQC V22 (Workspace-Aware) ---")
        print(f"[INIT] Workspace: {PROJECT_ROOT}")
        print(f"[INIT] State: {QDRANT_STATE_FILE}")
        print(f"[INIT] Log: {log_path}")
    
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            COLLECTION_NAME,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
        )
        if not quiet:
            print(f"[System] Created collection: {COLLECTION_NAME}")
    
    qdrant_state = load_qdrant_state()
    if not quiet:
        print(f"[System] Loaded {len(qdrant_state)} files from state")
    
    if repair_mode:
        qdrant_state = rebuild_state_from_qdrant(client, COLLECTION_NAME)
        if not quiet:
            print("[System] Repair complete.")
        if verify_only:
            return
    
    verify_report = verify_qdrant_ground_truth(client, COLLECTION_NAME, qdrant_state, quiet)
    start_count = verify_report['qdrant_points']
    
    if not quiet:
        print(f"[System] Qdrant: {start_count} points")
    
    if verify_only:
        if not quiet:
            print("[System] Verify-only mode. Exiting.")
        return
    
    ignore_patterns_ref = [load_ignore_patterns()]
    # BOUNDED queue to prevent RAM buildup - only 5 file paths in queue at once
    file_queue = asyncio.Queue(maxsize=5)
    file_completion_queue = asyncio.Queue()  # Queue for files successfully written to Qdrant
    
    # Clear old pending chunks from previous runs
    clear_pending_chunks()
    
    # Build filetree JSONL - on-disk storage, no RAM buildup
    if not quiet:
        print("[System] Building filetree...")
    build_and_save_filetree()
    
    stats = {"new": 0, "changed": 0, "unchanged": 0, "deleted": 0}
    
    # First pass: collect current files from filetree (line-by-line)
    if not quiet:
        print("[System] Checking for deleted files...")
    state_files = set(qdrant_state.keys())
    current_files = set()
    
    for f_abs in iterate_filetree():
        if f_abs is None:
            continue
        # Apply filters now
        if is_ignored(f_abs, ignore_patterns_ref[0]) or is_binary_file(f_abs):
            continue
        current_files.add(f_abs)
    
    # Delete removed files from Qdrant
    deleted = state_files - current_files
    for path in deleted:
        cached_data = qdrant_state.get(path)
        if cached_data and cached_data.get('chunk_ids'):
            try:
                client.delete(COLLECTION_NAME, points_selector=cached_data['chunk_ids'])
                stats['deleted'] += 1
                del qdrant_state[path]
            except Exception as e:
                print(f"[!] Error deleting: {e}")
    
    if not quiet:
        print(f"[System] NEW/CHANGED detection will stream from filetree...")
    
    # Background task to STREAM files into bounded queue from disk (NO RAM BUILDUP)
    async def filequeue_feeder():
        """Stream files from filetree.jsonl into bounded queue - only ~100 in RAM at once."""
        for f_abs in iterate_filetree():
            if f_abs is None:
                continue
            
            # Apply filters
            if is_ignored(f_abs, ignore_patterns_ref[0]) or is_binary_file(f_abs):
                continue
            
            current_hash = compute_file_hash(f_abs)
            if not current_hash:
                continue
            
            if f_abs not in qdrant_state:
                stats['new'] += 1
                # Wait for space in bounded queue - blocks when full
                await file_queue.put((f_abs, current_hash))
            else:
                cached_data = qdrant_state[f_abs]
                if cached_data['hash'] != current_hash:
                    stats['changed'] += 1
                    if cached_data.get('chunk_ids'):
                        try:
                            client.delete(COLLECTION_NAME, points_selector=cached_data['chunk_ids'])
                        except Exception as e:
                            print(f"[!] Error deleting: {e}")
                    del qdrant_state[f_abs]
                    # Wait for space in bounded queue - blocks when full
                    await file_queue.put((f_abs, current_hash))
                else:
                    stats['unchanged'] += 1
        
        # Signal end of files
        await file_queue.put(None)
    if not quiet:
        print(f"[System] Streaming files from disk (bounded queue)...")
    
    
    async with aiohttp.ClientSession() as session:
        batch_queue = asyncio.Queue(maxsize=100)
        
        # Start filequeue_feeder task - STREAMS files into bounded queue
        feeder_task = asyncio.create_task(filequeue_feeder())
        
        # writer_task now emits to file_completion_queue after successful Qdrant writes
        writer_task = asyncio.create_task(db_writer(batch_queue, ignore_patterns_ref, quiet, file_completion_queue))
        # state_manager reads from file_completion_queue AFTER Qdrant confirms writes
        state_task = asyncio.create_task(qdrant_state_manager(file_completion_queue, qdrant_state, quiet))
        
        # Node-centric: one silo_engine per NODE (not per worker)
        silos = []
        for n_idx, node in enumerate(ALL_NODES):
            node_id = f"{node['type'][:1]}{n_idx}"
            silos.append(silo_engine(node, file_queue, batch_queue, session, qdrant_state, ignore_patterns_ref, node_id, file_completion_queue))
        
        if not quiet:
            print(f"[System] Launching {len(silos)} node engines...")
        
        # Wait for all node engines to finish
        await asyncio.gather(*silos)
        
        # All done, signal shutdown
        await batch_queue.put(None)
        await file_completion_queue.put(None)
        await feeder_task  # Ensure feeder task completes
        await writer_task
        await state_task
    
    end_count = client.count(COLLECTION_NAME).count
    delta = end_count - start_count
    if not quiet:
        print(f"\n⬡ COMPLETE ⬡")
        print(f"Database: {start_count} → {end_count} (+{delta})")
    else:
        if delta != 0 or stats['new'] > 0 or stats['changed'] > 0 or stats['deleted'] > 0:
            sys.__stdout__.write(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] "
                  f"NEW={stats['new']}, CHANGED={stats['changed']}, DEL={stats['deleted']}, Vectors: {delta:+d}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="ALQC V22 Embedding Indexer - Workspace-Aware",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Workspace Detection:
  The script automatically detects the workspace by finding a .alqc/ directory.
  The workspace is the parent directory of .alqc/.
  
  Structure:
    my_project/
      .alqc/              <- Marker & state directory
        qdrant_state.jsonl
        .alqcignore       <- Ignore patterns
      src/
      other_files/

Logging:
  Logs are stored in ~/.config/qdrant_cache/logs/alqc_aware_embedder.log
  Maximum size: 100MiB with 3 rotated backups (4 files total)
  Each run starts with a searchable header:
    Run #YYMMDDhhmm (ALQC Searchable)
    Log Stardate: mm-dd-yyyy HH:MM:SS

Examples:
  # Run from workspace (auto-detect via .alqc/)
  cd /path/to/my_project && python3 %(prog)s
  
  # Run from anywhere with explicit workspace
  python3 %(prog)s --workspace /path/to/my_project
  
  # Cron-friendly (quiet mode, logs only to file)
  python3 %(prog)s
  
  # Verbose mode (print to console too)
  python3 %(prog)s --no-quiet
  
  # Verify state
  python3 %(prog)s --verify
  
  # Repair/rebuild from Qdrant
  python3 %(prog)s --repair

Cron example (every minute):
  * * * * * cd /path/to/project && python3 .alqc/%(prog)s
"""
    )
    parser.add_argument('--workspace', '-w', type=str, default=None,
                       help='Workspace directory (default: auto-detect via .alqc/)')
    parser.add_argument('--log-file', '-l', type=str, default=None,
                       help='Custom log file path (default: ~/.config/qdrant_cache/logs/alqc_aware_embedder.log)')
    parser.add_argument('--repair', action='store_true', 
                       help='Rebuild state from Qdrant')
    parser.add_argument('--verify', action='store_true', 
                       help='Verify state only, no reindexing')
    parser.add_argument('--quiet', '-q', action='store_true', default=True,
                       help='Quiet mode (only print on changes, default: True)')
    parser.add_argument('--no-quiet', dest='quiet', action='store_false',
                       help='Disable quiet mode (verbose output)')
    
    args = parser.parse_args()
    
    # Override log path if specified
    if args.log_file:
        LOG_FILE = args.log_file
        LOG_DIR = os.path.dirname(args.log_file)
    
    try:
        asyncio.run(main(
            workspace=args.workspace,
            repair_mode=args.repair,
            verify_only=args.verify,
            quiet=args.quiet
        ))
    except KeyboardInterrupt:
        # In quiet mode, write directly to original stdout to bypass logging
        if args.quiet:
            sys.__stdout__.write("\n[System] Interrupted.\n")
        else:
            print("\n[System] Interrupted.")
