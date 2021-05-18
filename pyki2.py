#Библиотека для работы с измерительным контроллером КИ-2.3
#На основе протокола обмена ver 0.7
#URL: http://www.prompribor-kaluga.ru/upload/support/protocols/protokol%20obmena%20KI%202_3.pdf

import binascii
import time
import serial
import sys

#Настройка порта для GNU/Linux
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1, rtscts=False, dsrdtr=True)


#Команда остановки режима и получения окончательных результатов измерения
#Возвращает кортеж данных:
#режим, байт-состояния, время измерения, такты измерения, импульсы с Входа2(МФ)


def GetAndRest():
    ser.write(b'\xFE')     
    #print(data, type(data))
    data = memoryview(ser.readline())
    print(data, type(data))
    for i in data:
        print(i, type(i))
    bite0 = int.from_bytes(bytes(data[0]), byteorder='little')       #режим
    bite1 = binascii.hexlify(bytes(data[1])).decode('ASCII')         #байт-состояния
    bite24 = int.from_bytes(data[2:5], byteorder='little')
    time1 = bite24/4096
    string = (format(time1, '6.2f').replace('.', ',')) + ' '  #ВРЕМЯ
    bite57 = int.from_bytes(data[5:8], byteorder='little')    #Импульсы тактов
    bite810 =int.from_bytes(data[8:11], byteorder='little')   #импульсы с Входа2(МФ)
    bite1113 = int.from_bytes(data[11:14], byteorder='little')
    bite1416 = int.from_bytes(data[16:17], byteorder='little')
    bite1719 = int.from_bytes(data[17:20], byteorder='little')
    bite2022 = int.from_bytes(data[20:23], byteorder='little')
    bite2325 = int.from_bytes(data[23:25], byteorder='little')
    bite2628 = int.from_bytes(data[25:28], byteorder='little')
    bite29 = int.from_bytes(bytes(data[28]), byteorder='little')


    if time1 == 0: time1=0.001    
    F=bite810/time1
    FMAX=1000    
    GMAX=3.75
    G=F*GMAX/FMAX
    V=G/3.6*time1
    G1=V/time1*3.6
    string += (format(G1, '6.4f').replace('.', ',')) + ' '   #РАСХОД
    string += (format(V, '6.4f').replace('.', ',')) + ' '   #ОБЪЕМ
    return string


def Get():
    ser.write(b'\xFD')         
    data = ser.readline()    
    bite0 = int.from_bytes(bytes(data[0]), byteorder='little')       #режим
    bite1 = binascii.hexlify(bytes(data[1])).decode('ASCII')         #байт-состояния
    bite2_4 = int.from_bytes(data[2:5], byteorder='little')
    time1 = bite2_4/4096
    string = (format(time1, '6.2f').replace('.', ',')) + ' '  #ВРЕМЯ
    bite5_7 = int.from_bytes(data[5:8], byteorder='little')    #Импульсы тактов
    bite8_10 =int.from_bytes(data[8:11], byteorder='little')   #импульсы с Входа2(МФ)
    bite11_13 = int.from_bytes(data[11:14], byteorder='little')
    bite17_19 = int.from_bytes(data[17:20], byteorder='little')
    bite20_22 = int.from_bytes(data[20:23], byteorder='little')
    bite23_25 = int.from_bytes(data[23:26], byteorder='little')
    bite26_28 = int.from_bytes(data[26:29], byteorder='little')
    bite29 = int.from_bytes(bytes(data[29]), byteorder='little')
    if time1 == 0: time1=0.001    
    F=bite8_10/time1
    FMAX=1000    
    GMAX=3.75
    G=F*GMAX/FMAX
    V=G/3.6*time1
    G1=V/time1*3.6
    string += (format(G1, '6.4f').replace('.', ',')) + ' '   #РАСХОД
    string += (format(V, '6.4f').replace('.', ',')) + ' '   #ОБЪЕМ
    return string

