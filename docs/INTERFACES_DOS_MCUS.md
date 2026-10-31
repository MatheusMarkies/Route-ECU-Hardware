# Pontos para os MCUs — ECTU

Data: 15/10/2026. Autor do projeto: Matheus Markies.

Foram colocados 71 pontos em `D:/Route-ECU-Hardware/MCU.SchDoc`, agrupados por função. Cada ponto tem uma identificação global de rede, um fio curto com ponta livre e uma anotação separada do periférico sugerido. Conecte a ponta livre ao destino indicado. A anotação não faz parte do nome elétrico da rede. Após o pedido de CAN no auxiliar G071, CAN_TX/RX passaram a indicar o controlador CAN externo; esses dois pontos não devem ser ligados diretamente ao G071. Permanecem 69 pontos para MCUs e dois para a interface do controlador CAN ainda ausente.

As recomendações são uma primeira reserva de recursos. Não constituem uma distribuição física de pinos validada: conferir funções alternativas, encapsulamentos H743 LQFP100 e G071 LQFP64, conflitos e requisitos de DMA no CubeMX antes de fechar o pinout. O auxiliar escolhido é o STM32G071RBT6; o símbolo e o circuito de suporte ainda não foram inseridos.

## Critérios de distribuição

- H743: sincronismo CKP/CMP, injeção, ignição, ETC, aquisição crítica e controle de atuadores.
- Auxiliar STM32G071RBT6: quatro rodas, neutro, aquisição térmica/EGT, CAN e telemetria. As recomendações foram colocadas ao lado dos sinais; alimentação, símbolo e modificações dos barramentos ainda precisam ser implementados. A seleção está sendo reavaliada a pedido do usuário para obter CAN FD integrado.
- Rodas no G071: TIM2_CH1 a TIM2_CH4, Input Capture de 32 bits. O ADC interno do G071 é de 12 bits; o ADS1115 continua sendo lido por I²C. SPI e I²C são as interfaces digitais de EGT/ADCs, sem exigir um canal ADC interno para cada sensor externo.
- CKP/CMP: TIM2, Input Capture de 32 bits. Os dois canais usam o mesmo contador.
- Injeção: TIM5, quatro canais de Output Compare de 32 bits. Ignição: TIM1, quatro canais de Output Compare de 16 bits. Pulsos/dwell exigem agendamento de bordas e tratamento correto de overflow; a indicação não significa PWM periódico de frequência fixa.
- PWM1–4: TIM4. Os canais do mesmo timer compartilham período e prescaler; se as frequências precisarem ser independentes, redistribuir timers.
- ETC: a conexão atual MODE=GND do DRV8873H seleciona PH/EN. EN recebe PWM; PH recebe direção. SLEEP e FAULT são GPIO.
- UART1_TX/RX permanecem sugeridos para USART1 do H743. UART2_TX/RX foram sugeridos para USART3 do G071 para telemetria; a indicação não obriga o uso de USART2 pelo nome da rede. Reservar USART1 do G071 e um USART livre do H743 para um enlace dedicado entre MCUs. O enlace ainda não tem redes implementadas.
- Reservar PA11/PA12 para USB FS e PA13/PA14 para SWD. SWO/JTDI são opcionais. Uma opção de TIM2_CH1/CH2 em PA15/PB3 conflita com JTDI/SWO; a escolha final deve resolver isso.
- ADC single-ended de 16 bits é uma configuração nominal do ADC do H743; não representa 16 bits de exatidão ou ENOB.

## Barramentos de aquisição

ADS8688 U5/U6 e MAX31856 U34 compartilham SPI_ADC no circuito atual. Devem ter o mesmo master e CS independentes; se o EGT migrar para o auxiliar, separar fisicamente esse SPI ou manter um único master e transmitir os resultados entre MCUs. Não conectar dois masters simultaneamente ao barramento sem uma arquitetura própria de arbitragem.

