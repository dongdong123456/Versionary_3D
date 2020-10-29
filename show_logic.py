# -*- coding: utf-8 -*-
# Created by WIN10 on 2020/10/9
# Copyright (c) 2020 WIN10. All rights reserved.
from resource.show_ui import Ui_Show
from camera.camera_utils import Camera_Utils
from PyQt5.QtWidgets import QFileDialog
from mrcnn.config import Config
import mrcnn.model as modellib
import mrcnn.visualize as visualize
import cv2
from imutils import perspective
import numpy as np
from scipy import signal  # 滤波等
from scipy.spatial import distance as dist
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QMainWindow
from PyQt5.Qt import QImage
from PyQt5 import QtCore, QtWidgets, QtGui


class BalloonConfig(Config):
    NAME = "coco"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + balloon

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 200

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9
    IMAGE_MIN_DIM = 512
    IMAGE_MAX_DIM = 640

# 继承QThread
class Runthread(QtCore.QThread):
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)

    def __init__(self, frameData):
        super(Runthread, self).__init__()
        self.frameData = frameData
        # 模型初始化
        config = BalloonConfig()
        self.model = model.MaskRCNN(mode="inference", model_dir='', config=config)
        self.class_names = ['BG', 'box']

    # 模型页触发模型加载
    def model_weight_load(self, model_path):
        self.model.load_weights(model_path, by_name=True)
        msg = '%s模型加载\n' % model_path
        return msg

    # 目标检测
    def detectron(self, image, distanceData, numRows, numCols, img_bgr):
        results = self.model.detect([image], verbose=1)
        r = results[0]

        counters = visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'],
                                               self.class_names, r['scores'], show_mask=False)
        boxcount = 0
        box_list = []
        # 如果没有箱子发送
        if counters.size == 0:
            send_message = '0,0,0,0,0,0\n'
            return send_message
        for cnt in counters:
            cnt1 = cnt.astype('int32')
            if cnt.size < 50:
                continue
            rect = cv2.minAreaRect(cnt1)  # 中心点、长宽、偏转角
            box = cv2.boxPoints(rect)  # 获取最小外接矩形的4个顶点坐标(ps: cv2.boxPoints(rect) for OpenCV 3.x)
            box = np.int0(box)
            # 顺时针排序
            box = perspective.order_points(box)
            # 左上、右上、右下、左下
            (tl, tr, br, bl) = box
            # 图像轮廓及中心点坐标
            M = cv2.moments(cnt1)  # 计算第一条轮廓的各阶矩,字典形式
            center_x = int(M['m10'] / M['m00'])
            center_y = int(M['m01'] / M['m00'])

            Z_map = np.array(distanceData).reshape(numRows, numCols, 1).astype(np.uint16)

            # 计算箱子的高度
            width = int(rect[1][0])
            height = int(rect[1][1])
            angle = rect[2]
            # print(angle)
            if width < height:  # 计算角度，为后续做准备
                angle = angle - 90

            src_pts = cv2.boxPoints(rect)
            dst_pts = np.array([[0, height],
                                [0, 0],
                                [width, 0],
                                [width, height]], dtype="float32")

            M = cv2.getPerspectiveTransform(src_pts, dst_pts)

            warped = cv2.warpPerspective(Z_map, M, (width, height))

            scal = 1600
            hist = cv2.calcHist([warped], [0], None, [scal], [250, 1850])

            # 使用极值法求取Z的高度值
            s_arry = hist[:, 0]
            num_peak_3 = signal.find_peaks(s_arry, height=100, distance=10)  # distance表极大值点的距离至少大于等于10个水平单位

            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)

            z_value = 1900 - (maxLoc[1] + 250)
            if len(num_peak_3[0]) == 0:
                z_value_max = z_value
            else:
                z_value_max = 1900 - (num_peak_3[0][0] + 250)

                # 箱子中心点
            x_w, y_w, z_w = self.cam2word(self.frameData.cameraParams, center_x, center_y, z_value, 1900, distanceData)
            # tltr

            x_w_tltr, y_w_tltr, z_w_tltr = self.cam2word(self.frameData.cameraParams, tl[0], tl[1], z_value, 1900,
                                                         distanceData)

            # blbr
            x_w_blbr, y_w_blbr, z_w_blbr = self.cam2word(self.frameData.cameraParams, tr[0], tr[1], z_value, 1900,
                                                         distanceData)

            # tlbl
            x_w_tlbl, y_w_tlbl, z_w_tlbl = self.cam2word(self.frameData.cameraParams, br[0], br[1], z_value, 1900,
                                                         distanceData)

            # trbr
            x_w_trbr, y_w_trbr, z_w_trbr = self.cam2word(self.frameData.cameraParams, bl[0], bl[1], z_value, 1900,
                                                         distanceData)

            dA = dist.euclidean((x_w_tltr, y_w_tltr), (x_w_blbr, y_w_blbr))
            dB = dist.euclidean((x_w_tlbl, y_w_tlbl), (x_w_trbr, y_w_trbr))
            if dA < dB:
                dA, dB = dB, dA
            angle = 0.0 - angle

            if angle > 90:
                angle = angle - 180
            else:

                angle = angle

            # 箱子结果可视化

            # 画外接矩形框
            cv2.drawContours(img_bgr, [box.astype("int")], 0, (0, 255, 0), 1)

            # 画四个顶点坐标
            for (x, y) in box:
                cv2.circle(img_bgr, (int(x), int(y)), 5, (0, 0, 255), -1)

            cv2.circle(img_bgr, (center_x, center_y), 5, 128, -1)

            str1 = str(boxcount)  # 把坐标转化为字符串
            cv2.putText(img_bgr, str1, (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1,
                        cv2.LINE_AA)  # 绘制坐标点位

            a = np.array([boxcount, dA, dB, z_value, z_value_max, x_w, y_w, z_w, angle])
            box_list.append(a)

            boxcount += 1

        return img_bgr, box_list

    def send_to_roboot(self, box_list):
        # 箱子排序
        send_masage=[]
        box_list = np.array(box_list)
        # 按中心点x排序
        box_list = box_list[np.lexsort([-box_list[:, 5]])]
        # 按中心点y排序
        box_list = box_list[np.lexsort([-box_list[:, 6]])]
        layer_Z = box_list[0][7] + 15
        # 箱子太高
        if layer_Z > 5000:
            send_message = "1,1,1,1,1,1"
            self._signal.emit(send_message)
        else:
            for box_detail in box_list:
                # 进行坐标转换
                P_cam = box_detail[5:8]
                P_rob = self.calculate(P_cam)
                send_message = '001' + ',' + '%.0f' % P_rob[0][0] + ',' + '%.0f' % P_rob[0][1] + ',' + '%.0f' % P_rob[
                    0][2] + ',' + '%.0f' % (box_detail[8]) + ',' + str(len(box_list)) + '\n'
                self._signal.emit(send_message)
                send_masage.append(send_message)
            return send_masage

    # 相机坐标转世界坐标
    def cam2word(self, cameraParams, p_x, p_y, z_value, def_plane, distanceData):

        cx = cameraParams.cx
        fx = cameraParams.fx
        cy = cameraParams.cy
        fy = cameraParams.fy
        m_c2w = cameraParams.cam2worldMatrix
        # 中心点
        # 相机坐标系
        xp = (cx - p_x) / fx
        yp = (cy - p_y) / fy
        if p_y > 510:
            p_y = 510
        zc = distanceData[int(p_y) * 640 + int(p_x)]
        if zc == 0.0:
            zc = def_plane - z_value
        xc = xp * zc
        yc = yp * zc
        # 世界坐标系
        x_w = round(m_c2w[0 * 4 + 3] + zc * m_c2w[0 * 4 + 2] + yc * m_c2w[0 * 4 + 1] + xc * m_c2w[0 * 4 + 0], 0)
        y_w = round(m_c2w[1 * 4 + 3] + zc * m_c2w[1 * 4 + 2] + yc * m_c2w[1 * 4 + 1] + xc * m_c2w[1 * 4 + 0], 0)
        z_w = round(m_c2w[2 * 4 + 3] + zc * m_c2w[2 * 4 + 2] + yc * m_c2w[2 * 4 + 1] + xc * m_c2w[2 * 4 + 0], 0)
        return x_w, y_w, z_w

    # 世界坐标系转机器人
    def calculate(self, P_cam):
        f = open("ret_R.txt", 'rb')
        pickle.load(f)
        f.seek(0)
        ret_R = pickle.load(f, encoding='bytes')
        f1 = open("ret_t.txt", 'rb')
        pickle.load(f1)
        f1.seek(0)
        ret_t = pickle.load(f1, encoding='bytes')
        # Compare the recovered R and t with the original
        tra = np.array(P_cam)
        P_Rob = np.dot(tra, ret_R) + ret_t.T
        # P_Rob = (ret_R * P_cam) + tile(ret_t, (1, n))
        return P_Rob.tolist()
class Show_logic(QMainWindow, Ui_Show):

    def __init__(self):
        super(Show_logic, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.connect()
        self.cu = Camera_Utils()
        self.status = False
        self.path = 'image'
        self.m_green_SheetStyle = "min-width: 16px; min-height: 16px;max-width:16px; max-height: 16px;border-radius: 8px;  border:1px solid black;background:green"
        self.m_red_SheetStyle = "min-width: 16px; min-height: 16px;max-width:16px; max-height: 16px;border-radius: 8px;  border:1px solid black;background:red"

        # 开启新线程
        self.thread = Runthread(self.frameData)
        self.thread._signal.connect(self.call_backlog)  # 进程连接回传到GUI的事件
        self.thread.start()

    def connect(self):
        self.pushButton.clicked.connect(self.comera_link)
        self.pushButton_2.clicked.connect(self.model_path)
        self.pushButton_3.clicked.connect(self.click_save)

    def comera_link(self, status):
        _translate = QtCore.QCoreApplication.translate
        if status == True:
            try:
                self.cu.Comera_link()
                self.label_2.setStyleSheet(self.m_green_SheetStyle)
                self.status = True
                self.pushButton.setText(_translate("Form", "断开相机"))
                msg = '相机已连接\n'
                self.write_msg(msg)
            except Exception as ret:
                msg = '无法连接相机\n'
                self.write_msg(msg)

        else:
            try:
                self.cu.close()
                self.label_2.setStyleSheet(self.m_red_SheetStyle)
                self.status = False
                self.pushButton.setText(_translate("Form", "连接相机"))
                msg = '相机已断开连接\n'
                self.write_msg(msg)
            except Exception as ret:
                msg = '无法连接相机\n'
                self.write_msg(msg)

    def model_path(self):
        fname = QFileDialog.getOpenFileName(self, 'open file', '/')
        if fname[0]:
            try:
                msg = self.thread.model_weight_load(fname[0])
                self.write_msg(msg)
            except:
                QtWidgets.QMessageBox.critical(self, "错误", "打开文件失败，可能是文件内型错误")


    def click_save(self):
        if self.status == True:
            b, distanceData, numRows, numCols, img_bgr, frameData = self.cu.click_save(self.path)
            self.run(b, distanceData, numRows, numCols, img_bgr, frameData)
        else:
            QtWidgets.QMessageBox.critical(self, "错误", "连接相机")

    def run(self, image, distanceData, numRows, numCols, img_bgr, frameData):
        results = self.model.detect([image], verbose=1)
        r = results[0]

        counters = visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'],
                                               self.class_names, r['scores'], show_mask=False)
        boxcount = 0
        box_list = []
        # 如果没有箱子发送
        if counters.size == 0:
            send_message = '0,0,0,0,0,0\n'
            self.send_robot(send_message)
        for cnt in counters:
            cnt1 = cnt.astype('int32')
            if cnt.size < 50:
                continue
            rect = cv2.minAreaRect(cnt1)  # 中心点、长宽、偏转角
            box = cv2.boxPoints(rect)  # 获取最小外接矩形的4个顶点坐标(ps: cv2.boxPoints(rect) for OpenCV 3.x)
            box = np.int0(box)
            # 顺时针排序
            box = perspective.order_points(box)
            # 左上、右上、右下、左下
            (tl, tr, br, bl) = box
            # 图像轮廓及中心点坐标
            M = cv2.moments(cnt1)  # 计算第一条轮廓的各阶矩,字典形式
            center_x = int(M['m10'] / M['m00'])
            center_y = int(M['m01'] / M['m00'])

            Z_map = np.array(distanceData).reshape(numRows, numCols, 1).astype(np.uint16)

            # 计算箱子的高度
            width = int(rect[1][0])
            height = int(rect[1][1])
            angle = rect[2]
            # print(angle)
            if width < height:  # 计算角度，为后续做准备
                angle = angle - 90

            src_pts = cv2.boxPoints(rect)
            dst_pts = np.array([[0, height],
                                [0, 0],
                                [width, 0],
                                [width, height]], dtype="float32")

            M = cv2.getPerspectiveTransform(src_pts, dst_pts)

            warped = cv2.warpPerspective(Z_map, M, (width, height))

            scal = 1600
            hist = cv2.calcHist([warped], [0], None, [scal], [250, 1850])

            # 使用极值法求取Z的高度值
            s_arry = hist[:, 0]
            num_peak_3 = signal.find_peaks(s_arry, height=100, distance=10)  # distance表极大值点的距离至少大于等于10个水平单位

            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)

            z_value = 1900 - (maxLoc[1] + 250)
            if len(num_peak_3[0]) == 0:
                z_value_max = z_value
            else:
                z_value_max = 1900 - (num_peak_3[0][0] + 250)

                # 箱子中心点
            x_w, y_w, z_w = self.cam2word(frameData.cameraParams, center_x, center_y, z_value, 1900, distanceData)
            # tltr

            x_w_tltr, y_w_tltr, z_w_tltr = self.cam2word(frameData.cameraParams, tl[0], tl[1], z_value, 1900,
                                                         distanceData)

            # blbr
            x_w_blbr, y_w_blbr, z_w_blbr = self.cam2word(frameData.cameraParams, tr[0], tr[1], z_value, 1900,
                                                         distanceData)

            # tlbl
            x_w_tlbl, y_w_tlbl, z_w_tlbl = self.cam2word(frameData.cameraParams, br[0], br[1], z_value, 1900,
                                                         distanceData)

            # trbr
            x_w_trbr, y_w_trbr, z_w_trbr = self.cam2word(frameData.cameraParams, bl[0], bl[1], z_value, 1900,
                                                         distanceData)

            dA = dist.euclidean((x_w_tltr, y_w_tltr), (x_w_blbr, y_w_blbr))
            dB = dist.euclidean((x_w_tlbl, y_w_tlbl), (x_w_trbr, y_w_trbr))
            if dA < dB:
                dA, dB = dB, dA
            angle = 0.0 - angle
            if angle > 90:
                angle = angle - 180
            else:
                angle = angle

            # 箱子结果可视化

            # 画外接矩形框
            cv2.drawContours(img_bgr, [box.astype("int")], 0, (0, 255, 0), 1)

            # 画四个顶点坐标
            for (x, y) in box:
                cv2.circle(img_bgr, (int(x), int(y)), 5, (0, 0, 255), -1)

            cv2.circle(img_bgr, (center_x, center_y), 5, 128, -1)

            str1 = str(boxcount)  # 把坐标转化为字符串
            cv2.putText(img_bgr, str1, (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1,
                        cv2.LINE_AA)  # 绘制坐标点位

            a = np.array([boxcount, dA, dB, z_value, z_value_max, x_w, y_w, z_w, angle])
            box_list.append(a)

            boxcount += 1

        # 箱子排序
        box_list = np.array(box_list)
        # 按中心点x排序
        box_list = box_list[np.lexsort([-box_list[:, 5]])]
        # 按中心点y排序
        box_list = box_list[np.lexsort([-box_list[:, 6]])]
        layer_Z = box_list[0][7] + 15
        # 箱子太高
        if layer_Z > 5000:
            send_message = "1,1,1,1,1,1"
            self.send_robot(send_message)
        else:
            for box_detail in box_list:
                # 进行坐标转换
                P_cam = box_detail[5:8]
                P_rob = ([[box_detail[5]], [box_detail[6]], [box_detail[7]]])
                send_message = '001' + ',' + '%.0f' % P_rob[0][0] + ',' + '%.0f' % P_rob[1][0] + ',' + '%.0f' % \
                               P_rob[
                                   2][0] + ',' + '%.0f' % (box_detail[8]) + ',' + str(len(box_list)) + '\n'
                self.write_msg(send_message)
        self.read_robot_image(img_bgr)

    # 相机坐标转世界坐标
    def cam2word(self, cameraParams, p_x, p_y, z_value, def_plane, distanceData):

        cx = cameraParams.cx
        fx = cameraParams.fx
        cy = cameraParams.cy
        fy = cameraParams.fy
        m_c2w = cameraParams.cam2worldMatrix
        # 中心点
        # 相机坐标系
        xp = (cx - p_x) / fx
        yp = (cy - p_y) / fy
        if p_y > 510:
            p_y = 510
        zc = distanceData[int(p_y) * 640 + int(p_x)]
        if zc == 0.0:
            zc = def_plane - z_value
        xc = xp * zc
        yc = yp * zc
        # 世界坐标系
        x_w = round(m_c2w[0 * 4 + 3] + zc * m_c2w[0 * 4 + 2] + yc * m_c2w[0 * 4 + 1] + xc * m_c2w[0 * 4 + 0], 0)
        y_w = round(m_c2w[1 * 4 + 3] + zc * m_c2w[1 * 4 + 2] + yc * m_c2w[1 * 4 + 1] + xc * m_c2w[1 * 4 + 0], 0)
        z_w = round(m_c2w[2 * 4 + 3] + zc * m_c2w[2 * 4 + 2] + yc * m_c2w[2 * 4 + 1] + xc * m_c2w[2 * 4 + 0], 0)
        return x_w, y_w, z_w

    # 标记好的图片展示
    def read_robot_image(self, cvimg):
        # 在QgraphicsScene上呈现检测结果图
        height, width, depth = cvimg.shape
        cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        cvimg = QImage(cvimg.data, width, height, width * depth, QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(cvimg)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)  # 将场景添加至视图

    def write_msg(self, msg):
        self.textBrowser.insertPlainText(msg)
        # 滚动条移动到结尾
        self.textBrowser.moveCursor(QtGui.QTextCursor.End)