def SpprCmdTMeasure(time):
    """Измерение импульсов по времени, (Время в секундах)"""
    byte0 = b'\x00'
    message = byte0
    byte1_3 = (time*4096).to_bytes(3, byteorder='little')
    message += byte1_3
    byte4 = ControlSumm(message)
    message += (byte4)
    ser.write(message)
    data = ser.readline()
    if data == message:
        string = ('Измерение импульсов, в течении '+ str(time) +' секунд.')
    else: string = ( 'Произошла ошибка! \n', data)
    return string


def SpprCmdSS1Measure():
    """Измерение  импульсов  по  потенциальному  сигналу старт стоп."""
    message = b'\x01'
    ser.write(message)
    data = ser.readline()
    if data == message:
        string = ('"Измерение импульсов, по сигналу "СТАРТ-СТОП 1"')
    else: string = ( 'Произошла ошибка! \n', data)
    return string


def SpprCmdSS2Measure():
    """Измерение  импульсов по импульсному  сигналу  старт-стоп."""
    message = b'\x02'
    ser.write(message)
    data = ser.readline()
    if data == message:
        string = ('"Измерение импульсов, по сигналу "СТАРТ-СТОП 2"')
    else: string = ( 'Произошла ошибка! \n', data)
    return string


def SpprCmdNMeasure(pulse, chanel):
    """Измерение импульсов по импульсам,(кол-во импульсов, канал)"""
    byte0 = b'\x03'
    message = (byte0)
    byte13 = pulse.to_bytes(3, byteorder='little')
    message += byte13
    while len(message)<4:
        message += (b'\x00')
    byte4 = chanel.to_bytes(3, byteorder='little')
    message += byte4
    byte5 = ControlSumm(message)
    message += byte5
    print(message)
    ser.write(message)
    data = ser.readline()
    if data == message:
        string = ('Измерение импульсов, в течении ', pulse, ' импульсов.')
    else: string = ('Произошла SpprCmdSS2Measure()ошибка!', data)
    return string


def SpprCmdSendTest():
    """Генерация импульсов"""
    pass #Не реализовано


def SpprCmdLaserOn():
    """Включить лазеры (подать напряжение на расходомер)"""
    message = b'\x05'
    ser.write(message)
    data = ser.readline()
    if data == message:
        string = ('Лазеры включены')
    else: string = ('Произошла ошибка!')
    return string


def SpprCmdLaserOff():
    """Выключить лазеры (снять напряжение с расходомера)"""
    message = b'\x06'
    ser.write(message)
    data = ser.readline()
    if data == message:
        string = ('Лазеры выключены')
    else: string = ('Произошла ошибка!')
    return string


def SpprCmdSetParam(): 
    """ Установить параметры
        Байт  Значение
        0  0x07 
        1  - 3  (TRIPLET) Delay 1 
        4 – 6  (TRIPLET) Delay 2 
        7 – 9  (TRIPLET) Delay 3 
        10 – 12  (TRIPLET) Delay 4 
        13  BYTE Edge 
        14 – 15   WORD nLaserDela y 
        16  Сумма
        Ответ:  Аналогичен  команде.  Параметры  записываются  в  eeprom,  затем
        считываются и отправляются обратно. 
        Ошибка: Если прибор находится в режиме.
        Dela y   – задержка начала формирования импу льсов канала  (0 – 0xFFFFFF)/4096 с
        Edge – детектир у емый фронт импу льса.  4 младших бита. 0 – спад 1 – фронт
        nLaserDela y   –  задержка  на  автоматическое  отключение  лазеров  после  окончания
        измерения. (nLaserDelay * 0,0144) c. 
    """
    pass  #Не реализовано


def SpprCmdGetParam():
    """ Считать параметры
        Байт  Значение
        0  0x08 
        Ответ: Аналогичен ответу  команды SpprCmdSetParam 
        Ошибка: Если прибор находится в режиме
    """
    pass  #Не реализовано


def SpprCmdGetVersion():
    message = b'\x09'
    ser.write(message)
    data = ser.readline()
    byte0 = int.from_bytes(data[0], byteorder='little')
    byte1 = int.from_bytes(data[1], byteorder='little')
    byte2 = int.from_bytes(data[2], byteorder='little')
    byte3 = int.from_bytes(data[3], byteorder='little')
    if data[4:] != ControlSumm(data[:-1]): print('Контрольная сумма неверна!')


