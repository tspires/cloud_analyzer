#!/usr/bin/env python3
"""Script to run cloud analyzer checks against Azure environment."""

import asyncio
import sys
import os
from decimal import Decimal
from datetime import datetime, timezone

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cloud_analyzer.common', 'src'))

# Import required modules
from models.base import CloudProvider, Resource, ResourceType
from checks.storage.unattached_volumes import UnattachedVolumesCheck
from checks.storage.old_snapshots import OldSnapshotsCheck
from checks.cost_optimization.reserved_instances import ReservedInstancesUtilizationCheck
from checks.cost_optimization.savings_plans import SavingsPlansCoverageCheck
from checks.database.database_sizing import DatabaseSizingCheck
from checks.base import CheckRunner
from providers.azure import AzureProvider
from providers.base import ProviderFactory, CloudProvider

# Register Azure provider
ProviderFactory.register(CloudProvider.AZURE, AzureProvider)


async def run_azure_checks():
    """Run all checks against Azure environment."""
    print("🔍 Cloud Analyzer - Azure Environment Analysis")
    print("=" * 50)
    
    # Get subscription ID from Azure CLI or environment
    subscription_id = os.environ.get('AZURE_SUBSCRIPTION_ID')
    if not subscription_id:
        # Try to get from Azure CLI
        try:
            import subprocess
            result = subprocess.run(['az', 'account', 'show', '--query', 'id', '-o', 'tsv'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                subscription_id = result.stdout.strip()
        except:
            pass
    
    if not subscription_id:
        subscription_id = "ca4f389b-4856-460f-8b5d-afffe6921e2e"  # From az account show
    
    print(f"✅ Using Azure Subscription: {subscription_id[:8]}...")
    
    try:
        # Initialize Azure provider with subscription ID
        provider = AzureProvider(subscription_id=subscription_id)
        await provider.initialize()
        
        print("\n📊 Fetching Azure resources...")
        
        # Fetch resources
        resources = await provider.list_resources()
        
        if not resources:
            print("⚠️  No resources found in the Azure subscription")
            return
        
        print(f"✅ Found {len(resources)} resources")
        
        # Group resources by type
        resource_types = {}
        for resource in resources:
            if resource.type not in resource_types:
                resource_types[resource.type] = 0
            resource_types[resource.type] += 1
        
        print("\n📋 Resource Summary:")
        for rtype, count in resource_types.items():
            # rtype is already a string from the enum
            print(f"  - {rtype}: {count}")
        
        # Initialize checks
        checks = [
            UnattachedVolumesCheck(),
            OldSnapshotsCheck(),
            ReservedInstancesUtilizationCheck(),
            SavingsPlansCoverageCheck(),
            DatabaseSizingCheck(),
        ]
        
        # Filter checks that support Azure
        azure_checks = [check for check in checks if CloudProvider.AZURE in check.supported_providers]
        
        print(f"\n🔧 Running {len(azure_checks)} optimization checks...")
        
        # Run checks
        check_runner = CheckRunner(provider)
        all_results = []
        
        for check in azure_checks:
            print(f"\n  ▶️  Running: {check.name}")
            try:
                results = await check_runner.run_check(check, resources)
                all_results.extend(results)
                print(f"     ✅ Found {len(results)} issues")
            except Exception as e:
                print(f"     ❌ Error: {str(e)}")
        
        # Display results
        print("\n" + "=" * 50)
        print("📊 ANALYSIS RESULTS")
        print("=" * 50)
        
        if not all_results:
            print("\n✨ No optimization opportunities found! Your Azure environment is well-optimized.")
            return
        
        # Group results by severity
        by_severity = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': [],
            'info': []
        }
        
        for result in all_results:
            by_severity[result.severity].append(result)
        
        # Calculate total savings
        total_monthly_savings = sum(r.monthly_savings for r in all_results)
        total_annual_savings = sum(r.annual_savings for r in all_results)
        
        print(f"\n💰 Total Potential Savings:")
        print(f"   Monthly: ${total_monthly_savings:,.2f}")
        print(f"   Annual:  ${total_annual_savings:,.2f}")
        
        # Display results by severity
        for severity in ['critical', 'high', 'medium', 'low', 'info']:
            results = by_severity[severity]
            if results:
                print(f"\n🔴 {severity.upper()} Priority ({len(results)} issues)")
                print("-" * 40)
                
                for result in results[:5]:  # Show top 5 per severity
                    print(f"\n📌 {result.title}")
                    print(f"   Resource: {result.resource.name} ({result.resource.type.value})")
                    print(f"   Region: {result.resource.region}")
                    print(f"   Monthly Savings: ${result.monthly_savings:,.2f}")
                    print(f"   {result.description}")
                
                if len(results) > 5:
                    print(f"\n   ... and {len(results) - 5} more {severity} issues")
        
        # Summary
        print("\n" + "=" * 50)
        print("📈 SUMMARY")
        print("=" * 50)
        print(f"Total Issues Found: {len(all_results)}")
        print(f"Critical: {len(by_severity['critical'])}")
        print(f"High: {len(by_severity['high'])}")
        print(f"Medium: {len(by_severity['medium'])}")
        print(f"Low: {len(by_severity['low'])}")
        print(f"Info: {len(by_severity['info'])}")
        
    except Exception as e:
        print(f"\n❌ Error running analysis: {str(e)}")
        print("\nPlease ensure you have:")
        print("1. Valid Azure credentials set as environment variables")
        print("2. Azure CLI installed and authenticated")
        print("3. Necessary permissions to read resources in your subscription")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(run_azure_checks())