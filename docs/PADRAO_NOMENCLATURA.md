# Padrão de nomes das conexões da ECU

Aplicado em 14/10/2026 às 12 folhas do ECTU.PrjPcb e aos nomes correspondentes existentes em ECTU_PCB.PcbDoc. A nomenclatura segue a função elétrica observada no projeto; a atribuição ao H743 ou ao futuro G0 pode mudar sem exigir renomear a função externa.

## Regras

- Usar letras maiúsculas, números e underscore, sem espaços, acentos ou sinais +/− nos nomes de redes.
- Identificar primeiro a função: INJ, IGN, ETC, LSU, MAP, MAF, IAT, CHT, ECT, EOT, APP, TPS, WHEEL, CAN, USB, SD, UART e I2C.
- Colocar o número do canal junto à função: INJ1, IGN1, TPS1, APP1, AUX1, PWM1 e ADC1. Posições de roda: FL, FR, RL e RR.
- Usar _N no fim dos sinais digitais comprovadamente ativos em nível baixo, como IGN_SW_N, MCU_RESET_N, EGT_CS_N e ETC_FAULT_N. Em ETC_SLEEP_N, zero solicita sleep; um permite operação. O nome descreve a função nSLEEP do CI.
- Usar _POS/_NEG para polaridade de sinais analógicos diferenciais e termopares: CKP_VR_POS/NEG e EGT1_TC_POS/NEG. Assim, _N fica reservado à convenção digital nesse projeto.
- Manter nomes de sinais de CI que já são claros, como CJ125_UA, CJ125_UR, SWDIO, SWCLK, SWO e JTDI. Os nomes dos pinos internos dos símbolos continuam seguindo seus fabricantes.
- Não criar nomes diferentes para simular estágios que eletricamente já são o mesmo nó. Consolidar somente aliases comprovados pela compilação; preservar nomes distintos dos nós realmente separados por resistores, filtros, net ties ou conversores de nível.
- Não introduzir PGND/AGND/SGND como novas redes durante uma revisão de nomes. A rede GND continua a mesma; separar retornos fisicamente exige projeto próprio.

## Sufixos e exemplos

| Nome / sufixo | Significado no projeto | Exemplo |
|---|---|---|
| _CMD | Comando lógico para o driver | INJ1_CMD, IGN1_CMD, RELAY1_CMD |
| _LS | Nó de potência com comutação pelo lado baixo | INJ1_LS, RELAY1_LS, LSU_HEATER_LS |
| _OUT | Saída do estágio indicado | IGN1_OUT, ETC_OUT1 |
| _CONN | Rede do conector ainda distinta da saída correspondente | IGN1_CONN |
| _IN | Entrada externa antes do condicionamento, quando há esse nó separado | MAP_EXT_IN, WHEEL_FL_IN |
| _FILT | Nó filtrado distinto | CKP_HALL_FILT |
| _ADC | Sinal que chega à aquisição analógica | APP1_ADC, TPS1_ADC, AUX1_ADC, IAT_ADC |
| _MCU | Lado lógico do MCU ou sinal condicionado para ele | CKP_MCU, USB_DP_MCU, IAC_STATUS_MCU |
| _IC | Lado do CI após o conversor de nível | CJ125_MOSI_IC |
| _GATE / _DRV | Gate da carga / estágio que o comanda | LSU_HEATER_GATE / LSU_HEATER_DRV |
| _SENSE_GND | Referência Kelvin/retorno do circuito de medição de corrente do bico | INJ1_SENSE_GND |
| _RETURN | Retorno do sensor, preservado como rede própria quando há net tie | IAT_RETURN |
| _POS / _NEG | Polaridade de sinal diferencial/termopar | EGT1_TC_POS / EGT1_TC_NEG |
| _N | Função digital ativa em nível baixo | IGN_SW_N, ETC_SLEEP_N |
| _LEVEL_SEL / _PULLUP_SW | Seleção do nível da saída PWM / nó da alimentação de pull-up comutada | PWM1_LEVEL_SEL / PWM1_PULLUP_SW |

