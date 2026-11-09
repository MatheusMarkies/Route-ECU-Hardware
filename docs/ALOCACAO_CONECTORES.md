# Alocação elétrica dos conectores — 07/11/2026

Distribuição da folha [ECUConnectors.SchDoc](../ECUConnectors.SchDoc), conferida pela conectividade compilada no Altium. O [PDF](../ECTU.pdf) e a [netlist](../Project%20Outputs%20for%20ECTU/ECTU.NET) arquivados são anteriores à ligação do APP2.

A tabela usa os identificadores dos pinos nos símbolos atuais. **Não é uma liberação do chicote ou da PCB:** a correspondência física entre símbolo, pads e cavidades do CMC48 ainda deve ser validada.

| Conector | Função | Posições conectadas | Reservadas | Total |
|---|---|---:|---:|---:|
| J11 | Sensores e comunicação | 42 | 6 | 48 |
| J12 | Atuação, alimentação e lambda | 34 | 1 | 35 |

Os 83 pinos principais têm 76 posições ligadas e sete reservas. O APP2 usa J11-B4. O J11-E2, anteriormente ligado ao AUX6, ficou reservado. Os quatro conectores EGT são adicionais a essas 83 posições.

## Organização aplicada

- J11 reúne entradas analógicas, NTCs e seus retornos, CKP/CMP, quatro rodas, neutro, CAN e alimentação dos sensores.
- J12 reúne injetores, comandos de smart coils, ETC, IAC, relés, PWM, lambda, alimentação e retornos de potência.
- Três reservas do orçamento anterior do J12 foram usadas para `IAC_VBAT`, `RELAY1_VBAT` e `RELAY2_VBAT`, já presentes na folha.
- O pino J12-17 é a referência dos comandos de ignição. Sua função no chicote deve ser separada do retorno de corrente de potência das bobinas.
- GND permanece eletricamente comum. A organização dos trajetos de retorno na PCB ainda deve ser feita.

## EGT e interfaces separadas

Os quatro conectores EGT estão incluídos na folha, fora das 48 + 35 posições principais. O modelo de footprint vinculado na netlist é `OMEGA_PCC-SMP-K-5` nos quatro componentes.

| Canal | Designador | Pino P | Pino N |
|---|---|---|---|
| EGT1 | J17 | `EGT1_TC_POS` | `EGT1_TC_NEG` |
| EGT2 | J16 | `EGT2_TC_POS` | `EGT2_TC_NEG` |
| EGT3 | J15 | `EGT3_TC_POS` | `EGT3_TC_NEG` |
| EGT4 | J14 | `EGT4_TC_POS` | `EGT4_TC_NEG` |

Os pinos P/N chegam aos canais correspondentes do ADG729. Os pinos S1/S2 dos quatro símbolos estão ligados a GND na netlist; essa indicação precisa ser confrontada com a função real dos terminais e elementos de fixação do componente físico. `TC_NEG` permanece separado de GND. As transições de materiais e a compensação de junta fria devem ser consideradas no layout.

USB, microSD, UART e programação permanecem na folha de interfaces.

## Verificação

- A conectividade compilada confirma as 76 ligações e os sete pinos reservados da tabela.
- Os oito sinais P/N de EGT1 a EGT4 foram conferidos entre os quatro conectores e os canais correspondentes de IC2 (ADG729).
- Os oito pinos S1/S2 dos conectores EGT aparecem em GND.
- O PDF arquivado contém as 12 folhas do esquemático na revisão anterior à troca de AUX6 por APP2.
- Os hashes SHA-256 das fontes estão no [manifesto das imagens](images/sources.json).

A revisão elétrica, a conferência dos footprints, o dimensionamento dos contatos e a atualização da PCB seguem como próximas etapas.

## Referências físicas

- J11: [desenho Molex SD-500762-001](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/salesdrawingpdf/500/500762/5007620483_sd.pdf). O símbolo usa `A1..M4` e a netlist indica o footprint `CONN_SD-500762-001_MOL`. A correspondência com pads e cavidades ainda precisa de revisão física.
- J12: a netlist indica o footprint `TE_1-776163-1` e os pinos `1..35`. A conferência anterior pela API do Altium encontrou esses 35 identificadores no footprint; dimensões, contatos e correntes ainda precisam de revisão para a nova PCB.
- EGT: J14 a J17 usam o modelo `OMEGA_PCC-SMP-K-5` na netlist. Conferir desenho mecânico, terminais P/N, função de S1/S2 e montagem antes de fechar os footprints.

## Tabela de conexões

[Planilha CSV](ALOCACAO_CONECTORES.csv)

