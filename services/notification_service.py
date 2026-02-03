"""
Legifyx Real-Time Notification Service
Handles alerts and notifications for contract analysis events
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import threading
import queue

logger = logging.getLogger(__name__)


class NotificationType(Enum):
    """Types of notifications"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    SUCCESS = "success"
    RISK_ALERT = "risk_alert"
    COMPLIANCE_ALERT = "compliance_alert"
    ANALYSIS_COMPLETE = "analysis_complete"


class NotificationPriority(Enum):
    """Priority levels for notifications"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class Notification:
    """Represents a notification"""
    id: str
    type: NotificationType
    priority: NotificationPriority
    title: str
    message: str
    timestamp: str
    contract_id: Optional[str] = None
    data: Optional[Dict] = None
    read: bool = False
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'type': self.type.value,
            'priority': self.priority.value,
            'title': self.title,
            'message': self.message,
            'timestamp': self.timestamp,
            'contract_id': self.contract_id,
            'data': self.data,
            'read': self.read
        }


class NotificationService:
    """
    Real-time notification service for contract analysis events
    Supports in-app notifications, logging, and callback handlers
    """
    
    def __init__(self, storage_dir: str = None):
        self.storage_dir = Path(storage_dir) if storage_dir else Path.cwd() / "data" / "notifications"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.notifications_file = self.storage_dir / "notifications.json"
        
        self.notifications: List[Notification] = []
        self.notification_queue = queue.Queue()
        self.handlers: List[Callable] = []
        self.running = False
        
        self._load_notifications()
        self._notification_counter = len(self.notifications)
    
    def _load_notifications(self):
        """Load notifications from storage"""
        if self.notifications_file.exists():
            try:
                with open(self.notifications_file, 'r') as f:
                    data = json.load(f)
                    for n in data.get('notifications', []):
                        self.notifications.append(Notification(
                            id=n['id'],
                            type=NotificationType(n['type']),
                            priority=NotificationPriority(n['priority']),
                            title=n['title'],
                            message=n['message'],
                            timestamp=n['timestamp'],
                            contract_id=n.get('contract_id'),
                            data=n.get('data'),
                            read=n.get('read', False)
                        ))
            except Exception as e:
                logger.error(f"Failed to load notifications: {e}")
    
    def _save_notifications(self):
        """Save notifications to storage"""
        try:
            data = {
                'last_updated': datetime.now().isoformat(),
                'notifications': [n.to_dict() for n in self.notifications[-1000:]]
            }
            with open(self.notifications_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save notifications: {e}")
    
    def _generate_id(self) -> str:
        """Generate unique notification ID"""
        self._notification_counter += 1
        return f"NOTIF_{datetime.now().strftime('%Y%m%d%H%M%S')}_{self._notification_counter}"
    
    def register_handler(self, handler: Callable):
        """Register a notification handler callback"""
        self.handlers.append(handler)
    
    def unregister_handler(self, handler: Callable):
        """Unregister a notification handler"""
        if handler in self.handlers:
            self.handlers.remove(handler)
    
    def notify(
        self,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.INFO,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        contract_id: str = None,
        data: Dict = None
    ) -> Notification:
        """
        Create and dispatch a notification
        
        Args:
            title: Notification title
            message: Notification message
            notification_type: Type of notification
            priority: Priority level
            contract_id: Associated contract ID
            data: Additional data
        
        Returns:
            Created notification
        """
        notification = Notification(
            id=self._generate_id(),
            type=notification_type,
            priority=priority,
            title=title,
            message=message,
            timestamp=datetime.now().isoformat(),
            contract_id=contract_id,
            data=data
        )
        
        self.notifications.append(notification)
        self._save_notifications()
        
        # Dispatch to handlers
        for handler in self.handlers:
            try:
                handler(notification)
            except Exception as e:
                logger.error(f"Handler failed: {e}")
        
        return notification
    
    def notify_risk_alert(
        self,
        contract_id: str,
        risk_score: float,
        risk_level: str,
        critical_clauses: List[str]
    ) -> Notification:
        """Send a risk alert notification"""
        priority = NotificationPriority.URGENT if risk_level in ['high', 'critical'] else NotificationPriority.HIGH
        
        return self.notify(
            title=f"⚠️ Risk Alert: {risk_level.upper()} Risk Detected",
            message=f"Contract analysis found {risk_level} risk level with score {risk_score}/10. "
                   f"{len(critical_clauses)} critical clauses identified.",
            notification_type=NotificationType.RISK_ALERT,
            priority=priority,
            contract_id=contract_id,
            data={
                'risk_score': risk_score,
                'risk_level': risk_level,
                'critical_clause_count': len(critical_clauses)
            }
        )
    
    def notify_compliance_issue(
        self,
        contract_id: str,
        compliance_issues: List[Dict]
    ) -> Notification:
        """Send a compliance alert notification"""
        return self.notify(
            title="📋 Compliance Check Required",
            message=f"Found {len(compliance_issues)} potential compliance issues that need attention.",
            notification_type=NotificationType.COMPLIANCE_ALERT,
            priority=NotificationPriority.HIGH,
            contract_id=contract_id,
            data={'issues': compliance_issues}
        )
    
    def notify_analysis_complete(
        self,
        contract_id: str,
        contract_type: str,
        summary: str
    ) -> Notification:
        """Send analysis complete notification"""
        return self.notify(
            title="✅ Contract Analysis Complete",
            message=f"{contract_type} has been analyzed successfully. {summary}",
            notification_type=NotificationType.ANALYSIS_COMPLETE,
            priority=NotificationPriority.MEDIUM,
            contract_id=contract_id
        )
    
    def get_unread(self) -> List[Notification]:
        """Get all unread notifications"""
        return [n for n in self.notifications if not n.read]
    
    def get_by_contract(self, contract_id: str) -> List[Notification]:
        """Get notifications for a specific contract"""
        return [n for n in self.notifications if n.contract_id == contract_id]
    
    def get_by_priority(self, priority: NotificationPriority) -> List[Notification]:
        """Get notifications by priority"""
        return [n for n in self.notifications if n.priority == priority]
    
    def get_recent(self, limit: int = 50) -> List[Notification]:
        """Get recent notifications"""
        return self.notifications[-limit:]
    
    def mark_as_read(self, notification_id: str) -> bool:
        """Mark a notification as read"""
        for n in self.notifications:
            if n.id == notification_id:
                n.read = True
                self._save_notifications()
                return True
        return False
    
    def mark_all_read(self):
        """Mark all notifications as read"""
        for n in self.notifications:
            n.read = True
        self._save_notifications()
    
    def delete_notification(self, notification_id: str) -> bool:
        """Delete a notification"""
        for i, n in enumerate(self.notifications):
            if n.id == notification_id:
                del self.notifications[i]
                self._save_notifications()
                return True
        return False
    
    def clear_all(self):
        """Clear all notifications"""
        self.notifications = []
        self._save_notifications()
    
    def get_stats(self) -> Dict:
        """Get notification statistics"""
        return {
            'total': len(self.notifications),
            'unread': len([n for n in self.notifications if not n.read]),
            'by_type': {
                t.value: len([n for n in self.notifications if n.type == t])
                for t in NotificationType
            },
            'by_priority': {
                p.name: len([n for n in self.notifications if n.priority == p])
                for p in NotificationPriority
            }
        }


class NotificationManager:
    """
    Singleton manager for the notification service
    Provides easy access throughout the application
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.service = NotificationService()
        return cls._instance
    
    @classmethod
    def get_service(cls) -> NotificationService:
        """Get the notification service instance"""
        return cls().service
