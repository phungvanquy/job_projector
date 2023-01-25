# Содержание

1. [Схема подключение](#Схема-подключение)
2. [Интрукция для тестирования](#Интрукция-для-тестирования)
3. [Описание структуры ПО](#test-instruction)
4. [Описание принцип работы и формата TCP/IP пакет для управления прожектором](#Описание-принцип-работы)

# <p id="Схема-подключение">1. Схема подключение</p>

Это павел сделает </br>
!!! Внимательно: что pin A1(Arduino) для измерения ADC value

# <p id="Интрукция-для-тестирования"></p>2. Инструкция для тестирования

Run into Virtual Environment

```bash
python3 -m venv venv &&
source ./venv/bin/activate
```

Install all dependencies

```bash
pip install -r requirements.txt
```

Run test file

```bash
python3 main.py
```

Result must be like this:

```bash
************* Successfully connected to TCPServer 192.168.113.10:23 ****************
SET <parameter> <value>: Set value for a parameter angle of fan
Enter the command:
```

Now you can enter command **set angle [value]** to control projector, for example:

```bash
set angle 10
```

# <p id="structure-description"></p> 3. Описание структуры ПО

```
📦backend
 ┣ 📂model                  (Build Machine learning Model to convert ADC_value->angle or vice versa)
 ┃ ┣ 📜data.csv             (Dataset)
 ┃ ┗ 📜modelEncoderADC.py   (Genereated ML model)
 ┣ 📜README.md              (Instruction file)
 ┃ 📜main.py                (Testing source file)
 ┗ 📜requirements.txt       (Dependencies file)
```

# <p id="Описание-принцип-работы"></p>4. Описание принципа работы и формата TCP/IP пакета для управления прожектором

## Принцип работы:

<p style="text-align:justify" >1. Из ПК TCP/IP команда (сообщение) отправлена на Arduino. В этом сообщение включено значение ADC_value для управления прожектором. Arduino получает это значение и управляет мотором так чтобы прожектор поворачивал к желаемому углу. Внимание в том что Arduino понимает только значение энкодера (ADC_value), а не значения желаемого угла </p>
<p style="text-align:justify" >2. Как можно получить значение ADC из угла? <br> - Оно можно получить с помощью Machine learning model. Это model используется для Convert "angle" to "ADC_value".</p>
<p style="text-align:justify" >3. Почему нужно использовать Machine Learning (ML) Model? <br> - Так как во время эксперимента мы заметили что зависимость между угла и значением энкодера (ADC_value) НЕ ЛИНЕЙНО из за погрешности и сложности конструкции комплекса. Поэтому  ML model (Polynomial regression) используется для решения этой проблемы.  <br> - Суть метода заключается в том что мы измеряем значение энкодера в соответствии с разными значениями угла поворота (Файл /model/data.csv). Из этих данных мы можем построить model (функцию зависимости угла и ADC_value). Преимущество этого метода в том что тем больше данные мы измеряем, чем точнее результат получим</p>

## Формат TCP/IP пакета:

<p style="text-align:justify">Так как мы используем протокол TCP/IP socket protocol поэтому нужно знать Arduino socket: <br>
- ip: 192.168.113.10 <br>
- port: 23 <br>
Для управления прожектором нам нужно отправить socket сообщение в виде byte stream по следующему формату:
<table style="text-align:center">
  <tr>
    <th></th>
    <th>BYTE_STREAM[0]</th>
    <th>BYTE_STREAM[1]</th>
    <th>BYTE_STREAM[2]</th>
    <th>BYTE_STREAM[3]</th>
  </tr>
  <tr>
    <td>Value</td>
    <td>'S'</td>
    <td>ADC_value_to_send / 100</td>
    <td>ADC_value_to_send % 100</td>
    <td>'\n'</td>
  </tr>
</table>
Например если мы хотим отправить ADC_value = 925 на Arduino. Тогда сообщение будет 
<table style="text-align:center">
  <tr>
    <th></th>
    <th>BYTE_STREAM[0]</th>
    <th>BYTE_STREAM[1]</th>
    <th>BYTE_STREAM[2]</th>
    <th>BYTE_STREAM[3]</th>
  </tr>
  <tr>
    <td>Value</td>
    <td>'S'</td>
    <td>9</td>
    <td>25</td>
    <td>'\n'</td>
  </tr>
</table>

Пример в python

```python
import socket
socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.113.10', 23))
valueToSend = 925
stringToSend =  'S' + chr(int(valueToSend/100)) + chr(int(valueToSend%100)) + '\n'
sock.send(stringToSend.encode('utf-8'))
```
