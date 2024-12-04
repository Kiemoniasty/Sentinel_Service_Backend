BASE_URL = "/api/v1"

# flask
INIT_APP = "Initializing app..."
INIT_SCHEDULER = "Initializing scheduler..."
SCHD_RETRIVED = "Retrieving tasks list"
API_RDY = "Endopoints ready"
APP_RDY = "Sentinel app is ready"

# ServiceController
SCHD_NEW1 = "STARTED NEW TASK: '"
SCHD_NEW2 = "' ("
SCHD_NEW3 = ") scheduled successfully."
SCHD_RES1 = "RESTARTED TASK: '"
SCHD_RES2 = "' ("
SCHD_RES3 = ") rescheduled successfully."
SCHD_STOP1 = "STOPPED TASK: '"
SCHD_STOP2 = "' ("
SCHD_STOP3 = ") stopped successfully."

# UserController
USR_NEW1 = "User: '"
USR_NEW2 = "' created successfully."
USR_UPD1 = "User: '"
USR_UPD2 = "' updated successfully."
USR_DEL1 = "User: '"
USR_DEL2 = "' deleted successfully."

# InfluxTools
BKT_NEW1 = "Bucket '"
BKT_NEW2 = "' created successfully."
BKT_DEL1 = "Bucket '"
BKT_DEL2 = "' deleted successfully."
BKT_ERROR = "Error while creating bucket: "

# StateChecker
SCHD_READY = "All tasks scheduled."
SCHD_RUNNING = "Background scheduler started."
SCHD_STOP_TAG1 = "Task with tag '"
SCHD_STOP_TAG2 = "' has been stopped."
SCHD_STOP = "Background scheduler stopped."

# InitPostgresDBs
INIT_PG = "Starting initialization of Postgres databases"
PG_CONN = "Connected to database"
PG_FETCHED = "Fetched databases"
SENDB_CREATED = "sentinel_db database created"
SENDB_EXISTS = "sentinel_db database already exists"
USRDB_CREATED = "user_db database created"
USRDB_EXISTS = "user_db database already exists"
PG_CLOSED = "Connection closed"
