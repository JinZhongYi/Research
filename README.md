## ECG_xml文件中12导联数据读取

## Name:
- 单个ECG_xml文件中12导联数据的读取并保存txt/mat文件

## Input:
- xml_url：xml文件路径
- save_url:输出文件保存路径
- file_type:选择保存文件格式txt/mat

## Output:
- 编号为1，2，3...的txt文件是原始xml中的digits的str类型文件无法直接用
- 编号为V1,V2,V3...的txt/mat文件是处理过后的N*1的数据

## Attenation:
- 如果要批量处理xml文件，先查找出所有xml文件路径，再批量新建文件夹存入数组，然后循环调用就行
