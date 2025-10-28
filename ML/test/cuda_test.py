import torch
import subprocess
import os
import sys

def comprehensive_diagnosis():
    print("=" * 50)
    print("CUDA 环境完整诊断")
    print("=" * 50)
    
    # 1. 检查 PyTorch
    print("\n1. PyTorch 信息:")
    print(f"   PyTorch 版本: {torch.__version__}")
    print(f"   CUDA 可用: {torch.cuda.is_available()}")
    print(f"   CUDA 版本: {getattr(torch.version, 'cuda', 'None')}")
    
    # 2. 检查 GPU
    print("\n2. GPU 信息:")
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("   ✓ nvidia-smi 执行成功")
            # 提取关键信息
            for line in result.stdout.split('\n'):
                if 'CUDA Version' in line:
                    print(f"   {line.strip()}")
                if 'Driver Version' in line:
                    print(f"   {line.strip()}")
        else:
            print("   ✗ nvidia-smi 执行失败")
    except Exception as e:
        print(f"   ✗ nvidia-smi 错误: {e}")
    
    # 3. 检查环境变量
    print("\n3. 环境变量检查:")
    cuda_path = os.environ.get('CUDA_PATH', '未设置')
    print(f"   CUDA_PATH: {cuda_path}")
    
    path_entries = [p for p in os.environ.get('PATH', '').split(';') if 'CUDA' in p.upper()]
    if path_entries:
        print("   PATH 中的 CUDA 路径:")
        for path in path_entries:
            print(f"     - {path}")
    else:
        print("   ✗ PATH 中未找到 CUDA 路径")
    
    # 4. 检查 nvcc
    print("\n4. nvcc 编译器检查:")
    try:
        nvcc_result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True)
        if nvcc_result.returncode == 0:
            print("   ✓ nvcc 可用")
            print(f"   版本: {nvcc_result.stdout.split('release')[-1].split(',')[0].strip()}")
        else:
            print("   ✗ nvcc 不可用")
    except Exception as e:
        print(f"   ✗ nvcc 错误: {e}")
    
    # 5. 检查 CUDA 安装目录
    print("\n5. CUDA 安装目录检查:")
    possible_paths = [
        r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA",
        r"D:\Program Files\NVIDIA GPU Computing Toolkit\CUDA", 
        r"D:\CUDA",
        os.environ.get('CUDA_PATH', '')
    ]
    
    for path in possible_paths:
        if path and os.path.exists(path):
            print(f"   ✓ 找到 CUDA 目录: {path}")
            # 列出子目录（版本）
            try:
                subdirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
                print(f"     版本: {subdirs}")
            except:
                pass


def check_version_compatibility():
    print("\n" + "="*50)
    print("版本兼容性检查")
    print("="*50)
    
    # 获取 nvidia-smi 中的 CUDA 版本
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'CUDA Version' in line:
                cuda_version_smi = line.split('CUDA Version:')[-1].strip().split(' ')[0]
                print(f"nvidia-smi 报告的 CUDA 版本: {cuda_version_smi}")
    except:
        pass
    
    # 检查当前 PyTorch 的 CUDA 支持
    print(f"PyTorch 编译的 CUDA 版本: {getattr(torch.version, 'cuda', 'None')}")
    
    # 常见版本兼容性
    compatibility = {
        '11.7': ['11.7', '11.8'],
        '11.8': ['11.7', '11.8', '12.0'],
        '12.1': ['12.1', '12.0']
    }
    
    print("\n建议: 确保 PyTorch 的 CUDA 版本与系统安装的 CUDA 版本匹配")


comprehensive_diagnosis()
check_version_compatibility()
