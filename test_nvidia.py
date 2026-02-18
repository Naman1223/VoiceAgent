import os
import sys

try:
    import nvidia.cublas
    print(f"nvidia.cublas found at {nvidia.cublas.__file__}")
    cublas_bin = os.path.join(os.path.dirname(nvidia.cublas.__file__), 'bin')
    print(f"cublas bin: {cublas_bin}, exists: {os.path.exists(cublas_bin)}")

    import nvidia.cudnn
    print(f"nvidia.cudnn found at {nvidia.cudnn.__file__}")
    cudnn_bin = os.path.join(os.path.dirname(nvidia.cudnn.__file__), 'bin')
    print(f"cudnn bin: {cudnn_bin}, exists: {os.path.exists(cudnn_bin)}")

except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
