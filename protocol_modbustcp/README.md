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

```
Angle to set:5
Angle:  10
Angle:  10
Angle:  9
Angle:  8
Angle:  8
Angle:  8
Angle:  7
Angle:  7
Angle:  7
Angle:  6
Angle:  5
Angle to set:
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

# <p id="Описание-принцип-работы"></p>4. Описание принципа работы и Modbus TCP/IP для управления прожектором

## 4.1. Принцип работы:

<p style="text-align:justify" >1. Из ПК (master) Modbus Request запись в holding register (1001) отправлена на Arduino (slave). В этом Request включаются значение Angle_value для управления прожектором. Arduino получает эти значений и управляет мотором так чтобы прожектор поворачивал к желаемому углу. Одновременно с этим master может читать значние текущего угла поворачивания прожектора с момощью modbus Request на читать holding регистор (1002) </p>
<p style="text-align:justify" >2. Как можно получить значение ADC из угла? <br> - Оно можно получить с помощью Machine learning model. Это model используется для Convert "angle" to "ADC_value".</p>

```python
from model.modelEncoderADC import angleToADC, ADCtoAngle
angle = 350
print("Converted ADC value:", angleToADC)
```
<p style="text-align:justify" > - Если converting process положим в Arduino to мы можем получить параметры у ML model:</p>

```python
from model.modelEncoderADC import reg_angleToADC_model
print("Coef of model", reg_angleToADC_model.coef_)
print("Bias (or Intercept) of model", reg_angleToADC_model.intercept_)
``` 

<p style="text-align:justify" >3. Почему нужно использовать Machine Learning (ML) Model? <br> - Так как во время эксперимента мы заметили что зависимость между угла и значением энкодера (ADC_value) НЕ ЛИНЕЙНО из за погрешности и сложности конструкции комплекса. Поэтому  ML model (Polynomial regression) используется для решения этой проблемы.  <br> - Суть метода заключается в том что мы измеряем значение энкодера в соответствии с разными значениями угла поворота (Файл /model/data.csv). Из этих данных мы можем построить model (функцию зависимости угла и ADC_value). Преимущество этого метода в том что тем больше данные мы измеряем, чем точнее результат получим</p>


## 4.2. Управлять прожектором с Modbus TCP/IP:

<p style="text-align:justify">Так как мы используем протокол Modbus TCP/IP socket protocol поэтому нужно знать Arduino socket: <br>
- ip: 192.168.1.222 <br>
- port: 502 <br>
Для управления прожектором нам нужно обратиться внимание на адресы регисторов:
<table style="text-align:left">
  <tr>
    <th>Value</th>
    <th>Address</th>
    <th>Type Of Register</th>
    <th>MIN ---> MAX</th>
    <th>Description</th>

  </tr>
  <tr>
    <td>ADC_Value</td>
    <td>1000</td>
    <td>Holding Register</td>
    <td>-</td>
    <td>Текущее значение ADC value, которое мы хотим читать</td>
  </tr>
    <tr>
    <td>Angle_Value_To_Set</td>
    <td>1001</td>
    <td>Holding Register</td>
    <td>(-18 ) 342 ---> 24 </td>
    <td>Желаемое значение угла, с которым мы хотим управлять прожектором</td>
  </tr>
    </tr>
    <tr>
    <td>Angle_Value</td>
    <td>1002</td>
    <td>Holding Register</td>
    <td>-</td>
    <td>Текущее значение ADC value, которое мы хотим читать <br> (Its converted from ADC_Value with a trained model)</td>
  </tr>
</table>

<b>Внимание:</b> Если мы хотим чтобы точность работы у прожектора больше была, тогда нам нужно использовать ADC_value (адрес 1000). Мы измеряем углы и сопоставить эти значения с соответствующими значениями ADC_value. Потом мы Train model занова 

Пример в python
```python
# Это программа для тестирования работы прожетора
# 1. Сначала пользователь нужно задать угол для управлять. 
# 2. Потом она постоянно читает значения угла прожектора
import time
from pyModbusTCP.client import ModbusClient
c = ModbusClient(host="192.168.1.222", port=502, unit_id=1, auto_open=True)

angleToSet = int(input("Angle to set:"))

# Задать значения угла (адрес 1001) чтобы управлять
c.write_single_register(1001,angleToSet)
while(True):
    if(regs != angleToSet):
        # Читать значение текущего угла в регисторе (адрес 1002)
        regs = c.read_holding_registers(1002,1)[0]
        print("Angle: ",regs)
    else:
        angleToSet = int(input("Angle to set:"))
        if angleToSet == 360:
          angleToSet = 0
        c.write_single_register(1001,angleToSet)
    time.sleep(0.05)
```

