import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
import numpy as np
import torch
import time


def normalize_keypoints(kpts, image_shape):
    """ Normalize keypoints locations based on image image_shape"""
    height, width = image_shape[0][1], image_shape[0][0]
    one = kpts.new_tensor(1)
    size = torch.stack([one * width, one * height])[None]
    center = size / 2
    scaling = size.max(1, keepdim=True).values * 0.7
    return (kpts - center[:, None, :]) / scaling[:, None, :]


def load_engine(trt_logger, engine_file_path):
    with open(engine_file_path, 'rb') as f:
        engine_data = f.read()
    runtime = trt.Runtime(trt_logger)
    return runtime.deserialize_cuda_engine(engine_data)


# 创建ExecutionContext
def create_execution_context(engine):
    return engine.create_execution_context()


def allocate_buffers(engine):
    inputs = []
    outputs = []
    bindings = []

    for binding in engine:
        binding_idx = engine.get_binding_index(binding)
        shape = context.get_binding_shape(binding_idx)
        size = trt.volume(shape)
        dtype = engine.get_binding_dtype(binding)
        dtype = trt.nptype(dtype)
        print(f"{binding},size={size},dtype={dtype},shape={shape},bytes={dtype.itemsize}")
        if engine.binding_is_input(binding):
            input_buffer = cuda.pagelocked_empty(size, dtype)
            input_memory = cuda.mem_alloc(input_buffer.nbytes)
            inputs.append(input_memory)
            bindings.append(int(input_memory))
        else:
            output_buffer = cuda.pagelocked_empty(size, dtype)
            output_memory = cuda.mem_alloc(output_buffer.nbytes)
            outputs.append(output_memory)
            bindings.append(int(output_memory))
    return inputs, outputs, bindings


# def infer(engine, context, input_path):
def preprocess_input_data(input_path: str):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    data = torch.load(input_path)
    data = {k: v.to(device) for k, v in data.items()}
    for key in data:
        print(f"data.key={key},value.shape={data[key].shape}")

    # for key in data:
    #     value = data[key]
    #     print(f"key={key},input_data.type={type(value)},input_data.shape={value.shape}")

    desc0, desc1 = data['descriptors0'], data['descriptors1']
    kpts0, kpts1 = data['keypoints0'], data['keypoints1']

    # if kpts0.shape[1] == 0 or kpts1.shape[1] == 0:  # no keypoints
    #     shape0, shape1 = kpts0.shape[:-1], kpts1.shape[:-1]
    #     return {
    #         'matches0': kpts0.new_full(shape0, -1, dtype=torch.int),
    #         'matches1': kpts1.new_full(shape1, -1, dtype=torch.int),
    #         'matching_scores0': kpts0.new_zeros(shape0),
    #         'matching_scores1': kpts1.new_zeros(shape1),
    #     }

    # Keypoint normalization.
    # kpts0 = normalize_keypoints(kpts0, data['image_size0'])
    # kpts1 = normalize_keypoints(kpts1, data['image_size1'])

    # Keypoint MLP encoder.
    # desc0 = desc0 + self.kenc(kpts0, data['scores0'])
    # desc1 = desc1 + self.kenc(kpts1, data['scores1'])

    # Input binding for descriptors0 with dimensions 8x256x1025 is created.
    # Input binding for descriptors1 with dimensions 8x256x1030 is created.
    # print(f"desc0={desc0.shape}")
    # print(f"desc1={desc1.shape}")
    return desc0, desc1


def infer(input_path, engine):
    # 将图片进行预处理
    input_desc0, input_desc1 = preprocess_input_data(input_path)

    start_time = time.time()

    # 分配输入和输出显存
    inputs, outputs, bindings = allocate_buffers(engine)

    stream = cuda.Stream()
    # 将输入数据拷贝到显存中
    # cuda.memcpy_htod(inputs[0], input_data)
    input_desc0 = input_desc0.cpu().numpy()
    input_desc1 = input_desc1.cpu().numpy()
    # memcpy_htod_async, d_input = <# class 'pycuda._driver.DeviceAllocation'>, batch= < class 'numpy.ndarray' >

    cuda.memcpy_htod_async(inputs[0], input_desc0, stream)
    cuda.memcpy_htod_async(inputs[1], input_desc1, stream)
    start_time_core = time.time()
    # Run inference
    context.execute_async_v2(bindings=bindings, stream_handle=stream.handle)
    # Transfer prediction output from the GPU.
    # 8x1026x1031
    scores = np.empty(8 * 1026 * 1031, dtype=np.float32)  # Need to set both input and output precisions to FP16 to fully enable FP16
    print(f"ouput,output_datas[0]={type(scores)},d_output={type(outputs[0])}")
    # ouput,output_datas[0]=<class 'pycuda._driver.DeviceAllocation'>,d_output=<class 'pycuda._driver.DeviceAllocation'>
    cuda.memcpy_dtoh_async(scores, outputs[0], stream)
    # Synchronize the stream
    stream.synchronize()
    print(f"output_type={type(scores)},shape={scores.shape},core_time+{(time.time() - start_time) * 1000}")
    print(f"inference_success,time={(time.time() - start_time) * 1000}")
    return scores


if __name__ == '__main__':
    # 加载TensorRT引擎
    logger = trt.Logger(trt.Logger.WARNING)
    engine = load_engine(logger, 'superglue_outdoor.trt')

    # 创建ExecutionContext
    context = create_execution_context(engine)

    # 对单张图片进行推理
    input_data = 'data.pt'
    for i in range(2):
        scores = infer(input_data, engine)
        # print("==========finish===========")
