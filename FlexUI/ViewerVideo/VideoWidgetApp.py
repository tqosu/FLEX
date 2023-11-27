# create user interface

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QWidget,QAction,QMenu,  QMenuBar,QStatusBar
# from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon,QImage, QPixmap,QKeySequence

import numpy as np
import cv2
import sys

from collections import defaultdict
import sys,json,os
from .VideoThreadApp import VideoThread
from ..app_helper import spoint

class VideoApp(QWidget):
    frame_id = pyqtSignal(int)
    # annotations_id = pyqtSignal(dict)
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Media Player") 
        self.setWindowIcon(QIcon('./icons/bridge.png'))
        self.disply_width = 1000
        self.display_height = 600
        self.annotation_on = False
        self.parent=parent
        #self.disply_width = 670
        #self.display_height = 540
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.setMinimumSize(self.disply_width, self.display_height)
        #self.image_label.setStyleSheet("border :3px solid black;")
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.image_label.mousePressEvent = self.video_clicked

        # create a text label
        self.textLabel = QLabel('Video')
        self.textLabel.setStyleSheet("border :1px solid black;")

        # self.menu_bar = QMenuBar(self)
        # # Create a menu
        # self.remove_menu = self.menu_bar.addMenu('Remove')

        # for i in range(4):
        #     # Create exit action
        #     action = QAction('&Remove '+str(i+1), self, checkable=True)
        #     action.setChecked(False)
        #     action.setStatusTip('Remove '+str(i+1))
        #     action.setData(i)
        #     action.setShortcut(str(i+1))
        #     # action.setShortcut(Qt.Key_Plus)
        #     action.triggered.connect(self.removeSelect)
        #     self.remove_menu.addAction(action)

        # self.swap_menu = self.menu_bar.addMenu('Swap')

        # for i in range(4):
        #     # Create exit action
        #     action = QAction('&Swap View '+str(i+1), self, checkable=True)
        #     action.setChecked(False)
        #     action.setShortcut(QKeySequence(Qt.ControlModifier + getattr(Qt, f"Key_{i+1}")))
        #     # action.setStatusTip('Swap view '+str(i+1))
        #     action.setData(i)
        #     action.triggered.connect(self.swapSelect)
        #     self.swap_menu.addAction(action)

        # self.statusBar = QStatusBar(self)
        vbox = QVBoxLayout()
        # vbox.addWidget(self.menu_bar)
        vbox.addWidget(self.image_label)#, alignment=Qt.AlignCenter)
        vbox.addWidget(self.textLabel, alignment=Qt.AlignBottom)
        # vbox.addWidget(self.statusBar)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        self.duration_on, self.duration_off= 0, 0
        self.width_video, self.height_video = 0, 0
        self.last_position = 0
        self.p2d = {}
        self.clicked_att = {}

        # start the thread     
        self.view = [0]
        self.setThread()

    def show_message(self, message):
        self.statusBar().showMessage(message)

    def clear_message(self, event):
        self.statusBar().clearMessage()

    def Box_Frame_Update(self):
        # curr_frame=self.mediaPlayer.thread.curr_frame-1
        # self.setPosition(self.mediaPlayer.thread.curr_frame)
        keymap1={0:'R', 1:'L'}
        data=self.thread.data
        t=self.thread.curr_frame
        myres={'midpoint':defaultdict(dict),'3dp':{}}

        if 'box_r' in data[t]:
            box_r=data[t]['box_r']
        else:
            box_r=set()
        
        for view in range(4): 
            if view in box_r:continue
            if view in data[t]['midpoint']:
                # myres['box'][view]=data[t]['box'][view]
                myres['midpoint'][view]=data[t]['midpoint'][view]
        for key in range(2):
            point=spoint(self.parent.cams,myres['midpoint'],key)
            if point is not None:
                key1=keymap1[key]
                myres['3dp'][key1]=point
        data[t]['3dp']=myres['3dp']
        # print("# location 6", self.thread.curr_frame)
        self.thread.run_one(0)

    def swapSelect(self):
        view_id = self.sender().data()
        data=self.thread.data
        t=self.thread.curr_frame
        box=data[t]['box']
        midpoint=data[t]['midpoint']
        # print(self.thread.data[self.thread.curr_frame]['midpoint'])
        if view_id not in box:return 
        myres={'midpoint':defaultdict(dict),'box':defaultdict(dict)}

        # box swap
        if 'box_s' in self.thread.data[self.thread.curr_frame]:
            box_s=data[t]['box_s']
        else:
            box_s=set()
        if view_id in box_s:
            box_s.remove(view_id)
        else:
            box_s.add(view_id)
        for key in box[view_id]:
            myres['midpoint'][view_id][1-key]=midpoint[view_id][key]
            myres['box'][view_id][1-key]=box[view_id][key]
        box[view_id]=myres['box'][view_id]
        midpoint[view_id]=myres['midpoint'][view_id]
        data[t]['box_s']=box_s
        print("Swap view {}".format(view_id+1))
        # print(self.thread.data[self.thread.curr_frame]['midpoint'])
        self.Box_Frame_Update()
        # self.thread.run_one(0)


    def removeSelect(self):
        # print("# location 8", self.thread.curr_frame)
        view_id = self.sender().data()
        
        if 'box_r' not in self.thread.data[self.thread.curr_frame]:
            self.thread.data[self.thread.curr_frame]['box_r']=set()
        myset=self.thread.data[self.thread.curr_frame]['box_r']

        if view_id not in myset:
            if len(myset)>=2:
                # actions[view_id].setChecked(False)
                print("Please keep at least two valid views.")
            else:
                myset.add(view_id)
                # actions[view_id].setChecked(True)
        else:
            myset.remove(view_id)
        print("Removed Views",end='')
        print(myset)
        self.Box_Frame_Update()


    def setThread(self):
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        # self.thread.protractor_signal.connect(self.update_image)
        self.thread.frame_id.connect(self.update_text)
        return

    def select_view(self, img):
        h, w, _ = img.shape
        if self.view[0] in [0,5]: return img
        im = []
        for view in self.view:
            if view == 1: im.append(img[:h//2, :w//2])
            elif view == 2: im.append(img[:h//2, w//2:])
            elif view == 3: im.append(img[h//2:, :w//2])
            elif view == 4: im.append(img[h//2:, w//2:])
        im = np.concatenate(im, axis=0)
        return im
    
    def set_file(self, mydict):
        self.thread._run_flag = False
        self.duration_on, self.duration_off, self.height_video, self.width_video = self.thread.set_file(mydict)    
        self.last_position=self.duration_on
        # self.resize(self.height_video, self.width_video)
    def reset_action_menu(self, query, actions):
        for i,action in enumerate(actions):
            if query not in self.thread.data[self.thread.curr_frame]:
                action.setChecked(False)
            else:
                if i in self.thread.data[self.thread.curr_frame][query]:
                    action.setChecked(True)
                else:
                    action.setChecked(False)
    def setPosition(self, position):
        self.thread.position_flag = position
        second = position//self.thread.fps
        self.textLabel.setText("Time: {:.0f}:{:.0f} \t-\t Frame: {}".format(second//60, second % 60, position))
        self.last_position = position
        self.reset_action_menu( 'box_r', self.parent.remove_menu.actions())
        self.reset_action_menu( 'box_s', self.parent.swap_menu.actions())
        
        # print('location 1')
        return

    def update_last_image(self):
        self.thread.get_last_image()
    
    def showImage(self):
        self.thread.get_image(self.last_position)
    
    def stop_video(self):
        self.thread._run_flag = False
    
    def start_video(self,S,D,one2one=False):
        print("S {:.1f}, D {}".format(S,D))
        self.thread._run_flag = True
        self.thread.S = S
        self.thread.D = D
        self.thread.one2one=one2one
        self.thread.start()
    
    def closeEvent(self, event):
        self.stop_video()
        event.accept()
    
    def close_thread(self):
        self.thread._run_flag = False
        self.thread.exit()
        self.thread.wait()
        return

    def video_clicked(self, event):
        if not self.annotation_on: return
        return
    
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        
        qt_img = self.convert_cv_qt(cv_img)
        # print(qt_img.shape)
        self.image_label.setPixmap(qt_img)
    
    # @pyqtSlot(np.ndarray)
    # def update_image1(self, cv_img):
    #     self.cv_img1=cv_img

    @pyqtSlot(int)
    def update_text(self, frame):
        second = frame//self.thread.fps
        self.textLabel.setText("Frame: {} \t Time: {} mn {} s".format(frame, second//60, second % 60))
        self.frame_id.emit(frame)
    
    @pyqtSlot(bool)
    def set_annotation(self, state):
        self.annotation_on = state
    
    @pyqtSlot(bool)
    def send_annotation(self, state):
        self.annotations_id.emit(self.clicked_att)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        cv_img = self.select_view(cv_img)
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        #p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)

        #convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio)

        return QPixmap.fromImage(p)