"""
IR package – permite `from CompilerLogic.ir import IRGenerator`
Cross-platform compatible initialization
"""

# Try to import IRGenerator with fallback
try:
    from .irBuilder import IRGenerator
    IR_AVAILABLE = True
except ImportError as e:
    # Create a dummy class if irBuilder is not available
    class IRGenerator:
        def __init__(self, *args, **kwargs):
            raise ImportError(f"IRGenerator not available: {e}")
        
        def generate(self):
            raise ImportError("IRGenerator not available")
    
    IR_AVAILABLE = False
    print(f"Warning: IRGenerator not available: {e}")

# Export for external use
__all__ = ['IRGenerator', 'IR_AVAILABLE']

# Version info
__version__ = "1.0.0"
__author__ = "VGraph Compiler Team"