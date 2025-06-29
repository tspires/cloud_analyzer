"""Example usage of Azure database metrics wrapper."""
import asyncio
from datetime import datetime, timedelta

from azure.identity import DefaultAzureCredential

from .client import AzureDatabaseMetricsWrapper


async def main():
    """Example usage of the Azure database metrics wrapper."""
    # Initialize the wrapper
    wrapper = AzureDatabaseMetricsWrapper(
        credential=DefaultAzureCredential(),
        subscription_id="your-subscription-id"
    )
    
    try:
        # Example 1: Get metrics for a specific SQL database
        sql_resource_id = "/subscriptions/xxx/resourceGroups/rg/providers/Microsoft.Sql/servers/server/databases/db"
        sql_metrics = await wrapper.get_database_metrics(
            resource_id=sql_resource_id,
            time_range=(datetime.utcnow() - timedelta(days=7), datetime.utcnow())
        )
        
        print(f"SQL Database: {sql_metrics.database_name}")
        print(f"  CPU Average: {sql_metrics.cpu_percent_avg:.2f}%")
        print(f"  CPU Max: {sql_metrics.cpu_percent_max:.2f}%")
        print(f"  Storage: {sql_metrics.storage_percent_avg:.2f}%")
        
        # Example 2: List all databases
        all_databases = await wrapper.list_all_databases()
        
        print("\nAll Databases in Subscription:")
        for db_type, databases in all_databases.items():
            print(f"\n{db_type.upper()} Databases:")
            for db in databases:
                print(f"  - {db['name']} ({db.get('location', 'unknown')})")
        
        # Example 3: Get metrics for all databases
        all_metrics = await wrapper.get_all_database_metrics(
            time_range=(datetime.utcnow() - timedelta(days=1), datetime.utcnow()),
            database_types=['sql', 'postgresql']  # Only SQL and PostgreSQL
        )
        
        print(f"\nCollected metrics for {len(all_metrics)} databases")
        
        # Example 4: Get optimization recommendations
        recommendations = await wrapper.get_optimization_recommendations(
            resource_id=sql_resource_id,
            metrics=sql_metrics
        )
        
        if recommendations:
            print(f"\nRecommendations for {sql_metrics.database_name}:")
            for rec in recommendations:
                print(f"  - [{rec['severity']}] {rec['description']}")
                print(f"    Action: {rec['action']}")
        
        # Example 5: Get recommendations for all databases
        all_recommendations = await wrapper.get_optimization_recommendations(
            include_all=True
        )
        
        print(f"\nOptimization opportunities found for {len(all_recommendations)} databases")
        
        # Example 6: Custom error handling
        try:
            invalid_resource = "/subscriptions/xxx/invalid/resource"
            await wrapper.get_database_metrics(invalid_resource)
        except Exception as e:
            print(f"\nExpected error for invalid resource: {e}")
        
    finally:
        # Clean up
        await wrapper.close()


if __name__ == "__main__":
    asyncio.run(main())