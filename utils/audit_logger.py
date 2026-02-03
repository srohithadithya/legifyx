"""
Legifyx Audit Logger
Maintains audit trail for compliance and security
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
import logging

logger = logging.getLogger(__name__)


class AuditLogger:
    """Secure audit logging for contract analysis activities"""
    
    def __init__(self, log_dir: str = None):
        self.log_dir = Path(log_dir) if log_dir else Path.cwd() / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "audit_log.json"
        self._ensure_log_file()
    
    def _ensure_log_file(self):
        """Ensure log file exists"""
        if not self.log_file.exists():
            with open(self.log_file, 'w') as f:
                json.dump({"entries": [], "metadata": {"created": datetime.now().isoformat()}}, f)
    
    def _generate_entry_id(self) -> str:
        """Generate unique entry ID"""
        timestamp = datetime.now().isoformat()
        return hashlib.sha256(f"{timestamp}".encode()).hexdigest()[:16]
    
    def _hash_content(self, content: str) -> str:
        """Generate hash of content for integrity verification"""
        return hashlib.sha256(content.encode()).hexdigest()
    
    def log_event(self, event_type: str, details: Dict, user_id: str = "system") -> str:
        """
        Log an audit event
        
        Args:
            event_type: Type of event (upload, analysis, export, etc.)
            details: Event details
            user_id: User identifier
        
        Returns:
            Entry ID
        """
        entry_id = self._generate_entry_id()
        
        entry = {
            "id": entry_id,
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "details": details
        }
        
        try:
            with open(self.log_file, 'r') as f:
                log_data = json.load(f)
            
            log_data["entries"].append(entry)
            
            # Keep only last 10000 entries
            if len(log_data["entries"]) > 10000:
                log_data["entries"] = log_data["entries"][-10000:]
            
            with open(self.log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
            
            return entry_id
        
        except Exception as e:
            logger.error(f"Audit log failed: {e}")
            return entry_id
    
    def log_upload(self, filename: str, file_hash: str, user_id: str = "system") -> str:
        """Log document upload"""
        return self.log_event("DOCUMENT_UPLOAD", {
            "filename": filename,
            "file_hash": file_hash,
            "action": "Contract document uploaded for analysis"
        }, user_id)
    
    def log_analysis(self, contract_id: str, contract_type: str, risk_score: float, user_id: str = "system") -> str:
        """Log analysis completion"""
        return self.log_event("ANALYSIS_COMPLETE", {
            "contract_id": contract_id,
            "contract_type": contract_type,
            "risk_score": risk_score,
            "action": "Contract analysis completed"
        }, user_id)
    
    def log_export(self, contract_id: str, export_format: str, user_id: str = "system") -> str:
        """Log report export"""
        return self.log_event("REPORT_EXPORT", {
            "contract_id": contract_id,
            "format": export_format,
            "action": "Report exported"
        }, user_id)
    
    def log_access(self, contract_id: str, action: str, user_id: str = "system") -> str:
        """Log data access"""
        return self.log_event("DATA_ACCESS", {
            "contract_id": contract_id,
            "action": action
        }, user_id)
    
    def get_entries(self, event_type: str = None, limit: int = 100) -> List[Dict]:
        """Get audit log entries"""
        try:
            with open(self.log_file, 'r') as f:
                log_data = json.load(f)
            
            entries = log_data.get("entries", [])
            
            if event_type:
                entries = [e for e in entries if e.get("event_type") == event_type]
            
            return entries[-limit:]
        
        except Exception as e:
            logger.error(f"Failed to read audit log: {e}")
            return []
    
    def get_contract_history(self, contract_id: str) -> List[Dict]:
        """Get all events for a specific contract"""
        entries = self.get_entries(limit=10000)
        return [e for e in entries if e.get("details", {}).get("contract_id") == contract_id]
    
    def export_audit_log(self, output_path: str = None) -> str:
        """Export audit log for compliance review"""
        if not output_path:
            output_path = self.log_dir / f"audit_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(self.log_file, 'r') as f:
                log_data = json.load(f)
            
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "total_entries": len(log_data.get("entries", [])),
                "entries": log_data.get("entries", [])
            }
            
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            return str(output_path)
        
        except Exception as e:
            logger.error(f"Audit export failed: {e}")
            return ""