I2C1 atende a FRAM e o ADS1115 via PCA9306. A recomendação passou a ser G071 como único master desse barramento, portanto a FRAM também fica acessível por ele; se a FRAM precisar continuar no H743, separar os barramentos antes da atribuição de pinos. Os pontos do lado do MCU são I2C1_SCL/SDA; TEMP_ADC_SCL/SDA são o lado de 5 V do conversor de nível. I2C2 do G071 controla o ADG729 que seleciona os termopares. Migrar um dispositivo não significa que o mesmo barramento possa ser ligado livremente a dois MCUs.

Reservas propostas: SPI1 do G071 para MAX31856 após separar o SPI_ADC; SPI2 para um controlador CAN externo, com GPIO para CS e entrada EXTI para INT; USART1 para o enlace com o H743. São anotações de planejamento, ainda sem novos circuitos ou redes implementados. Um exemplo de controlador CAN FD externo é MCP2518FD; ele deve ser conectado ao MCP2562FD existente. O G071 não contém controlador CAN integrado. Se o MCU auxiliar for trocado por uma variante com FDCAN, essa reserva de controlador SPI deixa de ser necessária e as anotações precisam ser revisadas.

TPS, APP, pressões, entradas extras, IAT/CHT/ECT/EOT e CJ125_UA/UR chegam pelos ADCs externos; não precisam de um pino ADC interno para cada sensor. MAP_INT_ADC e VBAT_MCU_ADC são os pontos analógicos diretos apresentados.

## Pendências registradas na folha

1. ADC1_ALERT e ADC2_ALERT estão nos pinos 35 DNC de U6/U5. O datasheet determina que esses pinos permaneçam sem conexão. Não foram criados pontos para ligá-los ao MCU; remover as conexões incorretas na revisão desses blocos.
2. RST/PD (pino 2) e DAISY (pino 3) de U5/U6 ainda precisam de definição. RST/PD pode receber pull-up ou controle por GPIO conforme a arquitetura; DAISY depende do modo de conexão SPI. Não foram inventadas redes como se essas ligações já existissem.
3. TEMP_ADC_ALERT tem pull-up em V5V0_SENS via R106. Adequar a 3,3 V ou escolher uma entrada comprovadamente tolerante a 5 V nas condições de uso antes de conectá-lo. A anotação na folha chama atenção para os 5 V.
4. IPROPI1/IPROPI2 e DISABLE do DRV8873 ainda não têm definição de interface. IPROPI requer circuito de conversão de corrente em tensão/condicionamento antes de um ADC; DISABLE precisa de estado de hardware ou GPIO definido. Estão como notas de pendência, não como conexões prontas.
5. PWM5/6 não têm estágio externo nesta revisão e não foram apresentados como saídas implementadas.
6. A exportação atual mostra NRST de U1 como NetU1_14, separado de MCU_RESET_N. Conferir o alinhamento/ligação do ponto existente no símbolo ao atribuir os pinos. Esta tarefa não refez essa ligação.
7. VBAT_MCU_ADC é o nome existente, mas o divisor na folha MCU está alimentado por V5V0_SENS. Confirmar se a intenção é monitorar 5 V ou bateria antes da calibração. O nome foi preservado.

Alimentação, desacoplamentos e osciladores já presentes foram preservados. Alimentação, reset e programação do G071 precisam ser adicionados quando o símbolo for inserido; não foram confundidos com interfaces já implementadas. Para o enlace entre MCUs, reservar UART ou SPI; o G071 não possui controlador CAN integrado.

## Lista de pontos

### H7 / ENTRADAS ANALÓGICAS DIRETAS

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `VBAT_MCU_ADC` | ADC single-ended / 16 bits | H743 | MCU.SchDoc |
| `MAP_INT_ADC` | ADC single-ended / 16 bits | H743 | PressureAirflow.SchDoc |

### H7 / SINCRONISMO DO MOTOR

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `CKP_MCU` | TIM2_CH1 / IC 32 bits | H743 | CrankAndCam.SchDoc |
| `CMP_MCU` | TIM2_CH2 / IC 32 bits | H743 | CrankAndCam.SchDoc |

