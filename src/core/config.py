from pathlib import Path


# ======================================
# PROJECT ROOT
# ======================================

# Root project directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ======================================
# APPLICATION FOLDERS
# ======================================

# Folder used for raw datasets
DATA_DIR = BASE_DIR / "data"

# Folder used for generated reports
OUTPUT_DIR = BASE_DIR / "output"

# Folder used for application logs
LOG_DIR = BASE_DIR / "logs"

# Folder used for SQLite database
DATABASE_DIR = BASE_DIR / "database"


# ======================================
# OUTPUT FILES
# ======================================

# Generated Excel report
OUTPUT_EXCEL = (
    OUTPUT_DIR / "ecommerce_products.xlsx"
)

# Generated CSV report
OUTPUT_CSV = (
    OUTPUT_DIR / "ecommerce_products.csv"
)

# SQLite database file
DATABASE_PATH = (
    DATABASE_DIR / "products.db"
)


# ======================================
# LOG FILES
# ======================================

# Main application log
LOG_FILE = (
    LOG_DIR / "app.log"
)


# ======================================
# CREATE FOLDERS AUTOMATICALLY
# ======================================

# Create data folder
DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# Create output folder
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# Create logs folder
LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# Create database folder
DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)