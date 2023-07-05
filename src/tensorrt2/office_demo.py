import time

import tensorrt as trt
import numpy as np
import os
import pycuda.driver as cuda
import pycuda.autoinit
from src.onnx_helper import ONNXClassifierWrapper

print("TensorRT version: {}".format(trt.__version__))

BATCH_SIZE = 32
dummy_input_batch = np.zeros((BATCH_SIZE, 224, 224, 3), dtype=np.float32)

model_path = "/home/hzsun/python_dev/lm-filter/src/tensorrt2/resnet50-v1-12/resnet_engine_intro.trt"
trt_model = ONNXClassifierWrapper(model_path, [BATCH_SIZE, 1000], target_dtype=np.float32)
start_time = time.time()
ret = trt_model.predict(dummy_input_batch)
print(f"time={(time.time() - start_time) * 1000}")
print(ret[0][:10])
