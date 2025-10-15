"""
Test script for Leaf Disease Detection API
Run this to verify your API is working correctly
"""

import requests
import json
from pathlib import Path
import sys

API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    print("\nTesting root endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint passed")
            data = response.json()
            print(f"   API Version: {data.get('version')}")
            print(f"   Available Endpoints: {list(data.get('endpoints', {}).keys())}")
            return True
        else:
            print(f"❌ Root endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint failed: {str(e)}")
        return False

def test_analyze_endpoint(image_path=None):
    """Test the analyze endpoint with an image"""
    print("\nTesting analyze endpoint...")
    
    if image_path and Path(image_path).exists():
        print(f"   Using provided image: {image_path}")
        try:
            with open(image_path, "rb") as f:
                files = {"file": (Path(image_path).name, f, "image/jpeg")}
                response = requests.post(
                    f"{API_BASE_URL}/analyze",
                    files=files,
                    timeout=30
                )
                
            if response.status_code == 200:
                print("✅ Analyze endpoint passed")
                data = response.json()
                print(f"\n   Analysis Results:")
                print(f"   Disease: {data.get('disease_name')}")
                print(f"   Confidence: {data.get('confidence')}")
                print(f"   Severity: {data.get('severity')}")
                print(f"   Symptoms: {len(data.get('symptoms', []))} found")
                print(f"   Treatments: {len(data.get('treatment', []))} recommended")
                print(f"   Prevention: {len(data.get('prevention', []))} measures")
                
                # Save result to file
                output_file = "test_analysis_result.json"
                with open(output_file, "w") as f:
                    json.dump(data, f, indent=2)
                print(f"\n   📄 Full results saved to: {output_file}")
                return True
            else:
                print(f"❌ Analyze endpoint failed with status {response.status_code}")
                print(f"   Error: {response.json()}")
                return False
        except Exception as e:
            print(f"❌ Analyze endpoint failed: {str(e)}")
            return False
    else:
        print("⚠️  No test image provided or image not found")
        print("   To test the analyze endpoint, run:")
        print(f"   python {sys.argv[0]} path/to/your/leaf/image.jpg")
        return None

def main():
    """Run all tests"""
    print("=" * 60)
    print("Leaf Disease Detection API - Test Suite")
    print("=" * 60)
    
    results = {
        "health_check": test_health_check(),
        "root_endpoint": test_root_endpoint(),
    }
    
    # Check if image path provided
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    analyze_result = test_analyze_endpoint(image_path)
    if analyze_result is not None:
        results["analyze_endpoint"] = analyze_result
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    
    for test, result in results.items():
        status = "✅ PASSED" if result else ("❌ FAILED" if result is False else "⚠️  SKIPPED")
        print(f"{test.replace('_', ' ').title()}: {status}")
    
    print(f"\nTotal: {passed} passed, {failed} failed, {skipped} skipped")
    print("=" * 60)
    
    if failed == 0 and passed > 0:
        print("\n🎉 All tests passed! Your API is working correctly.")
    elif failed > 0:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
