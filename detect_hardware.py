"""
Hardware Detection Script for Google Colab
Detects CPU, RAM, GPU, and VRAM information
"""

import psutil
import os

def detect_hardware():
    """Detect and print hardware information."""
    
    # === CPU Info ===
    print("=" * 50)
    print("CPU INFO")
    print("=" * 50)
    cpu_count = os.cpu_count()
    print(f"CPU Cores: {cpu_count}")
    
    # === RAM Info ===
    print("\n" + "=" * 50)
    print("RAM INFO")
    print("=" * 50)
    ram = psutil.virtual_memory()
    print(f"Total RAM: {ram.total / (1024**3):.1f} GB")
    print(f"Available RAM: {ram.available / (1024**3):.1f} GB")
    print(f"Used RAM: {ram.used / (1024**3):.1f} GB ({ram.percent}%)")
    
    # === GPU Info ===
    print("\n" + "=" * 50)
    print("GPU INFO")
    print("=" * 50)
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_props = torch.cuda.get_device_properties(0)
            vram_total = gpu_props.total_memory / (1024**3)
            vram_allocated = torch.cuda.memory_allocated(0) / (1024**3)
            vram_reserved = torch.cuda.memory_reserved(0) / (1024**3)
            vram_free = vram_total - vram_reserved
            
            print(f"GPU: {gpu_name}")
            print(f"VRAM Total: {vram_total:.1f} GB")
            print(f"VRAM Allocated: {vram_allocated:.1f} GB")
            print(f"VRAM Reserved: {vram_reserved:.1f} GB")
            print(f"VRAM Free: {vram_free:.1f} GB")
        else:
            print("No GPU available")
    except ImportError:
        print("PyTorch not installed - cannot detect GPU")


if __name__ == "__main__":
    detect_hardware()
