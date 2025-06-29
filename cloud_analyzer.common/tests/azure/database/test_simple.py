"""Simple test to verify test environment."""
import pytest
from unittest.mock import MagicMock
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))


class TestSimple:
    """Simple test cases."""
    
    def test_basic_assertion(self):
        """Test basic assertion."""
        assert 1 + 1 == 2
    
    def test_mock_usage(self):
        """Test mock usage."""
        mock = MagicMock()
        mock.method.return_value = "test"
        assert mock.method() == "test"
    
    @pytest.mark.asyncio
    async def test_async_function(self):
        """Test async function."""
        async def async_func():
            return "async result"
        
        result = await async_func()
        assert result == "async result"