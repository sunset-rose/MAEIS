import os
import numpy as np
import extract_feats.opensmile as of
import extract_feats.librosa as lf
import models
import utils

import os
os.environ['XLA_FLAGS'] = '--xla_gpu_cuda_data_dir=C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2'
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices=false'

def predict(config, audio_path: str, model) -> None:
    """
    预测音频情感

    Args:
        config: 配置项
        audio_path (str): 要预测的音频路径
        model: 加载的模型
    """

    # utils.play_audio(audio_path)

    if config.feature_method == 'o':
        # 一个玄学 bug 的暂时性解决方案
        of.get_data(config, audio_path, train=False)
        test_feature = of.load_feature(config, train=False)
    elif config.feature_method == 'l':
        test_feature = lf.get_data(config, audio_path, train=False)

    # 识别的情绪id
    result = model.predict(test_feature)
    result_id = int(result)
    return result_id
    # result_prob = model.predict_proba(test_feature)
    # print('Recogntion: ', config.class_labels[int(result)])
    # print('Probability: ', result_prob)
    # utils.radar(result_prob, config.class_labels)


if __name__ == '__main__':

    audio_path = '204-sad-wangzhe.wav'

    config = utils.parse_opt()
    model = models.load(config)
    predict(config, audio_path, model)