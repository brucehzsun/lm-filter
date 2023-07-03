import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np
import torch

device_id = 0

def normalize_keypoints(kpts, image_shape):
    """ Normalize keypoints locations based on image image_shape"""
    height, width = image_shape[0][1], image_shape[0][0]
    one = kpts.new_tensor(1)
    size = torch.stack([one * width, one * height])[None]
    center = size / 2
    scaling = size.max(1, keepdim=True).values * 0.7
    return (kpts - center[:, None, :]) / scaling[:, None, :]

# 加载Engine文件
def load_engine(engine_path):
    print(f"engine_path={engine_path},tensort_version={trt.__version__}")
    with open(engine_path, "rb") as f:
        engine_data = f.read()
    runtime = trt.Runtime(trt.Logger(trt.Logger.WARNING))
    engine = runtime.deserialize_cuda_engine(engine_data)
    if engine is None:
        raise RuntimeError("Failed to load engine file!")
    return engine


def tensorrt_test_gpu(input_data, engine_path):
    kpts0 = input_data['keypoints0']
    scores0 = input_data['scores0'].numpy()
    desc0 = input_data['descriptors0'].numpy()
    image_size0 = input_data['image_size0'].numpy()

    kpts1 = input_data['keypoints1']
    scores1 = input_data['scores1'].numpy()
    desc1 = input_data['descriptors1'].numpy()
    image_size1 = input_data['image_size1'].numpy()

    # 处理关键点和描述子等输入数据
    kpts0 = normalize_keypoints(kpts0, image_size0).numpy()
    kpts1 = normalize_keypoints(kpts1, image_size1).numpy()

    # 将输入数据存储在 Python 字典中
    inputs = {
        'keypoints0': kpts0,
        'scores0': scores0,
        'descriptors0': desc0,
        'keypoints1': kpts1,
        'scores1': scores1,
        'descriptors1': desc1
    }

    # 加载Engine文件
    engine = load_engine(engine_path)

    # Allocate host and device buffers
    input_names = ['keypoints0', 'scores0', 'descriptors0', 'keypoints1', 'scores1', 'descriptors1']
    output_names = ['scores']

    inputs_trt = []
    outputs_trt = []
    bindings = []
    for i, name in enumerate(input_names):
        # shape = (1,) + inputs[name].shape[1:]
        input_trt = np.ascontiguousarray(inputs[name]).astype(np.float32)
        inputs_trt.append(input_trt)
        bindings.append(int(input_trt.ctypes.data))

        # # Set the binding shape of the corresponding input tensor
        # engine_input_idx = engine.get_binding_index(name)
        # engine_input_shape = tuple(engine.get_binding_shape(engine_input_idx))
        # if engine_input_shape != shape:
        #     engine.set_binding_shape(engine_input_idx, shape)

    for i, name in enumerate(output_names):
        shape = (1,) + tuple(engine.get_binding_shape(i + len(input_names)))
        dtype = trt.DataType.FLOAT
        output_trt = np.empty(shape, dtype=np.float32)
        outputs_trt.append(output_trt)
        bindings.append(int(output_trt.ctypes.data))
        print(f"output_shape{i}={tuple(shape[1:])}")

    # Create CUDA stream for TensorRT execution
    stream = cuda.Stream()

    # Execute TensorRT inference
    cuda_ctx = cuda.Device(0).make_context()
    # cuda_ctx.execute_async_v2(bindings=bindings,stream_handle=stream.handle)
    cuda_ctx.execute_v2(bindings=bindings)

    # Synchronize CUDA stream to wait for inference to complete
    stream.synchronize()

    # Copy results from device to host memory
    scores_np = outputs_trt[0]
    print(f"socre={scores_np}")

    return scores_np


if __name__ == "__main__":
    # Set device to use
    device = "cpu"
    engine_path = '/home/hzsun/python_dev/model_deploy/c04_tensorrt/model.trt'
    input_data = torch.load('/home/hzsun/python_dev/model_deploy/c04_tensorrt/data.pt')
    input_data = {k: v.to(device) for k, v in input_data.items()}
    tensorrt_test_gpu(input_data, engine_path)