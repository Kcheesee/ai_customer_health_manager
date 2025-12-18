import sys
import os
sys.path.append(os.getcwd())
from app.core.database import SessionLocal
from app.models.llm_config import LLMConfiguration
from app.core.security import encrypt_string, decrypt_string

def test_encryption_logic():
    print("Testing Encryption Logic...")
    original = "sk-test-12345678"
    encrypted = encrypt_string(original)
    print(f"Original: {original}")
    print(f"Encrypted: {encrypted}")
    
    assert original != encrypted
    
    decrypted = decrypt_string(encrypted)
    print(f"Decrypted: {decrypted}")
    
    assert original == decrypted
    print("Encryption Logic PASS")

def test_db_storage():
    print("\nTesting DB Storage...")
    db = SessionLocal()
    
    # Create config
    test_key = "sk-db-test-key"
    config = LLMConfiguration(
        provider="openai",
        model_name="gpt-4",
        api_key_encrypted=encrypt_string(test_key),
        is_active=True
    )
    
    # Ensure cleanup
    db.query(LLMConfiguration).filter(LLMConfiguration.provider == "openai").delete()
    
    db.add(config)
    db.commit()
    db.refresh(config)
    
    print(f"Saved Config ID: {config.id}")
    print(f"Stored Encrypted: {config.api_key_encrypted}")
    
    # Retrieve
    retrieved = db.query(LLMConfiguration).filter(LLMConfiguration.id == config.id).first()
    decrypted_key = decrypt_string(retrieved.api_key_encrypted)
    
    assert decrypted_key == test_key
    print(f"Retrieved & Decrypted: {decrypted_key}")
    print("DB Storage PASS")
    
    # Cleanup
    db.delete(retrieved)
    db.commit()
    db.close()

if __name__ == "__main__":
    try:
        test_encryption_logic()
        test_db_storage()
        print("\nALL TESTS PASSED")
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        import traceback
        traceback.print_exc()