| Conector | Pino no símbolo | Rede | Função / reserva |
|---|---|---|---|
| J11 | A1 | `MAP_EXT_IN` | MAP externo |
| J11 | A2 | `MAF_EXT_IN` | MAF externo |
| J11 | A3 | `OIL_PRESS_ADC` | Pressao de oleo |
| J11 | A4 | `FUEL_PRESS_ADC` | Pressao de combustivel |
| J11 | B1 | `TPS1_ADC` | TPS 1 |
| J11 | B2 | `TPS2_ADC` | TPS 2 |
| J11 | B3 | `APP1_ADC` | APP 1 |
| J11 | B4 | `APP2_ADC` | APP 2 |
| J11 | C1 | `IAT_ADC` | Temperatura do ar |
| J11 | C2 | `CHT_ADC` | Temperatura do cabecote |
| J11 | C3 | `ECT_ADC` | Temperatura do liquido |
| J11 | C4 | `EOT_ADC` | Temperatura do oleo |
| J11 | D1 | `AUX1_ADC` | Entrada extra 1 |
| J11 | D2 | `AUX2_ADC` | Entrada extra 2 |
| J11 | D3 | `AUX3_ADC` | Entrada extra 3 |
| J11 | D4 | `AUX4_ADC` | Entrada extra 4 |
| J11 | E1 | `AUX5_ADC` | Entrada extra 5 |
| J11 | E2 | Sem conexão — reserva | Posição liberada pelo AUX6 |
| J11 | E3 | `CAN_H` | CAN H |
| J11 | E4 | `CAN_L` | CAN L |
| J11 | F1 | `CKP_VR_POS` | CKP VR + |
| J11 | F2 | `CKP_VR_NEG` | CKP VR - |
| J11 | F3 | `CKP_HALL_IN` | CKP Hall |
| J11 | F4 | `GND` | Retorno sensor CKP |
| J11 | G1 | `CMP_VR_POS` | CMP VR + |
| J11 | G2 | `CMP_VR_NEG` | CMP VR - |
| J11 | G3 | `CMP_HALL_IN` | CMP Hall |
| J11 | G4 | `GND` | Retorno sensor CMP |
| J11 | H1 | `WHEEL_FL_IN` | Roda dianteira esquerda |
| J11 | H2 | `WHEEL_FR_IN` | Roda dianteira direita |
| J11 | H3 | `WHEEL_RL_IN` | Roda traseira esquerda |
| J11 | H4 | `WHEEL_RR_IN` | Roda traseira direita |
| J11 | J1 | `NEUTRAL_SW_IN` | Neutro |
| J11 | J2 | `IAT_RETURN` | Retorno IAT |
| J11 | J3 | `CHT_RETURN` | Retorno CHT |
| J11 | J4 | `ECT_RETURN` | Retorno ECT |
| J11 | K1 | `EOT_RETURN` | Retorno EOT |
| J11 | K2 | `GND` | Retorno de sensores |
| J11 | K3 | `GND` | Retorno de sensores |
| J11 | K4 | `V5V0_SENS` | Alimentacao de sensores |
| J11 | L1 | `V5V0_SENS` | Alimentacao de sensores |
| J11 | L2 | `V5V0_SENS` | Alimentacao de sensores |
| J11 | L3 | `V5V0_SENS` | Alimentacao de sensores |
| J11 | L4 | Sem conexão — reserva | RESERVA BLINDAGEM 1 - terminacao a definir |
| J11 | M1 | Sem conexão — reserva | RESERVA BLINDAGEM 2 - terminacao a definir |
| J11 | M2 | Sem conexão — reserva | RESERVA SENSORES 1 |
| J11 | M3 | Sem conexão — reserva | RESERVA SENSORES 2 |
| J11 | M4 | Sem conexão — reserva | RESERVA SENSORES 3 |
| J12 | 1 | `LSU_IP` | Lambda IP |
| J12 | 2 | `LSU_IA` | Lambda IA |
| J12 | 3 | `LSU_UN` | Lambda UN |
| J12 | 4 | `LSU_VM` | Lambda VM |
| J12 | 5 | `LSU_HEATER_VBAT` | Positivo do aquecedor lambda |
| J12 | 6 | `LSU_HEATER_LS` | Low-side do aquecedor lambda |
| J12 | 7 | `GND` | Retorno de potencia |
| J12 | 8 | `GND` | Retorno de potencia |
| J12 | 9 | `GND` | Retorno de potencia |
| J12 | 10 | `GND` | Retorno de potencia |
| J12 | 11 | `VBAT_IN` | Entrada da alimentacao da ECU |
| J12 | 12 | `VBAT_IN` | Entrada da alimentacao da ECU |
| J12 | 13 | `IGN1_CONN` | Comando smart coil 1 |
| J12 | 14 | `IGN2_CONN` | Comando smart coil 2 |
| J12 | 15 | `IGN3_CONN` | Comando smart coil 3 |
| J12 | 16 | `IGN4_CONN` | Comando smart coil 4 |
| J12 | 17 | `GND` | Referencia de comando das smart coils - nao retorno de potencia |
| J12 | 18 | `PWM1_OUT` | PWM 1 |
| J12 | 19 | `PWM2_OUT` | PWM 2 |
| J12 | 20 | `PWM3_OUT` | PWM 3 |
| J12 | 21 | `PWM4_OUT` | PWM 4 |
| J12 | 22 | `IGN_SW_12V` | Entrada pos-chave |
| J12 | 23 | Sem conexão — reserva | RESERVA ATUACAO |
| J12 | 24 | `INJ1_LS` | Injetor 1 |
| J12 | 25 | `INJ2_LS` | Injetor 2 |
| J12 | 26 | `INJ3_LS` | Injetor 3 |
| J12 | 27 | `INJ4_LS` | Injetor 4 |
| J12 | 28 | `ETC_OUT1` | Motor ETC terminal 1 |
| J12 | 29 | `ETC_OUT2` | Motor ETC terminal 2 |
| J12 | 30 | `IAC_LS` | Comando IAC |
| J12 | 31 | `RELAY1_LS` | Comando rele 1 |
| J12 | 32 | `RELAY2_LS` | Comando rele 2 |
| J12 | 33 | `IAC_VBAT` | Positivo IAC |
| J12 | 34 | `RELAY1_VBAT` | Positivo rele 1 |
| J12 | 35 | `RELAY2_VBAT` | Positivo rele 2 |
