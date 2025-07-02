-- Azure Metrics Database Schema Initialization
-- Run this script to manually create the database schema if needed

-- Create database (run this as a superuser if database doesn't exist)
-- CREATE DATABASE azure_metrics;

-- Connect to the azure_metrics database before running the rest

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom types
CREATE TYPE resource_type_enum AS ENUM (
    'Microsoft.Compute/virtualMachines',
    'Microsoft.Web/sites',
    'Microsoft.Sql/servers/databases',
    'Microsoft.Storage/storageAccounts',
    'Microsoft.Insights/components',
    'Microsoft.Network/loadBalancers',
    'Microsoft.KeyVault/vaults',
    'Microsoft.DocumentDB/databaseAccounts',
    'Microsoft.DBforMySQL/servers',
    'Microsoft.DBforPostgreSQL/servers',
    'Microsoft.Compute/virtualMachineScaleSets'
);

CREATE TYPE collection_status_enum AS ENUM (
    'pending',
    'running',
    'completed',
    'failed',
    'partial'
);

CREATE TYPE metric_aggregation_type_enum AS ENUM (
    'Average',
    'Maximum',
    'Minimum',
    'Total',
    'Count'
);

-- Resources table
CREATE TABLE IF NOT EXISTS resources (
    id VARCHAR(500) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    location VARCHAR(50) NOT NULL,
    resource_group VARCHAR(255) NOT NULL,
    subscription_id VARCHAR(36) NOT NULL,
    tags JSONB DEFAULT '{}',
    properties JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_discovered TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Metric definitions table
CREATE TABLE IF NOT EXISTS metric_definitions (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    description TEXT,
    resource_type VARCHAR(100) NOT NULL,
    unit VARCHAR(50) NOT NULL,
    aggregation_types JSONB,
    dimensions JSONB,
    is_enabled BOOLEAN DEFAULT TRUE,
    retention_days INTEGER DEFAULT 30,
    collection_interval_minutes INTEGER DEFAULT 15,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Collection runs table
CREATE TABLE IF NOT EXISTS collection_runs (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4(),
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE,
    status collection_status_enum NOT NULL,
    resource_filters JSONB DEFAULT '{}',
    config JSONB DEFAULT '{}',
    metrics_collected INTEGER DEFAULT 0,
    resources_processed INTEGER DEFAULT 0,
    errors_count INTEGER DEFAULT 0,
    error_details JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Metric data table (partitioned by date for performance)
CREATE TABLE IF NOT EXISTS metric_data (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4(),
    resource_id VARCHAR(500) NOT NULL,
    metric_name VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    aggregation_type metric_aggregation_type_enum NOT NULL,
    dimensions JSONB DEFAULT '{}',
    unit VARCHAR(50),
    collection_run_id VARCHAR(36),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add foreign key constraints
ALTER TABLE metric_data 
ADD CONSTRAINT fk_metric_data_resource 
FOREIGN KEY (resource_id) REFERENCES resources(id) ON DELETE CASCADE;

ALTER TABLE metric_data 
ADD CONSTRAINT fk_metric_data_collection_run 
FOREIGN KEY (collection_run_id) REFERENCES collection_runs(id) ON DELETE SET NULL;

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_resource_type ON resources(resource_type);
CREATE INDEX IF NOT EXISTS idx_resource_group ON resources(resource_group);
CREATE INDEX IF NOT EXISTS idx_subscription_id ON resources(subscription_id);
CREATE INDEX IF NOT EXISTS idx_last_discovered ON resources(last_discovered);

CREATE INDEX IF NOT EXISTS idx_metric_resource_type ON metric_definitions(resource_type);
CREATE INDEX IF NOT EXISTS idx_metric_name ON metric_definitions(name);
CREATE INDEX IF NOT EXISTS idx_metric_enabled ON metric_definitions(is_enabled);

CREATE INDEX IF NOT EXISTS idx_metric_resource_id ON metric_data(resource_id);
CREATE INDEX IF NOT EXISTS idx_metric_name_timestamp ON metric_data(metric_name, timestamp);
CREATE INDEX IF NOT EXISTS idx_metric_timestamp ON metric_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_metric_collection_run ON metric_data(collection_run_id);
CREATE INDEX IF NOT EXISTS idx_metric_resource_metric_time ON metric_data(resource_id, metric_name, timestamp);

CREATE INDEX IF NOT EXISTS idx_collection_start_time ON collection_runs(start_time);
CREATE INDEX IF NOT EXISTS idx_collection_status ON collection_runs(status);
CREATE INDEX IF NOT EXISTS idx_collection_created_at ON collection_runs(created_at);

-- Update triggers for updated_at columns
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_resources_updated_at 
    BEFORE UPDATE ON resources 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_metric_definitions_updated_at 
    BEFORE UPDATE ON metric_definitions 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create a function to clean up old metric data
CREATE OR REPLACE FUNCTION cleanup_old_metric_data(retention_days INTEGER DEFAULT 30)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM metric_data 
    WHERE timestamp < (NOW() - INTERVAL '1 day' * retention_days);
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    RETURN deleted_count;
END;
$$ language 'plpgsql';

-- Create a view for recent collection runs with statistics
CREATE OR REPLACE VIEW recent_collection_runs AS
SELECT 
    cr.id,
    cr.start_time,
    cr.end_time,
    cr.status,
    cr.metrics_collected,
    cr.resources_processed,
    cr.errors_count,
    EXTRACT(EPOCH FROM (COALESCE(cr.end_time, NOW()) - cr.start_time))/60 as duration_minutes,
    cr.created_at
FROM collection_runs cr
ORDER BY cr.created_at DESC
LIMIT 50;

-- Create a view for resource summary statistics
CREATE OR REPLACE VIEW resource_summary AS
SELECT 
    resource_type,
    COUNT(*) as resource_count,
    COUNT(DISTINCT resource_group) as resource_groups,
    COUNT(DISTINCT subscription_id) as subscriptions,
    MAX(last_discovered) as last_discovery
FROM resources
GROUP BY resource_type
ORDER BY resource_count DESC;

-- Insert some sample metric definitions for common Azure resources
INSERT INTO metric_definitions (name, display_name, description, resource_type, unit, aggregation_types, dimensions) VALUES
('Percentage CPU', 'CPU Percentage', 'The percentage of allocated compute units that are currently in use', 'Microsoft.Compute/virtualMachines', 'Percent', '["Average", "Maximum"]', '[]'),
('Network In Total', 'Network In', 'The number of bytes received on all network interfaces', 'Microsoft.Compute/virtualMachines', 'Bytes', '["Total"]', '[]'),
('Network Out Total', 'Network Out', 'The number of bytes sent out on all network interfaces', 'Microsoft.Compute/virtualMachines', 'Bytes', '["Total"]', '[]'),
('Disk Read Bytes', 'Disk Read Bytes', 'Bytes read from disk during monitoring period', 'Microsoft.Compute/virtualMachines', 'Bytes', '["Total"]', '[]'),
('Disk Write Bytes', 'Disk Write Bytes', 'Bytes written to disk during monitoring period', 'Microsoft.Compute/virtualMachines', 'Bytes', '["Total"]', '[]'),

('Requests', 'Requests', 'The total number of requests', 'Microsoft.Web/sites', 'Count', '["Total", "Count"]', '[]'),
('Response Time', 'Response Time', 'The time taken for the app to serve requests', 'Microsoft.Web/sites', 'Seconds', '["Average"]', '[]'),
('Http Server Errors', 'HTTP Server Errors', 'The count of requests resulting in HTTP status codes >= 500', 'Microsoft.Web/sites', 'Count', '["Total"]', '[]'),
('Memory Percentage', 'Memory Percentage', 'The percentage of memory used by the app', 'Microsoft.Web/sites', 'Percent', '["Average"]', '[]'),

('DTU Consumption Percent', 'DTU Percentage', 'Database Transaction Unit consumption percentage', 'Microsoft.Sql/servers/databases', 'Percent', '["Average", "Maximum"]', '[]'),
('Connection Successful', 'Successful Connections', 'Number of successful connections', 'Microsoft.Sql/servers/databases', 'Count', '["Total"]', '[]'),
('Database Size', 'Database Size', 'Database size in bytes', 'Microsoft.Sql/servers/databases', 'Bytes', '["Maximum"]', '[]'),

('Used Capacity', 'Used Capacity', 'The amount of storage used by the storage account', 'Microsoft.Storage/storageAccounts', 'Bytes', '["Average"]', '[]'),
('Transactions', 'Transactions', 'The number of requests made to a storage service', 'Microsoft.Storage/storageAccounts', 'Count', '["Total"]', '[]'),
('Availability', 'Availability', 'The percentage of availability for the storage service', 'Microsoft.Storage/storageAccounts', 'Percent', '["Average"]', '[]')

ON CONFLICT (name, resource_type) DO NOTHING;

-- Grant permissions (adjust as needed for your setup)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO azure_metrics_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO azure_metrics_user;

COMMIT;