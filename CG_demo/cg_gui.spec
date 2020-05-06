# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['cg_gui.py'],
             pathex=['/Users/dingbaorong/Desktop/Github/ComputerGraphicsLabs/CG_demo'],
             binaries=[],
             datas=[('./resource', 'resource')],
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
          name='cg_gui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='resource/App.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='cg_gui')
app = BUNDLE(coll,
             name='cg_gui.app',
             icon='./resource/App.icns',
             bundle_identifier=None)
