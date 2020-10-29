# -*- mode: python ; coding: utf-8 -*-

import sys
sys.setrecursionlimit(5000)
block_cipher = None


a = Analysis(['main_logic.py', 'picture_logic.py', 'show_logic.py', 'train_logic.py', 'camera\\camera_utils.py', 'camera\\Data.py', 'camera\\Device.py', 'mrcnn\\config.py', 'mrcnn\\getmakpolygon.py', 'mrcnn\\model.py', 'mrcnn\\parallel_model.py', 'mrcnn\\utils.py', 'mrcnn\\visualize.py', 'resource\\main_ui.py', 'resource\\picture_ui.py', 'resource\\show_ui.py', 'resource\\train_ui.py'],
             pathex=['G:\\Anaconda3\\envs\\simple\\Lib\\site-packages', 'G:\\DL\\Project\\Versionary_3D - 副本'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main_logic',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main_logic')
