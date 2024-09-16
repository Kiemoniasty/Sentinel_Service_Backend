"""Enum list for service_statuses table"""

from enum import Enum


class Status(Enum):
    """Enum list for status column in settings table"""

    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    INACTIVE = "inactive"


class Response(Enum):
    """Enum list of state column for state_logger table"""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


class LoggerMessages(Enum):
    """Enum list for message column in state_logger table"""

    AVAILABLE = "Info: Service is up."
    UNAVAILABLE = "Error: Service is not responding."
    MAINTENANCE = "Info: Service is under maintenance."
    OVERLOAD = "Warning: Service is under heavy load."
    SLOW_RESPONSE = "Warning: Service is responding slowly."
    CREATED = "Info: New service signed."


class Codes(Enum):
    """Enum list for code column in state_logger table"""

    I001 = "INFO: Service started successfully"
    I002 = "INFO: Service stopped"
    I003 = "INFO: Configuration loaded successfully"
    I004 = "INFO: Health check passed"
    I005 = "INFO: User logged in successfully"
    I006 = "INFO: User logged out"
    I007 = "INFO: Service restarted successfully"
    I008 = "INFO: Backup completed successfully"

    W001 = "WARNING: High latency detected for service"
    W002 = "WARNING: High memory usage detected for service"
    W003 = "WARNING: Low disk space on server"
    W004 = "WARNING: Unusual activity detected on service"
    W005 = "WARNING: SSL certificate expiring soon"
    W006 = "WARNING: Deprecated configuration detected"
    W007 = "WARNING: Health check returned warnings"
    W008 = "WARNING: Service restart required to apply changes"

    E001 = "ERROR: Connection to service timed out"
    E002 = "ERROR: Service unreachable"
    E003 = "ERROR: Authentication failed for service"
    E004 = "ERROR: Unauthorized access attempt detected"
    E005 = "ERROR: Service is currently down"
    E006 = "ERROR: SSL certificate expired"
    E007 = "ERROR: Database connection failed"
    E008 = "ERROR: Configuration error detected"


class NotificationMessages(Enum):
    """Enum list for message column in notification_logger table"""

    BASE = "Service: "
    ERROR = "is not responding."
    WARNING = "needs attention."
    MAINTENANCE_START = "is started maintenance."
    MAINTENANCE_END = "maintenance is done."
    CREATED = "was signed successfully."
