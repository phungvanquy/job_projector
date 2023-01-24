# Содержание
- Схема подключение
- Описание структуры ПО
- Описание принцип работы и формата TCP/IP пакет для управления прожектором
- Интрукция для тестирования


# Схема подключение
Это павел сделает </br>
!!! Внимательно: что pin A1(Arduino) для измерения ADC value

# Интрукция для тестирования
Run into Virtual Evvironment
``` bash
python3 -m venv venv &&  
source ./venv/bin/activate
```
Install all dependencies
``` bash
pip install -r requirements.txt
```
Run test file
``` bash
python3 main.py
```
Result must be like this:
``` bash
************* Successfully connected to TCPServer 192.168.113.10:23 ****************
SET <parameter> <value>: Set value for a parameter angle of fan
Enter the command:
```
Now you can enter command **set angle [value]** to control projector, for example:
``` bash
set angle 10
```



# Описание структуры ПО
```
📦backend
 ┣ 📂model                  (Build Machine learning Model to convert ADC_value->angle or vice versa)
 ┃ ┣ 📜data.csv             (Dataset)
 ┃ ┗ 📜modelEncoderADC.py   (Genereated ML model)
 ┣ 📜README.md              (Instructtion file)
 ┃ 📜main.py                (Testing source file)
 ┗ 📜requirements.txt       (Dependencies file)
 ```


# Описание принцип работы и формата TCP/IP пакет для управления прожектором
## Принцип работы:
1.  Из ПК TCP/IP команда (сообщение) отправлена. В этом сообщение включено значение ADC value для управления прожектором.Arduino получает это значние и управляет мотором так чтобы прожектор перевачивал к желаемому углу</br>
2. Откуда возьмем значение ADC? Оно можно получить из Machine learning model. Это model используется для Convert angle to ADC value.