### H7 / INJETORES

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `INJ1_CMD` | TIM5_CH1 / OC 32 bits | H743 | SparkAndFuel.SchDoc |
| `INJ2_CMD` | TIM5_CH2 / OC 32 bits | H743 | SparkAndFuel.SchDoc |
| `INJ3_CMD` | TIM5_CH3 / OC 32 bits | H743 | SparkAndFuel.SchDoc |
| `INJ4_CMD` | TIM5_CH4 / OC 32 bits | H743 | SparkAndFuel.SchDoc |

### H7 / SMART COILS

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `IGN1_CMD` | TIM1_CH1 / OC 16 bits | H743 | SparkAndFuel.SchDoc |
| `IGN2_CMD` | TIM1_CH2 / OC 16 bits | H743 | SparkAndFuel.SchDoc |
| `IGN3_CMD` | TIM1_CH3 / OC 16 bits | H743 | SparkAndFuel.SchDoc |
| `IGN4_CMD` | TIM1_CH4 / OC 16 bits | H743 | SparkAndFuel.SchDoc |

### H7 / SAÍDAS PWM

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `PWM1_CMD` | TIM4_CH1 / PWM 16 bits | H743 | ExternalInterface.SchDoc |
| `PWM2_CMD` | TIM4_CH2 / PWM 16 bits | H743 | ExternalInterface.SchDoc |
| `PWM3_CMD` | TIM4_CH3 / PWM 16 bits | H743 | ExternalInterface.SchDoc |
| `PWM4_CMD` | TIM4_CH4 / PWM 16 bits | H743 | ExternalInterface.SchDoc |

### H7 / ETC - MODO PH/EN

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `ETC_EN_IN1` | TIM12_CH1 / PWM 16 bits | H743 | ETC.SchDoc |
| `ETC_PH_IN2` | GPIO OUT / direção | H743 | ETC.SchDoc |
| `ETC_SLEEP_N` | GPIO OUT / enable | H743 | ETC.SchDoc |
| `ETC_FAULT_N` | GPIO IN / EXTI | H743 | ETC.SchDoc |

### H7 / ATUADORES AUXILIARES

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `IAC_CMD` | TIM13_CH1 / PWM 16 bits | H743 | LowSideSwitches.SchDoc |
| `LSU_HEATER_PWM` | TIM14_CH1 / PWM 16 bits | H743 | LambdaWidebandController.SchDoc |
| `RELAY1_CMD` | GPIO OUT | H743 | LowSideSwitches.SchDoc |
| `RELAY2_CMD` | GPIO OUT | H743 | LowSideSwitches.SchDoc |
| `IAC_STATUS_MCU` | GPIO IN / EXTI | H743 | LowSideSwitches.SchDoc |

### ESTADOS / H7 OU G071

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `IGN_SW_N` | H7 GPIO IN / EXTI | H743 | ExternalInterface.SchDoc |
| `NEUTRAL_SW_N` | G071 GPIO IN / EXTI | STM32G071RBT6 | ExternalInterface.SchDoc |

### H7 / ADCs EXTERNOS + EGT

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `SPI_ADC_SCK` | SPI1_SCK / master | H743 (barramento compartilhado) | ExternalInterface.SchDoc;TemperatureSensors.SchDoc |
| `SPI_ADC_MOSI` | SPI1_MOSI / master | H743 (barramento compartilhado) | ExternalInterface.SchDoc;TemperatureSensors.SchDoc |
| `SPI_ADC_MISO` | SPI1_MISO / master | H743 (barramento compartilhado) | ExternalInterface.SchDoc;TemperatureSensors.SchDoc |
| `ADC1_CS_N` | GPIO OUT / CS | H743 (barramento compartilhado) | ExternalInterface.SchDoc |
| `ADC2_CS_N` | GPIO OUT / CS | H743 (barramento compartilhado) | ExternalInterface.SchDoc |

### H7 / CJ125 - LADO 3V3

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `CJ125_SCK_MCU` | SPI2_SCK / master | H743 | LambdaWidebandController.SchDoc |
| `CJ125_MOSI_MCU` | SPI2_MOSI / master | H743 | LambdaWidebandController.SchDoc |
| `CJ125_MISO_MCU` | SPI2_MISO / master | H743 | LambdaWidebandController.SchDoc |
| `CJ125_CS_MCU_N` | GPIO OUT / CS | H743 | LambdaWidebandController.SchDoc |

