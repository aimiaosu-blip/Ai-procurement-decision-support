import hashlib, json, sqlite3
from datetime import datetime, timezone
from pathlib import Path

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()

class ReviewStore:
    """Local demo identities are self-declared; not enterprise authorization."""
    def __init__(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY, artifact TEXT, decision TEXT, reviewer TEXT, reason TEXT, time TEXT, previous TEXT, hash TEXT)")
    def decide(self, artifact, decision, reviewer, reason, blocked=False):
        if decision not in {'approve','revise','reject'} or not reviewer.strip() or not reason.strip():
            raise ValueError('Decision, reviewer and reason are required')
        if blocked and decision == 'approve':
            raise ValueError('Unresolved exceptions block approval')
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            if self.db.execute('SELECT 1 FROM reviews WHERE artifact=?',(artifact,)).fetchone():
                raise ValueError('This artifact version already has a final review')
            last=self.db.execute('SELECT hash FROM reviews ORDER BY id DESC LIMIT 1').fetchone()
            payload=[artifact,decision,reviewer.strip(),reason.strip(),datetime.now(timezone.utc).isoformat(),last[0] if last else 'GENESIS']
            self.db.execute('INSERT INTO reviews (artifact,decision,reviewer,reason,time,previous,hash) VALUES (?,?,?,?,?,?,?)',payload+[digest(payload)])
    def rows(self):
        return self.db.execute('SELECT * FROM reviews ORDER BY id').fetchall()
    def verify(self):
        previous='GENESIS'
        for row in self.rows():
            if row[6]!=previous or digest(list(row[1:7]))!=row[7]: return False
            previous=row[7]
        return True
