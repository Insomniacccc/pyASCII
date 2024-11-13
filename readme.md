**PYTHON JPEG TO ASCII CONVERTER**
_by Dmitry Alekhin_

Console application that transform your picture into greyscale picture and makes ASCII art.
App has a few arguments

1. **img_name** Required position string argument that contains name of your Jpeg picture in 'Pics' folder
2. **--height** - unnecessary integer argument that you can use to change your ASCII art height 
(by default ASCII art width = height of originally picture // 13). Example: --height=1080
3. **--width** - unnecessary integer argument that you can use to change your ASCII art width 
(by default ASCII art width = height of originally picture // 5). Example: --width=1920
4. **--write** - unnecessary argument. It if use it, then your ASCII-art will be written into .txt file in 'ASCII' folder
5. **--view** - unnecessary argument. You can use it to see your ASCII-art txt's from ASCII folder. Also you can zoom your ASCII-art picture(integer numbers only)

**Examples:**
1. Use python ascii.py pic2 --height 50 --width 100 to create new ASCII art
2. Use python ascii.py pic2 --view to run view mode with zoom feature