### G071 / I²C TEMPERATURAS + FRAM

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `I2C1_SCL` | G071 I2C1_SCL / ver FRAM | STM32G071RBT6; barramento inclui FRAM | CommunicationInterfaces.SchDoc;TemperatureSensors.SchDoc |
| `I2C1_SDA` | G071 I2C1_SDA / ver FRAM | STM32G071RBT6; barramento inclui FRAM | CommunicationInterfaces.SchDoc;TemperatureSensors.SchDoc |
| `TEMP_ADC_ALERT` | G071 GPIO/EXTI / ver 5 V | STM32G071RBT6 | TemperatureSensors.SchDoc |

### G071 / I²C MUX DOS TERMOPARES

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `I2C2_SCL` | G071 I2C2_SCL | STM32G071RBT6 | CommunicationInterfaces.SchDoc;TemperatureSensors.SchDoc |
| `I2C2_SDA` | G071 I2C2_SDA | STM32G071RBT6 | CommunicationInterfaces.SchDoc;TemperatureSensors.SchDoc |

### G071 / EGT - SEPARAR SPI

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `EGT_CS_N` | G071 GPIO OUT / SPI1 CS | STM32G071RBT6; separar SPI_ADC | TemperatureSensors.SchDoc |
| `EGT_DRDY_N` | G071 GPIO IN / EXTI | STM32G071RBT6 | TemperatureSensors.SchDoc |
| `EGT_FAULT_N` | G071 GPIO IN / EXTI | STM32G071RBT6 | TemperatureSensors.SchDoc |

### G071 / VELOCIDADE DAS RODAS

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `WHEEL_FL_MCU` | G071 TIM2_CH1 / IC 32 bits | STM32G071RBT6 | CrankAndCam.SchDoc |
| `WHEEL_FR_MCU` | G071 TIM2_CH2 / IC 32 bits | STM32G071RBT6 | CrankAndCam.SchDoc |
| `WHEEL_RL_MCU` | G071 TIM2_CH3 / IC 32 bits | STM32G071RBT6 | CrankAndCam.SchDoc |
| `WHEEL_RR_MCU` | G071 TIM2_CH4 / IC 32 bits | STM32G071RBT6 | CrankAndCam.SchDoc |

### NÍVEL DAS SAÍDAS PWM

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `PWM1_LEVEL_SEL` | GPIO OUT / seletor | H743 ou G071 | ExternalInterface.SchDoc |
| `PWM2_LEVEL_SEL` | GPIO OUT / seletor | H743 ou G071 | ExternalInterface.SchDoc |
| `PWM3_LEVEL_SEL` | GPIO OUT / seletor | H743 ou G071 | ExternalInterface.SchDoc |
| `PWM4_LEVEL_SEL` | GPIO OUT / seletor | H743 ou G071 | ExternalInterface.SchDoc |

### G071 / CAN EXIGE CONTROLADOR SPI

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `CAN_TX` | TXCAN / controlador externo | Controlador CAN externo; não ligar diretamente ao G071 | CommunicationInterfaces.SchDoc |
| `CAN_RX` | RXCAN / controlador externo | Controlador CAN externo; não ligar diretamente ao G071 | CommunicationInterfaces.SchDoc |

### UART / SERVIÇO H7 E TELEMETRIA G071

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `UART1_TX` | H7 USART1_TX | H743 | CommunicationInterfaces.SchDoc |
| `UART1_RX` | H7 USART1_RX | H743 | CommunicationInterfaces.SchDoc |
| `UART2_TX` | G071 USART3_TX / telemetria | STM32G071RBT6 | CommunicationInterfaces.SchDoc |
| `UART2_RX` | G071 USART3_RX / telemetria | STM32G071RBT6 | CommunicationInterfaces.SchDoc |

### USB / LADO DO MCU

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `USB_DM_MCU` | USB_OTG_FS_DM / PA11 | H743 | CommunicationInterfaces.SchDoc |
| `USB_DP_MCU` | USB_OTG_FS_DP / PA12 | H743 | CommunicationInterfaces.SchDoc |

