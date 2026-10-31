# Pontos para conectores e carimbos — ECU / ECTU

Aplicado em 14/10/2026 ao projeto `D:/Route-ECU-Hardware/ECTU.PrjPcb`.

## O que foi aplicado

- A folha `ECUConnectors.SchDoc` recebeu **87 pontos com fios livres**, agrupados por função: **72 pontos de interface com o chicote e 15 pontos opcionais para serviço/expansão**. São 86 nomes de rede distintos, pois GND aparece nos dois conjuntos. A lista é uma organização de redes, e não um orçamento final de cavidades; alimentações e retornos podem exigir vários contatos.
- Os símbolos são power ports globais com os nomes existentes no circuito. Cada fio termina livre para atribuição manual a um pino. Não foram atribuídos pinos ao AMPSEAL novo, nem removidos os pontos que já estavam ligados a J11.
- Conforme solicitado, `IGN1_OUT` a `IGN4_OUT` foram renomeados para `IGN1_CONN` a `IGN4_CONN` nas saídas dos drivers. Isso une intencionalmente os quatro canais às redes correspondentes já existentes em J11.
- O carimbo das 12 folhas foi substituído por um modelo do próprio projeto, com autor **Matheus Markies**, projeto **ROUTE ECU / ECTU**, título de cada subsistema, código `ECTU-SCH-01` a `ECTU-SCH-12`, data documental **14/10/2026**, revisão **A definir**, status **Em desenvolvimento**, arquivo e folha/total. O campo de revisão não declara uma versão de hardware aprovada.
- O modelo reutilizável está em `Templates/ECTU_A3_MatheusMarkies.SchDot`. Os campos ficam em parâmetros do documento; `ProjectTitle` é um parâmetro próprio para evitar o nome reservado `ProjectName` do Altium. Os arquivos atualmente guardam o caminho absoluto para esse modelo; se o checkout mudar de local, reassociar o modelo pela interface de templates.

## Limites e pontos ainda pendentes

- APP2 está indicado como planejado: ainda não há uma rede/canal ADC definido no circuito atual. Não foi criado um sinal elétrico fictício.
- PWM5 e PWM6 existem como comandos internos do MCU, sem estágios de saída externos; foram indicados como pendência.
- Os sinais de serviço/expansão são interfaces lógicas internas. Sua inclusão é opcional, e não constitui condicionamento para conexão ao chicote automotivo. USB X1 e microSD J4 continuam em CommunicationInterfaces; os headers existentes também foram preservados.
- Pares EGT preservam `TC_POS` e `TC_NEG`. Não foi transformado o negativo do termopar em GND.
- Alimentações de sensores, retornos de potência e positivos de IAC/relés precisam da distribuição de contatos e da revisão de corrente apropriadas quando os pinos físicos forem definidos.
- A PCB não foi modificada nesta etapa. Sincronizar o esquema com a PCB por ECO após concluir a atribuição dos conectores.

## Verificação realizada

- Cópias de segurança dos arquivos em disco e do estado salvo do projeto foram mantidas antes das edições. A inserção do novo AMPSEAL feita pelo usuário foi salva e incluída na cópia de segurança.
- A organização dos pontos foi primeiro aplicada e inspecionada em uma cópia da folha. Depois, a folha original foi salva e conferida visualmente no Altium.
- Foram criados 87 power ports e 87 fios, com os extremos na grade de captura do documento.
- A comparação das duas exportações nativas de conectividade contém **1.255 pinos antes e depois**. Não houve diferenças além da substituição solicitada dos quatro nomes de ignição e da consequente união com suas redes CONN.
- A comparação dos registros de circuito das 12 folhas antes e depois da edição dos carimbos foi idêntica, após tratar a renumeração da tabela de fontes e a normalização de texto/identificadores de parâmetros feita pelo Altium. Componentes, pinos, fios, junções e redes não foram alterados pela edição dos carimbos.
- A PCB foi conferida por comparação integral de bytes e permanece igual à cópia de segurança.
- Isso não significa aprovação de ERC: a compilação já retornava falso antes desta etapa e atingia o limite de 1.000 mensagens. A comparação foi usada para verificar as alterações deste pedido, sem corrigir os problemas anteriores do projeto.

## Redes disponibilizadas na folha

### ALIMENTAÇÃO

`VBAT_IN`, `V5V0_SENS`, `GND`.

### SENSORES ANALÓGICOS

`MAP_EXT_IN`, `MAF_EXT_IN`, `TPS1_ADC`, `TPS2_ADC`, `APP1_ADC`, `OIL_PRESS_ADC`, `FUEL_PRESS_ADC`, `AUX1_ADC`, `AUX2_ADC`, `AUX3_ADC`, `AUX4_ADC`, `AUX5_ADC`, `AUX6_ADC`.

### TEMPERATURAS — NTC

`IAT_ADC`, `IAT_RETURN`, `CHT_ADC`, `CHT_RETURN`, `ECT_ADC`, `ECT_RETURN`, `EOT_ADC`, `EOT_RETURN`.

### EGT — TERMOPARES

`EGT1_TC_POS`, `EGT1_TC_NEG`, `EGT2_TC_POS`, `EGT2_TC_NEG`, `EGT3_TC_POS`, `EGT3_TC_NEG`, `EGT4_TC_POS`, `EGT4_TC_NEG`.

### NEUTRO / PÓS-CHAVE

`NEUTRAL_SW_IN`, `IGN_SW_12V`.

### REDE CAN

`CAN_H`, `CAN_L`.

### SONDA LAMBDA

`LSU_IP`, `LSU_IA`, `LSU_UN`, `LSU_VM`, `LSU_HEATER_VBAT`, `LSU_HEATER_LS`.

### ROTAÇÃO / FASE

`CKP_VR_POS`, `CKP_VR_NEG`, `CKP_HALL_IN`, `CMP_VR_POS`, `CMP_VR_NEG`, `CMP_HALL_IN`.

### VELOCIDADE DAS RODAS

`WHEEL_FL_IN`, `WHEEL_FR_IN`, `WHEEL_RL_IN`, `WHEEL_RR_IN`.

### BICOS — LOW-SIDE

`INJ1_LS`, `INJ2_LS`, `INJ3_LS`, `INJ4_LS`.

### IGNIÇÃO — SMART COIL

`IGN1_CONN`, `IGN2_CONN`, `IGN3_CONN`, `IGN4_CONN`.

### MOTOR DA BORBOLETA

`ETC_OUT1`, `ETC_OUT2`.

### MARCHA LENTA — IAC

`IAC_LS`, `IAC_VBAT`.

### RELÉS AUXILIARES

`RELAY1_LS`, `RELAY1_VBAT`, `RELAY2_LS`, `RELAY2_VBAT`.

### SAÍDAS PWM

`PWM1_OUT`, `PWM2_OUT`, `PWM3_OUT`, `PWM4_OUT`.

### SERVIÇO / EXPANSÃO — OPCIONAL

`UART1_TX`, `UART1_RX`, `UART2_TX`, `UART2_RX`, `I2C1_SCL`, `I2C1_SDA`, `I2C2_SCL`, `I2C2_SDA`, `SWDIO`, `SWCLK`, `MCU_RESET_N`, `SWO`, `JTDI`, `V3V3`, `GND`.

## Cópias de segurança

- Antes de adicionar pontos e renomear ignição: `D:\Route-ECU-Hardware\_codex_harness\backup_live_20261014_211615`.
- Antes de aplicar os carimbos, já incluindo os pontos: `D:\Route-ECU-Hardware\_codex_titleblock\backup_20261014_212128`.
