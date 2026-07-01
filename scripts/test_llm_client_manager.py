"""
Unit tests for LLMClientManager.

This script contains asynchronous unit tests for the LLMClientManager class
located in app.llm.client. It verifies the expected behavior for initialization,
status changes, shutdown, and proper error handling when accessing clients
before initialization.
"""

import sys
import os

# Add the parent directory (where 'app' resides) to the Python path
# This allows importing from the 'app' package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.llm.client import LLMClientManager, ClientStatus


async def run_tests():
    """
    Executes all defined unit tests for LLMClientManager.
    """
    print("--- Running LLMClientManager Tests ---")

    # Test 1: Initialization
    print("\nTest 1: Initialization")
    manager = LLMClientManager()
    assert manager.status == ClientStatus.CREATED, f"Expected status {ClientStatus.CREATED}, got {manager.status}"
    print("PASSED: Manager initialized with status CREATED")

    # Test 2: Initialize
    print("\nTest 2: Initialize")
    await manager.initialize()
    assert manager.status == ClientStatus.INITIALIZED, f"Expected status {ClientStatus.INITIALIZED}, got {manager.status}"
    print("PASSED: Manager status changed to INITIALIZED after initialize()")

    # Test 3: Shutdown
    print("\nTest 3: Shutdown")
    await manager.shutdown()
    assert manager.status == ClientStatus.CLOSED, f"Expected status {ClientStatus.CLOSED}, got {manager.status}"
    print("PASSED: Manager status changed to CLOSED after shutdown()")

    # Create a new manager instance for the next test
    print("\n--- Preparing for Test 4 (Uninitialized Access) ---")
    manager_for_uninit_test = LLMClientManager()
    assert manager_for_uninit_test.status == ClientStatus.CREATED, f"Expected status {ClientStatus.CREATED}, got {manager_for_uninit_test.status}"

    # Test 4: Accessing client before initialization should raise RuntimeError
    print("\nTest 4: Uninitialized Access (get_client)")
    try:
        await manager_for_uninit_test.get_client("some_provider") # Pass any provider name, it shouldn't matter
        # If we reach this line, the assertion failed because no exception was raised
        assert False, "Expected RuntimeError but no exception was raised by get_client() before initialization"
    except RuntimeError as e:
        assert str(e) == "ClientManager not initialized.", f"Expected specific RuntimeError message, got: {e}"
        print("PASSED: RuntimeError raised correctly when calling get_client() before initialization")
    except Exception as e:
        # If a different type of exception was raised, the test also fails
        assert False, f"Expected RuntimeError, but got {type(e).__name__}: {e}"

    print("\n--- All Tests Passed! ---")


if __name__ == "__main__":
    import asyncio
    # Run the async tests using asyncio.run
    asyncio.run(run_tests())