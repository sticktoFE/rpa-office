import win32con
import win32gui

# 本程序可用微软的spy++小程序代替，那个很方便
# hwnd_title是一个dict
def get_all_hwnd_title(hwnd,hwnd_title_dict):
      #这个根据情况可以去掉
      # if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title_dict.update({hwnd:(win32gui.GetClassName(hwnd),win32gui.GetWindowText(hwnd))})
#获取能识别的所有窗口，包括本身和子孙窗口
def get_all_hwnds():
      # f = open('./log.txt','w',encoding="utf-8")
      hwnd_title_dict = dict()
      temp_hwnd_title_dict = dict()
      win32gui.EnumWindows(get_all_hwnd_title,temp_hwnd_title_dict)
      hwnd_title_dict.update(temp_hwnd_title_dict)
      for h,t in temp_hwnd_title_dict.items():
            if h is not None :
                  print("+--" + f"顶层窗口:{hex(h),t}")#,file=f)
                  get_child_hwnds(h,hwnd_title_dict,1)
      # f.close()
      return hwnd_title_dict
#获取parent_hwd及所有子孙的窗口体系
def get_child_hwnds(parent_hwd,hwnd_title_dict,depth): 
      if parent_hwd is None:
            print("parent_hwd不能为空")
            return
      temp_hwnd_title_dict = dict()
      win32gui.EnumChildWindows(parent_hwd,get_all_hwnd_title,temp_hwnd_title_dict)
      hwnd_title_dict.update(temp_hwnd_title_dict)
      for h,t in temp_hwnd_title_dict.items():
            if h is not None and win32gui.GetParent(h) == parent_hwd:
                  print("|      " * depth + "+--" + f"{depth+1}层:{h,hex(h),t[0],t[1]}")
                  get_child_hwnds(h,hwnd_title_dict,depth +1)
#获取特定窗口的子窗口的hwnd                 
def get_hwnd(parent_hwnd,wnd_name):
      result_hwnd = 0
      hwnd_title_dict = dict()
      #枚举所有子窗口，包括孙子窗口,如果parent_hwnd为空 类似 EnumWindows只列举顶层窗口
      win32gui.EnumChildWindows(parent_hwnd,get_all_hwnd_title,hwnd_title_dict) 
      for h,t in hwnd_title_dict.items():
            if len(t)>0  and t == wnd_name:
                  return h
            else:
                  result_hwnd = get_hwnd(h,wnd_name)
                  if result_hwnd>0:
                        return result_hwnd
      return result_hwnd

# phwd =get_hwnd(None,"多屏协同")
# print("**********")
# print(phwd)
# #获取'系统设置'的句柄
# w3hd=win32gui.FindWindowEx(phwd,None,None,'plrNativeInputWindow')
# print(w3hd)


# menu = win32gui.GetMenu(66962)
# # menu1 = win32gui.GetSubMenu(328994, 1)#第几个菜单
# print(menu)
# for i in range(5):
#     print(get_menu_item_txt(menu,i))
# get_hwnds("BlueStacks",None)
hwnds = get_all_hwnds()
print(hwnds)
# for h,t in tem_dict.items():
#       menu = win32gui.GetMenu(h)
#       if menu>0:
#             print("------------")
#             print(menu)
#             # print(get_menu_item_txt(menu,1))

print(hex(66292))

def get_menu_item_info(window_name):
      hwnd = win32gui.FindWindow(None, window_name)
      menu = win32gui.GetMenu(hwnd)
      menu1 = win32gui.GetSubMenu(menu, 1)#第几个菜单
      cmd_ID = win32gui.GetMenuItemID(menu1, 1)#第几个子菜单
      win32gui.PostMessage(hwnd, win32con.WM_COMMAND, cmd_ID, 0)
#获取某个菜单的内容
def get_menu_item_txt(menu,idx):
    import win32gui_struct
    mii, extra = win32gui_struct.EmptyMENUITEMINFO() #新建一个win32gui的空的结构体mii
    win32gui.GetMenuItemInfo(menu, idx, True, mii) #将子菜单内容获取到mii
    ftype, fstate, wid, hsubmenu, hbmpchecked, hbmpunchecked,\
    dwitemdata, text, hbmpitem = win32gui_struct.UnpackMENUITEMINFO(mii) #解包mii
    return text
