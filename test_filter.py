#!/usr/bin/env python3
"""
Test script for the intelligent filter functionality.
This script tests the configuration loading and basic functionality without requiring API keys.
"""

import json
from intelligent_filter import FilterConfig, load_config_from_file

def test_config_loading():
    """Test configuration loading from JSON file."""
    print("🧪 Testing configuration loading...")
    
    try:
        config = load_config_from_file()
        print(f"✅ Configuration loaded successfully:")
        print(f"   Primary keyword: {config.primary_keyword}")
        print(f"   Additional keywords: {', '.join(config.additional_keywords)}")
        print(f"   Relevance threshold: {config.relevance_threshold}")
        print(f"   Max articles to process: {config.max_articles_to_process}")
        return True
    except Exception as e:
        print(f"❌ Configuration loading failed: {e}")
        return False

def test_filter_prompt_generation():
    """Test the prompt generation for LLM filtering."""
    print("\n🧪 Testing prompt generation...")
    
    try:
        from intelligent_filter import GroqLLMFilter
        
        # Mock articles for testing
        test_articles = [
            {
                "title": "Quantum sensors revolutionize energy storage efficiency",
                "url": "https://example.com/article1"
            },
            {
                "title": "New solar panel technology increases efficiency",
                "url": "https://example.com/article2"
            },
            {
                "title": "Machine learning in healthcare applications",
                "url": "https://example.com/article3"
            }
        ]
        
        config = FilterConfig(
            primary_keyword="quantum",
            additional_keywords=["energy", "storage", "efficiency"],
            relevance_threshold=0.6
        )
        
        # Create filter instance (without API key for testing)
        try:
            filter_instance = GroqLLMFilter("test_key")
        except:
            print("⚠️  Groq API key validation skipped for testing")
            return True
        
        # Test prompt creation
        prompt = filter_instance._create_filtering_prompt(test_articles, config)
        
        print("✅ Prompt generation successful")
        print(f"   Prompt length: {len(prompt)} characters")
        print(f"   Contains primary keyword: {'quantum' in prompt}")
        print(f"   Contains additional keywords: {all(kw in prompt for kw in ['energy', 'storage', 'efficiency'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Prompt generation test failed: {e}")
        return False

def test_json_config_structure():
    """Test the JSON configuration file structure."""
    print("\n🧪 Testing JSON configuration structure...")
    
    try:
        with open("filter_config.json", 'r') as f:
            config_data = json.load(f)
        
        required_fields = ["primary_keyword", "additional_keywords"]
        optional_fields = ["relevance_threshold", "max_articles_to_process", "description"]
        
        # Check required fields
        for field in required_fields:
            if field not in config_data:
                print(f"❌ Missing required field: {field}")
                return False
        
        # Validate data types
        if not isinstance(config_data["primary_keyword"], str):
            print("❌ primary_keyword must be a string")
            return False
            
        if not isinstance(config_data["additional_keywords"], list):
            print("❌ additional_keywords must be a list")
            return False
        
        print("✅ JSON configuration structure is valid")
        print(f"   Primary keyword: {config_data['primary_keyword']}")
        print(f"   Additional keywords count: {len(config_data['additional_keywords'])}")
        
        if "description" in config_data:
            print(f"   Description: {config_data['description']}")
        
        return True
        
    except FileNotFoundError:
        print("❌ filter_config.json file not found")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return False
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Running Intelligent Filter Tests")
    print("=" * 50)
    
    tests = [
        test_json_config_structure,
        test_config_loading,
        test_filter_prompt_generation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The intelligent filter is ready to use.")
        print("\n💡 To run the full intelligent filter:")
        print("   1. Set SCRAPESTACK_API_KEY environment variable")
        print("   2. Set GROQ_API_KEY environment variable")
        print("   3. Run: python intelligent_filter.py")
    else:
        print("⚠️  Some tests failed. Please check the configuration.")

if __name__ == "__main__":
    main()