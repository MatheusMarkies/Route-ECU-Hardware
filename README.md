# DOCUMENTAÇÃO TÉCNICA
## Unidade de Controle Eletrônico (ECU) Automotiva

[![ECU-Render](https://i.ibb.co/vrg7kG9/ECU-Render.png)](https://i.ibb.co/vrg7kG9/ECU-Render.png)

---

**Versão:** 1.5  
**Data:** Setembro 2025  
**Classificação:** Documento Técnico  
**Status:** Em Desenvolvimento  

[Route ECU Firmware](https://github.com/MatheusMarkies/Route-ECU-Firmware)

---

## 1. INFORMAÇÕES GERAIS

### 1.1 Aplicação
ECU destinada ao controle de motores de combustão interna com sistema de injeção eletrônica, com capacidade para:
- 4 cilindros/injetores
- Comunicação CAN bus
- Comunicação Serial
- Armazenamento de dados e mapas

---

## 2. ESPECIFICAÇÕES TÉCNICAS

### 2.1 Especificações Elétricas

| Parâmetro | Mínimo | Típico | Máximo | Unidade |
|-----------|---------|---------|---------|----------|
| Tensão de Entrada | 9 | 12 | 18.81 | V |
| Corrente (Standby) | - | A Determinar | A Determinar | mA |
| Corrente (Operação) | - | A Determinar | A Determinar | mA |
| Corrente por Injetor | - | A Determinar | A Determinar | A |
| Tensão Lógica (MCU) | - | 3.3 | - | V |
| Tensão Periféricos | - | 5.0 | - | V |

Sendo a tensão de perifericos uma tensão derivada do regulador principal, porem com filtros extras para a alimentação de sensores.

### 2.2 Especificações de Gerais

| Característica | Valor | Unidade |
|----------------|--------|----------|
| Frequência MCU | 100 | MHz |
| Resolução de Tempo | A Determinar | µs |
| Taxa CAN Bus | A Determinar | kbps |
| Canais de Injeção | 4 | - |
| Canais de Ignição | 4 | - |
| Memória Flash | TBD | KB |
| Memória RAM | TBD | KB |
---

## 3. ARQUITETURA DO HARDWARE

### 3.1 Microcontrolador Principal
- **Família**: STM32H743VIT6 (ARM Cortex-M)
- **Clock Principal**: 16MHz (cristal externo) x2
- **Clock RTC**: 32.768kHz
- **Interfaces**: SPI, I2C, UART, CAN, GPIO

### 3.2 Sistema de Clock
```
Oscilador Principal (16MHz) ──▶ PLL ──▶ System Clock (100MHz)
                                  │
RTC Crystal (32.768kHz) ─────────┴──▶ RTC Clock
```

### 3.3 Mapa de Memória
- **Flash**: Código do programa
- **FRAM**: Dados grandes de acesso rapido
- **SD Card**: Log de dados e Mapas

### 3.4 Sistema de Injeção
- **Atuador**: TIP142
- **Driver**: LM1949 (Modo peak-and-hold)
- **Indicador**: LEDs indicadores individuais para cada canal de injeção

#### 3.4.2 Canais de Injeção
| Canal |
|-------|
| INJ 1 |
| INJ 2 |
| INJ 3 |
| INJ 4 |

[![INJECTOR](https://i.ibb.co/99wgFJhB/INJECTOR.png)](https://i.ibb.co/99wgFJhB/INJECTOR.png)

### 3.5 Sistema de Ignição
- **Atuador**: ISL9V5036P3-F085
- **Driver**: TC4424CPA (Controla duas ignições)
- **Corrente de Pico**: 3A

#### 3.5.2 Canais de Injeção
| Canal |
|------|
| IG 1 |
| IG 2 |
| IG 3 |
| IG 4 |

[![IGNITION](https://i.ibb.co/ycDnkN8f/IGNITION.png)](https://i.ibb.co/ycDnkN8f/IGNITION.png)

### 3.6 Sensores de Posição
- **CKP**: Posição do Virabrequim
- **CMP**: Posição do Comando de Válvulas (Se aplicavel)
- **Tipos de Entradas**: Relutância Variável e Hall
- **Condicionador de Sinal VR**: MAX9924

[![CKP](https://i.ibb.co/mFYfzqwf/CKP.png)](https://i.ibb.co/mFYfzqwf/CKP.png)

### 3.7 Sensor MAP
- **Sensor**: MPXA4250AC6U
- **Faixa de Trabalho**: 20 a 250 kPa
- **Relação de Calculo**: VOUT = VCC x (P × 0.004 – 0.04)

[![MAP](https://i.ibb.co/p6Ym96gr/MAP.png)](https://i.ibb.co/p6Ym96gr/MAP.png)

### 3.8 Sensor LAMBDA
- **Controlador**: CJ125
- **Controle de Aquecimento**: Sim
- **Sensores**: LSU4.X

[![LAMBDA](https://i.ibb.co/d0LBV45P/LAMBDA.png)](https://i.ibb.co/d0LBV45P/LAMBDA.png)

### 3.9 Sensores Analogicos
- **Conversor das Entradas (map)**: Tensão de Entrada no MCU = 3.205V Quando V_Sensor = 5V

#### 3.9.2 Sensores de Baixa Potencia

| Entrada | Tensão Maxima | TVS | Tipo de Entrada |
|----------------|--------|----------|----------|
| Entrada 1 | 5V | Sim | Analogico |
| Entrada 2 | 5V | Sim | Analogico |
| Entrada 3 | 5V | Sim | Analogico |
| Entrada 4 | 5V | Sim | Analogico |
| Entrada 5 | 5V | Sim | Analogico |
| Entrada 6 | 5V | Sim | Analogico |
| Entrada 7 | 5V | Sim | Analogico |
| Entrada 8 | 5V | Sim | Analogico |
| Entrada 9 | 5V | Sim | Analogico |
| Entrada 10 | 5V | Sim | Analogico |
| Entrada 11 | 5V | Sim | Analogico |
| Entrada 12 | 5V | Sim | Analogico |

[![LOW-POWER-SENSOR](https://i.ibb.co/27B8pFJF/LOW-POWER-SENSOR.png)](https://i.ibb.co/27B8pFJF/LOW-POWER-SENSOR.png)

#### 3.9.3 Sensores de Alta Potencia

| Entrada | Tensão Maxima | Optoacoplada | Tipo de Entrada |
|----------------|--------|----------|----------|
| Entrada 1 | 12V | Sim | Analogico |
| Entrada 2 | 12V | Sim | Analogico |
| Entrada 3 | 12V | Sim | Analogico |
| Entrada 4 | 12V | Sim | Analogico |

[![HIGH-POWER-SENSORS](https://i.ibb.co/LzSqFQfp/HIGH-POWER-SENSORS.png)](https://i.ibb.co/LzSqFQfp/HIGH-POWER-SENSORS.png)

### 3.10 Saidas

| Entrada | Tensão Maxima | PWM |
|----------------|--------|----------|
| Saida 1 | 5V | Sim |
| Saida 2 | 5V | Sim |
| Saida 3 | 5V | Sim |
| Saida 4 | 5V | Sim |

[![PWM](https://i.ibb.co/xtqXdg2R/PWM.png)](https://i.ibb.co/xtqXdg2R/PWM.png)

---

## 4. SUBSISTEMAS

### 4.1 Sistema de Alimentação

#### 4.1.1 Conversão DC-DC
- **Entrada**: 12V automotiva (9 a 18.81V)
- **Saídas**: 
  - 5V 2A (periféricos)
  - 3.3V 500mA (MCU e lógica)

## 5. INTERFACES E CONECTORES

### 5.1 Conector Principal (J1)
- **Tipo**: TE 796739-2
- **Função**: Interface principal do veículo
- **Sinais**: Alimentação, CAN, sinais de controle

### 5.2 Headers de Programação

| Designador | Tipo | Função |
|------------|------|---------|
| J2 | TSM-104-01-L-MT | Debug/SWD |

### 5.3 Interface SD Card (J9)
- **Conector**: 5007620483
- **Protocolo**: SPI
- **Tensão**: 3.3V
- **Capacidade**: Até 32GB

### 5.4 Pinagem do Conector Principal

| Pino | Sinal |
|-----|---------------|
| **A1** | INJ 1          |
| **A2** | INJ 4          |
| **A3** | INJ 3          |
| **A4** | INJ 2          |
| **B1** | Sensor_In_1    |
| **B2** | CANL           |
| **B3** | CANH           |
| **B4** | PWM_MCU_OUT_4  |
| **C1** | Sensor_In_2    |
| **C2** | 5V Sensor      |
| **C3** | 3.3V           |
| **C4** | PWM_MCU_OUT_3  |
| **D1** | Sensor_In_3    |
| **D2** | CMP_IN_1       |
| **D3** | CMP_HALL_IN    |
| **D4** | PWM_MCU_OUT_2  |
| **E1** | Sensor_In_4    |
| **E2** | CMP_IN_2       |
| **E3** | GND            |
| **E4** | PWM_MCU_OUT    |
| **F1** | Sensor_In_5    |
| **F2** | CKP_IN         |
| **F3** | CKP_HALL_IN    |
| **F4** | CJ125_UP       |
| **G1** | Sensor_In_6    |
| **G2** | CKP_IN_1       |
| **G3** | CJ125_IA       |
| **G4** | CJ125_UA       |
| **H1** | Sensor_In_7    |
| **H2** | Sensor_In_10   |
| **H3** | CJ125_US       |
| **H4** | CJ125_IP       |
| **J1** | Sensor_In_8    |
| **J2** | Sensor_In_11   |
| **J3** | CJ125_VM       |
| **J4** | CJ125_UN       |
| **K1** | Sensor_In_9    |
| **K2** | Sensor_In_12   |
| **K3** | MAP_OUT        |
| **K4** | Sensor_OPT_3   |
| **L1** | Sensor_OPT_2   |
| **L2** | Sensor_OPT_1   |
| **L3** | Sensor_OPT_0   |
| **L4** | Heater OUT     |
| **M1** | Ig 1           |
| **M2** | Ig 2           |
| **M3** | Ig 3           |
| **M4** | Ig 4           |
