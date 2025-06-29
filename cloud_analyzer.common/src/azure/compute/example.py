"""Example usage of Azure compute metrics wrapper."""
import asyncio
from datetime import datetime, timedelta, timezone

from azure.identity import DefaultAzureCredential

from .client import AzureComputeMetricsWrapper


async def main():
    """Example usage of the Azure compute metrics wrapper."""
    # Initialize the wrapper
    wrapper = AzureComputeMetricsWrapper(
        credential=DefaultAzureCredential(),
        subscription_id="your-subscription-id",
        concurrent_requests=20  # Handle up to 20 concurrent API calls
    )
    
    try:
        # Example 1: Get metrics for a specific Virtual Machine
        vm_resource_id = "/subscriptions/xxx/resourceGroups/rg/providers/Microsoft.Compute/virtualMachines/myvm"
        vm_metrics = await wrapper.get_compute_metrics(
            resource_id=vm_resource_id,
            time_range=(datetime.now(timezone.utc) - timedelta(days=7), datetime.now(timezone.utc))
        )
        
        print(f"Virtual Machine: {vm_metrics.resource_name}")
        print(f"  CPU Average: {vm_metrics.cpu_percent_avg:.2f}%")
        print(f"  CPU Max: {vm_metrics.cpu_percent_max:.2f}%")
        print(f"  Memory Average: {vm_metrics.memory_percent_avg:.2f}%" if vm_metrics.memory_percent_avg else "  Memory: N/A")
        print(f"  State: {vm_metrics.state}")
        
        # Example 2: Get metrics for an App Service
        app_resource_id = "/subscriptions/xxx/resourceGroups/rg/providers/Microsoft.Web/sites/myapp"
        app_metrics = await wrapper.get_compute_metrics(app_resource_id)
        
        print(f"\nApp Service: {app_metrics.resource_name}")
        print(f"  CPU: {app_metrics.cpu_percent_avg:.2f}%")
        print(f"  Response Time: {app_metrics.response_time_avg:.0f}ms")
        print(f"  Total Requests: {app_metrics.request_count}")
        print(f"  Error Count: {app_metrics.error_count}")
        
        # Example 3: List all compute resources
        all_resources = await wrapper.list_all_compute_resources()
        
        print("\nAll Compute Resources:")
        for resource_type, resources in all_resources.items():
            print(f"\n{resource_type}:")
            for resource in resources[:5]:  # Show first 5
                print(f"  - {resource['name']} ({resource.get('location', 'unknown')})")
        
        # Example 4: Get metrics for all VMs with specific tags
        all_metrics = await wrapper.get_all_compute_metrics(
            resource_types=['virtual_machines'],
            resource_filter={
                'tags': {'environment': 'production'},
                'locations': ['eastus', 'westus']
            }
        )
        
        print(f"\nCollected metrics for {len(all_metrics)} production VMs")
        
        # Example 5: Get optimization recommendations for a specific VM
        recommendations = await wrapper.get_optimization_recommendations(
            resource_id=vm_resource_id,
            metrics=vm_metrics
        )
        
        if recommendations:
            print(f"\nRecommendations for {vm_metrics.resource_name}:")
            for rec in recommendations:
                print(f"  - [{rec.severity}] {rec.description}")
                if rec.estimated_annual_savings:
                    print(f"    Potential savings: ${rec.estimated_annual_savings:,.0f}/year")
        
        # Example 6: Get cost optimization summary for all resources
        cost_summary = await wrapper.get_cost_optimization_summary()
        
        print("\nCost Optimization Summary:")
        print(f"  Total resources analyzed: {cost_summary['total_resources_analyzed']}")
        print(f"  Resources with recommendations: {cost_summary['resources_with_recommendations']}")
        print(f"  Total recommendations: {cost_summary['total_recommendations']}")
        print(f"  Estimated annual savings: ${cost_summary['estimated_annual_savings']:,.0f}")
        
        print("\nTop Cost Optimization Opportunities:")
        for i, opportunity in enumerate(cost_summary['top_opportunities'][:5], 1):
            print(f"  {i}. {opportunity['resource_name']}: ${opportunity['annual_savings']:,.0f}/year")
            print(f"     {opportunity['recommendation']}")
        
        # Example 7: Batch process multiple resources efficiently
        resource_ids = [
            "/subscriptions/xxx/.../virtualMachines/vm1",
            "/subscriptions/xxx/.../virtualMachines/vm2",
            "/subscriptions/xxx/.../sites/app1",
            "/subscriptions/xxx/.../sites/app2"
        ]
        
        # Get metrics for multiple resources concurrently
        tasks = [wrapper.get_compute_metrics(rid) for rid in resource_ids]
        batch_metrics = await asyncio.gather(*tasks, return_exceptions=True)
        
        print(f"\nBatch processed {len(batch_metrics)} resources")
        
        # Example 8: Filter recommendations by type
        all_recommendations = await wrapper.get_optimization_recommendations(
            include_all=True,
            recommendation_types=['resize', 'shutdown', 'reserved_instance']
        )
        
        resize_count = sum(
            1 for recs in all_recommendations.values()
            for rec in recs
            if rec.recommendation_type == 'resize'
        )
        print(f"\nFound {resize_count} resize recommendations across all resources")
        
    except Exception as e:
        print(f"\nError: {e}")
    
    finally:
        # Clean up
        await wrapper.close()


async def advanced_example():
    """Advanced example with custom error handling and monitoring."""
    wrapper = AzureComputeMetricsWrapper(
        subscription_id="your-subscription-id",
        retry_count=5,
        retry_delay=2.0,
        timeout=60.0,
        concurrent_requests=50
    )
    
    try:
        # Monitor VM performance over time
        vm_id = "/subscriptions/xxx/.../virtualMachines/critical-vm"
        
        # Get hourly metrics for the last 24 hours
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=1)
        
        metrics = await wrapper.get_compute_metrics(
            resource_id=vm_id,
            time_range=(start_time, end_time),
            aggregation="Average",
            interval=timedelta(hours=1)  # Hourly granularity
        )
        
        # Check for performance issues
        if metrics.cpu_percent_p95 and metrics.cpu_percent_p95 > 90:
            print(f"WARNING: VM {metrics.resource_name} has high CPU usage (95th percentile: {metrics.cpu_percent_p95:.1f}%)")
        
        if metrics.memory_percent_max and metrics.memory_percent_max > 85:
            print(f"WARNING: VM {metrics.resource_name} has high memory usage (max: {metrics.memory_percent_max:.1f}%)")
        
        # Get App Service metrics with error rate analysis
        app_id = "/subscriptions/xxx/.../sites/critical-app"
        app_metrics = await wrapper.get_compute_metrics(app_id)
        
        if app_metrics.request_count and app_metrics.error_count:
            error_rate = (app_metrics.error_count / app_metrics.request_count) * 100
            if error_rate > 1:
                print(f"ALERT: App {app_metrics.resource_name} has {error_rate:.2f}% error rate")
                
                # Get detailed HTTP status breakdown
                http_4xx = app_metrics.additional_metrics.get('http_4xx_count', 0)
                http_5xx = app_metrics.additional_metrics.get('http_5xx_count', 0)
                print(f"  4xx errors: {http_4xx}")
                print(f"  5xx errors: {http_5xx}")
        
    finally:
        await wrapper.close()


if __name__ == "__main__":
    # Run the basic example
    asyncio.run(main())
    
    # Run the advanced example
    # asyncio.run(advanced_example())