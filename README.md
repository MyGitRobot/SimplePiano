# SimplePiano
A simple piano simulator / tool / assistant that can note notes

## Simple Piano

### Introduction

- A simple piano which can show key information and note down notes. Moreover, it can switch key map to selected chords.
- Content:
  - **soundLib** folder
  - **Simple Piano.exe**

### Materials

- **sys**
- **os**
- **PyQt6**
- **pygame**
- **pynput**
- **logging**

### Method

- Notice: Don't forget to download **soundLib** to local, or you cannot run it successfully. (Download **soundLib** from `Releases`)
- **Simple Piano 1.0.0**
  - Work Space
    - State: Show real-time work state
    - Information
      - Scale: Choose what scale to display for keys pressed
      - Keys origin: Show original note pitch of keys that you pressed
      - Keys on scale: Show grades on scale of keys pressed
      - Scale: Show what notes on the selected scale

    - `Switch to Scale`: Switch keys pitch to selected scale
    - Keyboard: Where you can play the piano, only available when focused
      - Click piano keys on screen to make sounds.
      - Press PC keyboard like `S` `P` `2` etc. to make sounds. The characters on the piano keyboard indicate buttons on PC keyboard.

  - Note Pad
    - You can note down something here such as some thoughts, notes heard, plans to do and etc.
    - Click `Save` button to save the content of Note Pad.
    - Forgot to click `Save` button before quit? Don't worry. It will automatically saved when you exit Simple Piano.

- Download link: https://github.com/MyGitRobot/SimplePiano/releases/download/v1.0.0/SimplePiano.zip

### Statement

- **ONLY** for personal learning, **NOT for Commercial Use**!

## 简易钢琴助手

### 简介

- 一款简易钢琴软件，实时显示按下的琴键及所在调式的级数，并且可以做笔记。
- 包含：
  - **soundLib** folder
  - **Simple Piano.exe**

### 需要的包

- **sys**
- **os**
- **PyQt6**
- **pygame**
- **pynput**
- **logging**

### 使用说明

- 注意：缺乏**soundLib**文件夹则无法正常运行（请从`Releases`下载）
- **Simple Piano 1.0.0**
  - Work Space
    - State: 显示各种操作状态
    - Information
      - Scale: 选择所在调式
      - Keys origin: 显示按下键盘的原始音高
      - Keys on scale: 显示按下键盘在所选调式的级数
      - Scale: 显示所选调式包含的音名
    - `Switch to Scale`: 切换按键映射到所选调式，改变钢琴音高
    - Keyboard: 弹钢琴的地方，只有该区域拥有焦点时可以弹奏
      - 鼠标点击钢琴键盘发声。
      - 按下电脑键盘如`S` `P` `2`等也可以发声，钢琴键盘上的字符表示电脑键盘的按键。
  - Note Pad
    - 可以在这记录音符、想法和计划等。
    - 点击`Save`按钮保存Note Pad内容。
    - 没点`Save`也没事，关闭Simple Piano时会自动保存。
- 下载链接：https://github.com/MyGitRobot/SimplePiano/releases/download/v1.0.0/SimplePiano.zip

### 声明

- 仅供个人学习使用，**禁止商用**！
