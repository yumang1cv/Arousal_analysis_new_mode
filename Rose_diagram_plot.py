import itertools
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import numpy as np


def main():
    # plt.rcParams["font.family"] = "Times New Roman"  #全局字体
    fig = plt.figure(dpi=300, figsize=(4, 3))  # 分辨率参数-dpi，画布大小参数-figsize
    ax = fig.add_subplot(111, projection='polar')  # 111的意思是，把区域分成1*1份，图像在第1区间、和subplot(1,1,1)一样
    ax.set_theta_offset(np.pi / 2)  # 设置起始角度为90度
    ax.set_theta_direction(-1)  # 设置顺时针旋转。逆时针是direction=1
    ax.set_rlabel_position(0)  # 设置Y轴的标签位置为起始角度位置
    ax.set_xticks(np.arange(0, 2.0 * np.pi, np.pi / 4.0))  # 设置半径方向轴（y轴）的间距
    minor_ticks = np.arange(0, 2.0 * np.pi, np.pi / 12.0)  # 设置副刻度线，间隔为pi/8
    ax.set_xticks(minor_ticks, minor=True)  # 设置副刻度线
    ax.grid(which="minor", alpha=0.5)  # 设置副刻度线条，线宽为0.5
    # ax.grid(which='minor', axis="x", linestyle=':', linewidth='0.5', color='black')
    '''
    x为玫瑰图每一瓣区域角度的设置
    y为玫瑰图每一瓣区域半径，这里是number
    z为用颜色表示的量，这里是mean contact force
    '''
    x = np.radians(np.arange(0, 360, 20))  # theta, Convert a degree array to radians
    y = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3, 2])  # radii
    z = np.array([0.12, 0.11, 0.18, 0.15, 0.14, 0.19, 0.17, 0.19, 0.2, 0.18, 0.115, 0.15, 0.17, 0.1, 0.135, 0.14, 0.17,
                  0.12])  # colar
    cmap = plt.get_cmap('cool')  # color of bar,彩虹色为jet,如果要分n段，get_cmap('cool',n)
    coll = colored_bar(x, y, z, ax=ax, width=np.radians(10), cmap=cmap)  # width为10 degree
    cbar = fig.colorbar(coll, shrink=1, pad=0.12)  # 添加颜色条, shrink为颜色条的大小倍率,pad为间隔
    cbar.set_label("Mean contact force (N)", fontsize=10, labelpad=10)  # 设置颜色条的标签和字体大小和以及和图的间距
    # cbar.set_ticks([0.1, 0.12, 0.14, 0.16, 0.18, 0.2])             #设置颜色条的刻度
    cbar.ax.tick_params(labelsize=8)  # 颜色条刻度的字体大小
    plt.xlim([0, 2 * np.pi])  # 设置极坐标圆周角度,这里为360度
    plt.xticks(fontsize=10)  # 改变圆周文字大小参数-fontsize
    plt.yticks(fontsize=10)  # 改变半径方向文字大小参数-fontsize
    plt.ylim([0, 10])  # 设置半径大小
    ax.set_yticks([0, 2.5, 5, 7.5, 10])  # axis scale 半径方向刻度
    ax.set_ylabel('number', fontsize=10)  # 设置y轴标签
    ax.yaxis.set_label_coords(0.45, 0.76)  # 设置y轴标签的坐标
    # ax.set_rlabel_position(0)   # 半径（y轴）标签旋转 (度数法)
    plt.show()


def colored_bar(left, height, z=None, width=np.radians(10), bottom=0, ax=None, **kwargs):
    if ax is None:
        ax = plt.gca()  # If the current axes doesn't exist, or isn't a polar one, the appropriate axes will be created and then returned.
    width = itertools.cycle(np.atleast_1d(width))
    bottom = itertools.cycle(np.atleast_1d(bottom))
    rects = []
    for x, y, h, w in zip(left, bottom, height, width):
        rects.append(Rectangle((x, y), w, h))
    coll = PatchCollection(rects, array=z, **kwargs)
    ax.add_collection(coll)
    ax.autoscale()
    return coll


if __name__ == '__main__':
    main()
