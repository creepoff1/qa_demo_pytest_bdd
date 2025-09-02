"""
Test data loading utilities.
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class DataLoader:
    """Utility class for loading test data from JSON files."""
    
    def __init__(self, data_dir: Path = None):
        """Initialize DataLoader with data directory path."""
        if data_dir is None:
            # Default to tests/data directory
            self.data_dir = Path(__file__).resolve().parent.parent / "data"
        else:
            self.data_dir = Path(data_dir)
    
    def load_json(self, filename: str) -> Dict[str, Any]:
        """
        Load JSON data from file.
        
        Args:
            filename: Name of the JSON file (with or without .json extension)
            
        Returns:
            Dictionary containing the JSON data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        if not filename.endswith('.json'):
            filename += '.json'
            
        file_path = self.data_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Test data file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.debug(f"Loaded test data from {filename}")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {filename}: {e}")
            raise
    
    def get_auth_data(self) -> Dict[str, Any]:
        """Get authentication test data."""
        return self.load_json('auth_data')
    
    def get_user_data(self) -> Dict[str, Any]:
        """Get user test data."""
        return self.load_json('user_data')
    
    def get_resource_data(self) -> Dict[str, Any]:
        """Get resource test data."""
        return self.load_json('resource_data')
    
    def get_valid_users(self) -> List[Dict[str, Any]]:
        """Get list of valid users for authentication."""
        auth_data = self.get_auth_data()
        return auth_data.get('valid_users', [])
    
    def get_invalid_users(self) -> List[Dict[str, Any]]:
        """Get list of invalid users for authentication."""
        auth_data = self.get_auth_data()
        return auth_data.get('invalid_users', [])
    
    def get_existing_user_ids(self) -> List[int]:
        """Get list of existing user IDs."""
        user_data = self.get_user_data()
        return user_data.get('existing_user_ids', [])
    
    def get_non_existing_user_ids(self) -> List[int]:
        """Get list of non-existing user IDs."""
        user_data = self.get_user_data()
        return user_data.get('non_existing_user_ids', [])

# Global instance
data_loader = DataLoader()
