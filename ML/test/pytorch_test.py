import subprocess
import sys

def check_available_pytorch_versions():
    """检查可用的PyTorch版本"""
    print("检查PyTorch CUDA版本...")
    
    # 测试不同的索引URL
    cuda_versions = {
        "cu118": "https://download.pytorch.org/whl/cu118",
        "cu121": "https://download.pytorch.org/whl/cu121", 
        "cpu": "https://download.pytorch.org/whl/cpu"
    }
    
    for cuda_type, index_url in cuda_versions.items():
        print(f"\n检查 {cuda_type} 版本:")
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "index", "versions", "torch", 
                "--index-url", index_url
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # 提取版本信息
                for line in result.stdout.split('\n'):
                    if 'Available versions:' in line or 'torch' in line.lower():
                        print(f"  {line.strip()}")
            else:
                print(f"  无法获取 {cuda_type} 版本信息")
                
        except Exception as e:
            print(f"  检查失败: {e}")

check_available_pytorch_versions()