import time

import tensorrt as trt
import torch
import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np
from skimage import io
from skimage.transform import resize
from torchvision.transforms import Normalize


print(trt.__version__)
# trtexec --onnx=resnet50_pytorch.onnx --saveEngine=resnet_engine_pytorch_fp16.trt --explicitBatch --inputIOFormats=fp16:chw --outputIOFormats=fp16:chw --fp16
# trtexec --onnx=resnet50_pytorch.onnx --saveEngine=resnet_engine_pytorch.trt --explicitBatch

BATCH_SIZE = 32
USE_FP16 = True
target_dtype = np.float16 if USE_FP16 else np.float32


def preprocess_image(img):
    norm = Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    result = norm(torch.from_numpy(img).transpose(0, 2).transpose(1, 2))
    return np.array(result, dtype=target_dtype)


def load_egine():
    if USE_FP16:
        engine_path = "/home/hzsun/python_dev/lm-filter/src/tensorrt_demo/resnet_engine_pytorch_fp16.trt"
    else:
        engine_path = "/home/hzsun/python_dev/lm-filter/src/tensorrt_demo/resnet_engine_pytorch.trt"

    print(f"load model={engine_path}")
    with open(engine_path, "rb") as f:
        engine_data = f.read()
        logger = trt.Logger(trt.Logger.WARNING)
        runtime = trt.Runtime(logger)
        engine = runtime.deserialize_cuda_engine(engine_data)
    return engine


def get_batch_imgs():
    url = 'https://images.dog.ceo/breeds/retriever-golden/n02099601_3004.jpg'
    img = io.imread(url)
    print(f"img_1.shape={img.shape}")
    img = resize(img, (224, 224))
    print(f"img_2.shape={img.shape}")
    img = np.array(img, dtype=target_dtype)
    print(f"img_3.shape={img.shape}")
    img = np.expand_dims(img, axis=0)
    print(f"img_4.shape={img.shape}")
    img = np.repeat(img, BATCH_SIZE, axis=0)
    print(f"img_5.shape={img.shape}")
    input_batch = np.array(img, dtype=target_dtype)
    print(f"img_6.shape={img.shape}")
    return input_batch


def allocate_buffers(input_batch, output):
    # need to set input and output precisions to FP16 to fully enable it
    # allocate device memory
    d_input = cuda.mem_alloc(1 * input_batch.nbytes)
    d_output = cuda.mem_alloc(1 * output.nbytes)

    bindings = [int(d_input), int(d_output)]
    return d_input, d_output, bindings


def predict(d_input, d_output, bindings, output, preprocessed_images):
    stream = cuda.Stream()
    cuda.memcpy_htod_async(d_input, preprocessed_images, stream)

    print(f"Warming up...")
    # pred = predict(preprocessed_images, d_input, output, d_output, stream)
    # execute model
    context.execute_async_v2(bindings, stream.handle, None)
    # transfer predictions back
    cuda.memcpy_dtoh_async(output, d_output, stream)
    # syncronize threads
    stream.synchronize()
    return output


if __name__ == "__main__":
    engine = load_egine()
    input_batch = get_batch_imgs()
    output = np.empty([BATCH_SIZE, 1000], dtype=target_dtype)
    print(f"input_batch.shape={input_batch.shape},nbytes={input_batch.nbytes}")
    preprocessed_images = np.array([preprocess_image(image) for image in input_batch])
    print(f"preprocessed_images.shape={preprocessed_images.shape}")

    context = engine.create_execution_context()

    d_input, d_output, bindings = allocate_buffers(input_batch, output)

    # transfer input data to device
    start_time = time.time()
    pred = predict(d_input, d_output, bindings, output, preprocessed_images)

    indices = (-pred[0]).argsort()[:5]
    ret = list(zip(indices, output[0][indices]))
    print(f"Done warming up!,time={(time.time() - start_time) * 1000},ret={ret}")
