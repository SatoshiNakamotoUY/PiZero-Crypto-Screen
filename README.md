# Creditos

Este proyecto es un fork del proyecto de shadowandy
https://github.com/shadowandy
que a su vez es un fork del proyecto de dr-mod's zero-btc-screen
https://github.com/dr-mod/zero-btc-screen

# Mejoras realizadas por SatoshiUY
* Se agrega la pantalla epd2in3bv4 (rojo, blanco, negro).
  Está configurado en blanco y negro

# Mejoras realizadas por shadowandy
* Se usa la api de CoinGecko
* Alternancia entre varias monedas
* Se alinea el texto contra la derecha
* Se puede cambiar la moneda de base en la que se muestra el precio (usd, eur, etc)

# Zero Crypto Screen - Original - Traduccion por SatoshiUY

Precio del Bitcoin u otra moneda para Raspberry PiZero

![display](display_1.jpeg)
![display](display_2.jpeg)

## Equipo

### Platforma

* Raspberry Pi Zero W (o cualquier otra Raspberry Pi)

### Pantallas

* Waveshare eInk displays: epd2in13v2, epd2in13bv3, epd2in3bv4 (agregada por SatoshiUY)
* inkyWhat (Red, Black, White)
* Virtual (imagen)

## Instalación

1. Prender SPI via `sudo raspi-config`
    ```
    Interfacing Options -> SPI
   ```
2. Instalar dependencias
    ```
    sudo apt update
    sudo apt-get install python3-pip python3-pil python3-numpy
    pip3 install RPi.GPIO spidev
    ```

3. Instalar drivers de la pantalla
    1. Pantalla Waveshare
    ```
    git clone https://github.com/waveshare/e-Paper.git ~/e-Paper
    pip3 install ~/e-Paper/RaspberryPi_JetsonNano/python/
    ```
   para más información referise a: https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT
    2. Inky wHAT display
    ```
    pip3 install inky[rpi]
    ```
4. Descargar el codigo de  PiZero Crypto Screen (nombre original de dr mod: zero-btc-screen)
    ```
    git clone https://github.com/SatoshiNakamotoUY/PiZero-Crypto-Screen.git ~/Pantalla

5. Modificar las lineas 11 y 12 del archivo main.py
   
   En estas líneas cambiar "epd2in13b_V4" por la correspondiente a su pantalla
   
      11  from waveshare_epd import epd2in13b_V4
       
      12  epd = epd2in13b_V4.EPD()
   
5. Inicializar
    ```
    python3 ~/PiZero-Crypo-Screen/main.py
    ```

## Configuración de la Pantalla

La aplicación soporta multiples pantallas tipo e-screen, y adicionalmente pantalla tipo "imágen"

Para configurar la pantalla a usar se debe modificar el archivo configuration.cfg. En el siguiente ejemplo se usa la pantalla epd2in13bv4. 

Los valores para las monedas (cryptocurrencies) se deben ingresar con el formato:

  <Cryptomoneda 1:abreviación moneda 1>, <Cryptomoneda 2:abreviación moneda 2>, etc.

El ejemplo debajo es para dos monedas, bitcoin y cardano. Ver mas detalles en https://www.coingecko.com/.

La configuración de los dias (days) determina el intervalo entre velas, admite valers 1, 7 o 14. 

El valor 1 represent 30minutos, los valore 7 y 14 dan velas de 4 horas.

El campo "refresh_interval_minutes" define cada cuantos minutos se va a refrescar la imágen.

```cfg
[base]
console_logs             : false
#logs_file               : /tmp/zero-crypto-screen.log
dummy_data               : false
refresh_interval_minutes : 6
days                     : 1
cryptocurrencies         : bitcoin:BTC,ethereum:ETH,solana:SOL,wonderland:TIME
currency                 : usd

# Pantallas Habilitadas
screens : [
#    epd2in13v2
#    epd2in13bv3
    epd2in13bv4
#    picture
#    inkyWhatRBW
  ]

# Configuración por pantallas
# Esto no produce ningun efecto si no está habilitado arriba en "Pantallas Habilitadas"
# "candle" muestra grafico de velas y "line" una línea
[epd2in13v2]
mode : candle

[epd2in13bv3]
mode  : line

[epd2in13bv4]
mode  : candle

[picture]
filename : /home/pi/output.png

[inkyWhatRBW]
mode : candle
```

## Configuració de Inicio automático

  1. Crear un nuevo archivo de configuracion del servicio
       ```
        sudo nano /etc/systemd/system/crypto-screen.service
        ```
  2. Copiar y pegar lo siguiente en el archivo de configuración de servicio, cambiar los ajustes para que conincida con su entorno 
    
        ```
        [Unit]
        Description=zero-crypto-screen
        After=network.target
 
        [Service]
        ExecStart=/usr/bin/python3 -u main.py
        WorkingDirectory=/home/pi/zero-crypto-screen
        StandardOutput=inherit
        StandardError=inherit
        Restart=always
        User=pi
 
        [Install]
        WantedBy=multi-user.target
        ```
  3. Habilitar el revicio para que se inicie al prender la Raspberry Pi
       ```
        sudo systemctl enable crypto-screen.service
       ```
  4. Comenzar y disfrutar!
       ```
        sudo systemctl start crypto-screen.service
       ```
       En caso de problemas se puede utilizar el serviccio de logging de este programa (mencionado debajo)
     
       Alternativamente se puede chequear si existe alguna salida en el logging del sistema.
       ```
        sudo journalctl -f -u crypto-screen.service
       ```