### MICROSD / BARRAMENTO 4 BITS

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `SD_CLK` | SDMMC1_CK | H743 | CommunicationInterfaces.SchDoc |
| `SD_CMD` | SDMMC1_CMD | H743 | CommunicationInterfaces.SchDoc |
| `SD_D0` | SDMMC1_D0 | H743 | CommunicationInterfaces.SchDoc |
| `SD_D1` | SDMMC1_D1 | H743 | CommunicationInterfaces.SchDoc |
| `SD_D2` | SDMMC1_D2 | H743 | CommunicationInterfaces.SchDoc |
| `SD_D3` | SDMMC1_D3 | H743 | CommunicationInterfaces.SchDoc |

### PROGRAMAÇÃO / DEPURAÇÃO

| Rede | Recomendação | MCU / propriedade do barramento | Origem |
|---|---|---|---|
| `SWDIO` | SWDIO / PA13 | H743 | CommunicationInterfaces.SchDoc |
| `SWCLK` | SWCLK / PA14 | H743 | CommunicationInterfaces.SchDoc |
| `MCU_RESET_N` | NRST / pino dedicado | H743 | CommunicationInterfaces.SchDoc;MCU.SchDoc |
| `SWO` | TRACE_SWO / opcional | H743 | CommunicationInterfaces.SchDoc |
| `JTDI` | JTDI / só JTAG opcional | H743 | CommunicationInterfaces.SchDoc |

## Verificação e arquivos

- Edição feita pelo servidor nativo de esquemáticos do Altium, com prévia em cópia separada.
- 71 identificações de rede, 71 fios e 119 textos adicionados. Nenhum registro existente do circuito foi removido ou modificado na comparação semântica.
- 1.255 conexões de pinos exportadas antes e depois: idênticas, incluindo nomes de redes. Os pontos continuam sem atribuição aos GPIOs.
- As outras 11 folhas, a PCB e o arquivo do projeto permaneceram byte a byte iguais à cópia de segurança feita após salvar as edições do usuário.
- O projeto continua com erros ERC preexistentes: a compilação retornou FALSE e o relatório atingiu 1.000 ocorrências tanto antes como depois. A comparação de conectividade não equivale à aprovação do circuito pelo ERC.
- Seleção posterior do STM32G071RBT6: 11 anotações foram atualizadas pelo Altium, incluindo o timer das rodas e a resolução do ADC. Essa atualização modifica somente textos explicativos; a comparação semântica dos demais registros e das outras folhas confirma a preservação do circuito.
- Revisão das responsabilidades e CAN no G071: 31 anotações atualizadas e quatro notas de reserva adicionadas. Os demais registros, inclusive todas as conexões elétricas, foram preservados; apenas MCU.SchDoc mudou. Evidência em `_codex_mcu/g071_distribution_verification.json`.

Backup: `D:\Route-ECU-Hardware\_codex_mcu\backup_live_20261015_103329`.

Evidências: `D:/Route-ECU-Hardware/_codex_mcu/verification.json`, `points.csv` e exportações `topology_mcu_before.tsv` / `topology_mcu_after.tsv` em `_codex_naming`.

## Referências de componentes

- [ST — STM32H743, datasheet DS12110 Rev. 11](https://www.st.com/resource/en/datasheet/stm32h743xi.pdf): timers, ADC e funções alternativas.
- [ST — STM32G071, datasheet DS12232](https://www.st.com/resource/en/datasheet/stm32g071rb.pdf): TIM2 de 32 bits, quatro canais de captura, ADC nativo de 12 bits e interfaces disponíveis.
- [TI — ADS8688, datasheet](https://www.ti.com/lit/ds/symlink/ads8688.pdf): pino 35 DNC, DAISY, RST/PD e SPI.
- [TI — DRV8873-Q1, datasheet](https://www.ti.com/lit/ds/symlink/drv8873-q1.pdf): configuração de MODE e controle PH/EN.
- [Microchip — MCP2518FD](https://www.microchip.com/en-us/product/mcp2518fd): exemplo de controlador CAN FD com SPI externo.
