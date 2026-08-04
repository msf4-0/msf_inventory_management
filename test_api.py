#!/usr/bin/env python3
"""
Simple Python script to demonstrate using the Inventory Management API.
Shows how to add and delete factory equipment from the database.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def add_equipment(name: str, description: str, quantity: int):
    """Add a new equipment to the inventory."""
    url = f"{BASE_URL}/items/"
    payload = {
        "name": name,
        "description": description,
        "quantity": quantity
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"Added: {response.json()}")
        return response.json()
    else:
        print(f"Error adding equipment: {response.text}")
        return None

def list_equipment():
    """List all equipment in the inventory."""
    url = f"{BASE_URL}/items/"
    response = requests.get(url)
    if response.status_code == 200:
        items = response.json()
        print("\nCurrent Inventory:")
        print("-" * 60)
        for item in items:
            print(f"ID: {item['id']} | Name: {item['name']} | Qty: {item['quantity']} | Desc: {item['description']}")
        print("-" * 60)
        return items
    else:
        print(f"Error listing equipment: {response.text}")
        return []

def delete_equipment_by_id(item_id: int):
    """Delete equipment from the inventory by ID."""
    url = f"{BASE_URL}/items/{item_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        print(f"Deleted item {item_id}: {response.json()}")
        return True
    else:
        print(f"Error deleting equipment: {response.text}")
        return False

def delete_equipment_by_name(item_name: str):
    """Delete equipment from the inventory by name."""
    url = f"{BASE_URL}/items/name/{item_name}"
    response = requests.delete(url)
    if response.status_code == 200:
        print(f"Deleted item '{item_name}': {response.json()}")
        return True
    else:
        print(f"Error deleting equipment: {response.text}")
        return False

def main():
    print("=" * 60)
    print("Factory Equipment Inventory Management - Demo Script")
    print("=" * 60)
    
    # Add some factory equipment
    print("\n1. Adding factory equipment...")
    item1 = add_equipment("CNC Milling Machine", "5-axis CNC milling machine", 2)
    item2 = add_equipment("Industrial Lathe", "Heavy-duty metal lathe", 3)
    item3 = add_equipment("Welding Robot", "Automated welding arm", 1)
    item4 = add_equipment("3D Printer", "Industrial FDM 3D printer", 4)
    
    # List all equipment
    print("\n2. Listing all equipment...")
    list_equipment()
    
    # Delete by ID
    if item2:
        print(f"\n3. Deleting equipment by ID ({item2['id']})...")
        delete_equipment_by_id(item2['id'])
    
    # List again to confirm deletion
    print("\n4. Listing equipment after ID deletion...")
    list_equipment()
    
    # Delete by name
    if item3:
        print(f"\n5. Deleting equipment by name ('{item3['name']}')...")
        delete_equipment_by_name(item3['name'])
    
    # List again to confirm deletion
    print("\n6. Listing equipment after name deletion...")
    list_equipment()
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()