## Alimentações e barramentos

| Nome | Função |
|---|---|
| VBAT_IN | Entrada de bateria antes do circuito de entrada da ECU |
| VBAT_ECU | Barramento de bateria interno da ECU; o nome não aprova a proteção contra surtos |
| V5V0 | Alimentação de 5 V |
| V5V0_SENS | Alimentação de sensores de 5 V |
| V3V3 | Alimentação lógica de 3,3 V |
| V3V3_A | Alimentação analógica que hoje une VDDA e VREF do MCU |
| VBAT_MCU_ADC / VBAT_EXT_ADC | Divisores de bateria destinados ao ADC interno / externo, preservados separados |
| I2C1_SCL/SDA, I2C2_SCL/SDA | Barramentos existentes; o nome não pressupõe tensão correta dos pull-ups |
| TEMP_ADC_SCL/SDA | Lado do ADS1115 no conversor de nível |
| SPI_ADC_SCK/MOSI/MISO | Barramento de aquisição atualmente compartilhado também pelo EGT |
| ADC1_CS_N / ADC2_CS_N | Seleções individuais dos dois ADCs |
| CJ125_SCK/MOSI/MISO_MCU ou _IC | Dois lados dos conversores de nível do CJ125 |
| CJ125_CS_MCU_N / CJ125_CS_IC_N | Seleção do CJ125, ativa em nível baixo |
| UART1_TX/RX, UART2_TX/RX | TX e RX vistos pelo MCU da ECU |
| CAN_H/L, CAN_TX/RX | Barramento CAN externo e interface lógica do transceptor |
| USB_DP/DM_CONN e USB_DP/DM_MCU | Lados do conector e do MCU, preservando a interface de proteção existente |
| SD_CLK, SD_CMD, SD_D0…SD_D3 | Interface do cartão SD |
| HSE_OSC_IN/OUT, LSE_OSC_IN/OUT | Osciladores principal e de baixa frequência do MCU |

ADC1_ALERT, ADC2_ALERT e TEMP_ADC_ALERT permanecem sem _N: não foi atribuída uma polaridade fixa a sinais cuja variante/configuração ainda precisa ser fechada. A troca de nome não corrige o uso de DNC/ALARM no símbolo dos ADS8688.

## Redes que exigem decisão elétrica separada

IGN1_OUT…IGN4_OUT e IGN1_CONN…IGN4_CONN continuam distintas, como já eram antes sob Output_Ig_n e Ig_n. O conector J11 usa M4/M3/M2/M1 para IGN1_CONN/IGN2_CONN/IGN3_CONN/IGN4_CONN. Unir esses pares exige resolver a conexão, e não apenas dar o mesmo nome para esconder a pendência.

Os aliases Sensor_n, Sensor_In_n e os respectivos TVS_n foram consolidados em AUXn_ADC porque a compilação confirmou que já pertencem ao mesmo nó. O mesmo vale para APP1, TPS1/TPS2 e pressões. Isso não cria um resistor série ou um estágio de filtro que não exista no circuito. MAP_EXT_IN/ADC e MAF_EXT_IN/ADC continuam separados porque são nós distintos.

PROT_SPARE1 identifica a entrada de proteção antes chamada TVS_8 sem atribuir-lhe um sensor ainda não conectado. Redes locais automáticas NetC…/NetR… permanecem automáticas. Nomes legados que só existem na revisão antiga da PCB, sem correspondência comprovada no esquema atual, não receberam uma função inventada.

O mapa completo antes/depois está em [MAPA_RENOMEACAO_REDES.csv](MAPA_RENOMEACAO_REDES.csv). A revisão de nomes não resolve designadores R?/D?, pinos abertos, proteções ou sincronização de componentes/layout entre revisões.
