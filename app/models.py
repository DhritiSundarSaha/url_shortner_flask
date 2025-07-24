# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata
# app/models.py

from datetime import datetime
from threading import Lock

# This dictionary will act as our in-memory database.
# The structure will be:
# {
#   "short_code": {
#     "original_url": "https://...",
#     "created_at": "2024-01-01T10:00:00",
#     "clicks": 0
#   }
# }
url_db = {}

# A lock to handle thread safety when modifying the url_db dictionary.
# This prevents issues if multiple people click a link at the exact same time.
db_lock = Lock()