def SpprCmdCalibrate100():
    pass  #Не реализовано


def SpprCmdCalibrate200():
    pass  #Не реализовано


def SpprCmdGetTemperature():
    message = b'\xFB'
    ser.write(message)
    data = ser.readline()
    byte0 = int.from_bytes(data[0:1], byteorder='little')
    print(data[0:1], byte0)
    byte1_2 = int.from_bytes(data[1:3], byteorder='little')
    print(data[1:3], byte12)
    byte3_4 = int.from_bytes(data[3:5], byteorder='little')
    print(data[3:5], byte34)
    byte5_6 = int.from_bytes(data[5:7], byteorder='little')
    print(data[5:7], byte56)
    byte7_8 = int.from_bytes(data[7:9], byteorder='little')
    print(data[7:9], byte78)
    byte9 = int.from_bytes(data[9:], byteorder='little')
    print(data[9:], byte9)
    if data[9:] != ControlSumm(data[:-1]): print('Контрольная сумма неверна!')


def SpprCmdGet():
    """ Запросить текущие значения и выйти из режима
        Байт  Значение
        0  0xFD
        Ответ:
        Если  прибор  не  находится  в  режиме  ответ  аналогичен  ответу   команды
    """
    message = b'\xFD'
    #print("Посылаю:", message)
    ser.write(message)         
    data = ser.readline()
    #print("Получаю:", bytes(data), len(data))    
    if len(data) == 4:
        string = "Прибор не в режиме"
        return string  
    bite0 = int.from_bytes(bytes(data[0]), byteorder='little')       #режим
    bite1 = binascii.hexlify(bytes(data[1])).decode('ASCII')         #байт-состояния
    bite2_4 = int.from_bytes(bytes(data[2:5]), byteorder='little')
    time1 = bite2_4/4096
    string = (format(time1, '6.2f').replace('.', ',')) + ' '  #ВРЕМЯ
    bite5_7 = int.from_bytes(data[5:8], byteorder='little')    #Импульсы тактов
    bite8_10 =int.from_bytes(data[8:11], byteorder='little')   #импульсы с Входа2(МФ)
    bite11_13 = int.from_bytes(data[11:14], byteorder='little')
    bite17_19 = int.from_bytes(data[17:20], byteorder='little')
    bite20_22 = int.from_bytes(data[20:23], byteorder='little')
    bite23_25 = int.from_bytes(data[23:26], byteorder='little')
    bite26_28 = int.from_bytes(data[26:29], byteorder='little')
    bite29 = int.from_bytes(bytes(data[29]), byteorder='little')
    if time1 == 0: time1=0.001    
    F=bite8_10/time1
    FMAX=1000    
    GMAX=3.75
    G=F*GMAX/FMAX
    V=G/3.6*time1
    G1=V/time1*3.6
    string += (format(G1, '6.4f').replace('.', ',')) + ' '   #РАСХОД
    string += (format(V, '6.4f').replace('.', ',')) + ' '   #ОБЪЕМ
    return string


