import os
import sys

try:
    import nvidia.cublas
    print(f"nvidia.cublas path: {nvidia.cublas.__path__}")
    cublas_bin = os.path.join(list(nvidia.cublas.__path__)[0], 'bin')
    print(f"cublas bin: {cublas_bin}, exists: {os.path.exists(cublas_bin)}")

    import nvidia.cudnn
    print(f"nvidia.cudnn path: {nvidia.cudnn.__path__}")
    cudnn_bin = os.path.join(list(nvidia.cudnn.__path__)[0], 'bin')
    print(f"cudnn bin: {cudnn_bin}, exists: {os.path.exists(cudnn_bin)}")

except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
