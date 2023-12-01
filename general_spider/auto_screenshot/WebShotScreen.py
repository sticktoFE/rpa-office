from myutils.info_out_manager import get_temp_folder


class ShotScreenManager:
    def __init__(
        self,
        url,
        x=None,
        y=None,
        width=750,
        height=1370,
        callback=None,
        shot_driver=None,
    ):
        self.win_url = url
        self.shot_driver = shot_driver
        self.win_x = x
        self.win_y = y
        self.win_width = width
        self.win_height = height
        self.shot_callback = callback
        self.image_path = get_temp_folder(
            des_folder_path=__file__, is_clear_folder=True
        )
        self.temp_path = get_temp_folder(
            des_folder_path=f"{__file__}/tmp_pic", is_clear_folder=True
        )
        # 截完图的回调函数

    def checkShotCallback(self, file=None, error=None):
        if self.shot_callback:
            self.shot_callback({"file": file, "error": error})
        return self

    def shotScreen(self):
        print("BaseDriver->shotScreen")
        return self