def SpprCmdGetAndReset():
    """ Запросить текущие значения и выйти из режима
        Байт  Значение
        0  0xFE 
        Ответ:
        Если  прибор  не  находится  в  режиме  ответ  аналогичен  ответу   команды
        SpprCmdGetVersion 
        Если прибор в режиме подсчета числа импульсов
        Байт  Значение
        0  Теку щий режим измерения 0x00 – 0x03 
        1  BYTE State 
        2 – 4  Тимп 1 
        5 – 7  N имп 1 
        8 – 10  Тимп 2 
        11 – 13  N имп 2 
        14 – 16  Тимп 3 
        17 – 19  N имп 3 
        20 – 22  Тимп 4 
        23 – 25  N имп 4 
        26 -28  T изм
        29  Сумма
        State – байт состояния, аналогичен команде SpprCmdGetVersion 
        T изм  – теку щее время измерения (0 . . 0xFFFFFF)/4096 c 
        Тимп – Интервал между  последним измеренным импульсом (0 .. 0xFFFFFF)/4096 c 
        Nимп – Количество подсчитываемых перепадов посту пивших на вход
        Если прибор в режиме генерации импу льсов
        Байт  Значение
        0  Теку щий режим 0x04 
        1  BYTE State 
        2 – 4  N имп 1 
        5 – 7  N имп 2 
        8 – 10  N имп 3 
        11 – 13  N имп 4 
        14  Сумма
        Nимп – Оставшееся количество импу льсов
    """
    message = b'\xFE'
    #print("Посылаю:", message)
    ser.write(message)         
    data = ser.readline()
    #print("Получаю:", bytes(data), len(data))
    if len(data) == 4:
        string = "Прибор не в режиме"
        return string
    #print(binascii.hexlify(bytes(data)).decode('ASCII'))
    bite0 = int.from_bytes(bytes(data[0]), byteorder='little')       #режим
    bite1 = binascii.hexlify(bytes(data[1])).decode('ASCII')         #байт-состояния
    bite24 = int.from_bytes(data[2:5], byteorder='little')
    time1 = bite24/4096
    string = (format(time1, '6.2f').replace('.', ',')) + '|'  #ВРЕМЯ
    bite57 = int.from_bytes(data[5:8], byteorder='little')    #Импульсы тактов
    bite810 =int.from_bytes(data[8:11], byteorder='little')   #импульсы с Входа2(МФ)
    bite1113 = int.from_bytes(data[11:14], byteorder='little')
    bite1416 = int.from_bytes(data[16:17], byteorder='little')
    bite1719 = int.from_bytes(data[17:20], byteorder='little')
    bite2022 = int.from_bytes(data[20:23], byteorder='little')
    bite2325 = int.from_bytes(data[23:26], byteorder='little')
    bite2628 = int.from_bytes(data[26:29], byteorder='little')
    bite29 = int.from_bytes(bytes(data[29]), byteorder='little')


    if time1 == 0: time1=0.001    
    F=bite810/time1
    FMAX=1000    
    GMAX=3.75
    G=F*GMAX/FMAX
    V=G/3.6*time1
    G1=V/time1*3.6
    string += (format(G1, '6.4f').replace('.', ',')) + '|'   #РАСХОД
    string += (format(V, '6.4f').replace('.', ',')) + ' '   #ОБЪЕМ
    return string

def SpprCmdGetQuality():
    ser.write(b'\xFC')         
    data = ser.readline()    
    string=data
    string = binascii.hexlify(data).decode('ASCII')
    bite0 = string[0:2]
    bite1_2 = int.from_bytes(data[1:3], byteorder='little')
    bite3_4 = int.from_bytes(data[3:5], byteorder='little')
    bite5_6 = int.from_bytes(data[5:7], byteorder='little')
    bite7_8 = int.from_bytes(data[7:9], byteorder='little')

    time1 = bite1_2
    print(format(bite1_2, '6.2f').replace('.', ','), end = ' ')
    print(format(bite3_4, '6.2f').replace('.', ','), end = ' ')
    print(format(bite5_6, '6.2f').replace('.', ','), end = ' ')
    print(format(bite7_8, '6.2f').replace('.', ','))
    
def SpprGetFlashVersion():
    pass  #Не реализовано


def SpprSelfTest():
    pass  #Не реализовано


def ControlSumm(message):
    summ=0
    for byte in message[1:]:
        summ += byte
    a = summ.to_bytes(3, byteorder='little')
    return (a[0:1])

def preparation():
    print(SpprCmdLaserOff())
    print(SpprCmdLaserOn())
    time.sleep(2)
    print(SpprCmdGetAndReset())
    print('Расходомер готов')

def mesuring():    
    SpprCmdSS2Measure()
    oldget = 1
    while True:
        get = Get()
        if get != '  0,00 0,0000 0,0000 ':#уже не работает
            if get == oldget:
                print(GetAndRest(), 'finish')
                break
            print(get)
            sys.stdout.write("\033[F") # Cursor up one line
            sys.stdout.write("\033[K")
        oldget = get   
        time.sleep(0.1)
    SpprCmdLaserOff()

if __name__ == "__main__":
    preparation()
    mesuring()


