import cv2

class Finder():  # 选择智能选区
    def __init__(self, parent):
        self.h = self.w = 0
        self.rect_list = self.contours = []
        self.area_threshold = 200
        self.parent = parent
        self.img = None
    def find_contours_setup(self):
        try:
            self.area_threshold = self.parent.parent.ss_areathreshold.value()
        except Exception:
            self.area_threshold = 200
        # t1 = time.process_time()
        # self.img = cv2.imread(f'{Path(__file__).parent}/tmp/get.png')
        # t2 = time.process_time()
        self.h, self.w, _ = self.img.shape
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)  # 灰度化
        # t3 = time.process_time()
        # ret, th = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
        th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)  # 自动阈值
        # th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_TRUNC, 11, 2)  # 自动阈值
        # t4 = time.process_time()
        self.contours = cv2.findContours(th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
        self.find_contours()
        # print('setuptime', t2 - t1, t3 - t2, t4 - t3)

    def find_contours(self):
        draw_img = cv2.drawContours(self.img.copy(), self.contours, -1, (0, 255, 0), 1)
        # cv2.imshow("tt", draw_img)
        # cv2.imwrite("test.png", self.img.copy())
        # cv2.waitKey(0)
        # newcontours = []
        self.rect_list = [[0, 0, self.w, self.h]]
        for i in self.contours:
            x, y, w, h = cv2.boundingRect(i)
            area = cv2.contourArea(i)
            if area > self.area_threshold and w > 10 and h > 10:
                # cv2.rectangle(self.img, (x, y), (x + w, y + h), (0, 0, 255), 1)
                # newcontours.append(i)
                self.rect_list.append([x, y, x + w, y + h])
        # print('contours:', len(self.contours), 'left', len(self.rect_list))

    def find_targetrect(self, point):
        # print(len(self.rect_list))
        # point = (1000, 600)
        target_rect = [0, 0, self.w, self.h]
        target_area = 1920 * 1080
        for rect in self.rect_list:
            if point[0] in range(rect[0], rect[2]):
                # print('xin',rect)
                if point[1] in range(rect[1], rect[3]):
                    # print('yin', rect)
                    area = (rect[3] - rect[1]) * (rect[2] - rect[0])
                    # print(area,target_area)
                    if area < target_area:
                        target_rect = rect
                        target_area = area
                        # print('target', target_area, target_rect)
                        # x,y,w,h=target_rect[0],target_rect[1],target_rect[2]-target_rect[0],target_rect[3]-target_rect[1]
                        # cv2.rectangle(self.img, (x, y), (x + w, y + h), (0, 0, 255), 1)
        # cv2.imwrite("img.png", self.img)
        return target_rect

    def clear_setup(self):
        self.h = self.w = 0
        self.rect_list = self.contours = []
        self.img = None
