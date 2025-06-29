"""Constants for Azure database metrics collection."""

# Time constants
SECONDS_PER_MINUTE = 60
DEFAULT_LOOKBACK_DAYS = 7

# Metric aggregation types
AGGREGATION_AVERAGE = "Average"
AGGREGATION_MAXIMUM = "Maximum"
AGGREGATION_MINIMUM = "Minimum"
AGGREGATION_TOTAL = "Total"

# Default thresholds
DEFAULT_CPU_THRESHOLD = 40.0
DEFAULT_MEMORY_THRESHOLD = 40.0
DEFAULT_DTU_THRESHOLD = 40.0
DEFAULT_STORAGE_THRESHOLD = 80.0

# Database types
DATABASE_TYPE_SQL = 'sql'
DATABASE_TYPE_POSTGRESQL = 'postgresql'
DATABASE_TYPE_MYSQL = 'mysql'

# Recommendation severities
SEVERITY_HIGH = 'high'
SEVERITY_MEDIUM = 'medium'
SEVERITY_LOW = 'low'

# Recommendation types
RECOMMENDATION_DOWNSIZE = 'downsize'
RECOMMENDATION_UPSIZE = 'upsize'
RECOMMENDATION_OPTIMIZE = 'optimize'
RECOMMENDATION_STORAGE = 'storage'

# Impact types
IMPACT_COST = 'cost'
IMPACT_PERFORMANCE = 'performance'
IMPACT_AVAILABILITY = 'availability'
IMPACT_GOVERNANCE = 'governance'