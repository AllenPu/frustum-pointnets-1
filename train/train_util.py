# -*- coding: utf-8 -*-

''' Util functions for training and evaluation.

Author: Charles R. Qi
Date: September 2017
'''

import numpy as np


# 准备一个batch的数据
# 输入dataset,索引,点数,通道数
# 输出数据和标签
def get_batch(dataset, idxs, start_idx, end_idx, num_point, num_channel, from_rgb_detection=False):
    ''' Prepare batch data for training/evaluation.
    batch size is determined by start_idx-end_idx

    Input:
        dataset: an instance of FrustumDataset class
        idxs: a list of data element indices
        start_idx: int scalar, start position in idxs
        end_idx: int scalar, end position in idxs
        num_point: int scalar
        num_channel: int scalar
        from_rgb_detection: bool
    Output:
        batched data and label
    '''
    if from_rgb_detection:
        return get_batch_from_rgb_detection(dataset, idxs, start_idx, end_idx, num_point, num_channel)

    bsize = end_idx-start_idx   # batchsize
    batch_data = np.zeros((bsize, num_point, num_channel))      # 数据(B,N,C)
    batch_label = np.zeros((bsize, num_point), dtype=np.int32)  # 标签(B,N)
    batch_center = np.zeros((bsize, 3))                         # 中心(B,3)
    batch_heading_class = np.zeros((bsize,), dtype=np.int32)    # 朝向角类别(B,)
    batch_heading_residual = np.zeros((bsize,))                 # 朝向角残差(B,)
    batch_size_class = np.zeros((bsize,), dtype=np.int32)       # 尺寸类别(B,)
    batch_size_residual = np.zeros((bsize, 3))                  # 尺寸残差(B,3)
    batch_rot_angle = np.zeros((bsize,))                        # 旋转角(B,)
    if dataset.one_hot:
        batch_one_hot_vec = np.zeros((bsize, 3))    # 类别独热编码向量(B,3)
    for i in range(bsize):
        if dataset.one_hot:
            ps, seg, center, hclass, hres, sclass, sres, rotangle, onehotvec = dataset[idxs[i+start_idx]]
            batch_one_hot_vec[i] = onehotvec
        else:
            ps, seg, center, hclass, hres, sclass, sres, rotangle = dataset[idxs[i+start_idx]]
        batch_data[i, ...] = ps[:, 0:num_channel]
        batch_label[i, :] = seg
        batch_center[i, :] = center
        batch_heading_class[i] = hclass
        batch_heading_residual[i] = hres
        batch_size_class[i] = sclass
        batch_size_residual[i] = sres
        batch_rot_angle[i] = rotangle
    if dataset.one_hot:
        return batch_data, batch_label, batch_center, \
            batch_heading_class, batch_heading_residual, \
            batch_size_class, batch_size_residual, \
            batch_rot_angle, batch_one_hot_vec
    else:
        return batch_data, batch_label, batch_center, \
            batch_heading_class, batch_heading_residual, \
            batch_size_class, batch_size_residual, batch_rot_angle


# 从RGB检测器获得一个batch的数据
def get_batch_from_rgb_detection(dataset, idxs, start_idx, end_idx,
                                 num_point, num_channel):
    bsize = end_idx-start_idx
    batch_data = np.zeros((bsize, num_point, num_channel))
    batch_rot_angle = np.zeros((bsize,))
    batch_prob = np.zeros((bsize,))
    if dataset.one_hot:
        batch_one_hot_vec = np.zeros((bsize, 3))    # for car,ped,cyc
    for i in range(bsize):
        if dataset.one_hot:
            ps, rotangle, prob, onehotvec = dataset[idxs[i+start_idx]]
            batch_one_hot_vec[i] = onehotvec
        else:
            ps, rotangle, prob = dataset[idxs[i+start_idx]]
        batch_data[i, ...] = ps[:, 0:num_channel]
        batch_rot_angle[i] = rotangle
        batch_prob[i] = prob
    if dataset.one_hot:
        return batch_data, batch_rot_angle, batch_prob, batch_one_hot_vec
    else:
        return batch_data, batch_rot_angle, batch_prob


