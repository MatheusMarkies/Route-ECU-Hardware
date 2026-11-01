"""Render README figures from ECTU.pdf and draw the documented architecture.

Requires PyMuPDF: python -m pip install pymupdf
Run from any directory: python docs/generate_readme_images.py
"""

from pathlib import Path
from xml.sax.saxutils import escape
import hashlib
import json
import math

import fitz


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "images"
SOURCE = ROOT / "ECTU.pdf"
NETLIST = ROOT / "Project Outputs for ECTU" / "ECTU.NET"
PAGES = {
    "schematic-mcus.png": (1, "Microcontroladores, clocks e resets"),
    "schematic-communications.png": (2, "CAN, USB, microSD e interfaces de serviço"),
    "schematic-analog.png": (3, "Aquisição analógica e saídas PWM"),
    "schematic-injection-ignition.png": (4, "Injeção e comandos de ignição"),
    "schematic-crank-cam.png": (5, "Rotação, fase e velocidade das rodas"),
    "schematic-low-side.png": (6, "Drivers de IAC e relés"),
    "schematic-pressure-airflow.png": (7, "Pressão e fluxo de ar"),
    "schematic-lambda.png": (8, "Lambda wideband e comando do aquecedor"),
    "schematic-power.png": (9, "Alimentação e proteções"),
    "schematic-etc.png": (10, "Ponte H da borboleta eletrônica"),
    "schematic-connectors.png": (11, "J11, J12 e quatro conectores EGT tipo K"),
    "schematic-temperatures.png": (12, "Temperaturas NTC e termopares multiplexados"),
}
DETAILS = {
    "schematic-j11-detail.png": (11, (545, 105, 700, 410), "J11: sensores e comunicação"),
    "schematic-j12-detail.png": (11, (285, 105, 415, 410), "J12: atuação, alimentação e lambda"),
    "schematic-egt-connectors-detail.png": (11, (195, 450, 415, 535), "J17 a J14: EGT1 a EGT4"),
}


class Diagram:
    def __init__(self, width, height, title, subtitle):
        self.width, self.height = width, height
        self.items = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'<title>{escape(title)}</title>',
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#52677b"/></marker></defs>',
            f'<rect width="{width}" height="{height}" fill="#f7f9fc"/>',
        ]
        self.text(55, 63, title, 34, "#152c44", True)
        self.text(55, 105, subtitle, 20, "#52677b")

    def text(self, x, y, label, size=21, color="#263d52", bold=False, anchor="start"):
        self.items.append(
            f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(label)}</text>'
        )

    def box(self, x, y, w, h, title, rows, color="#536b83", fill="#ffffff"):
        self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="13" fill="{fill}" stroke="{color}" stroke-width="2"/>')
        self.items.append(f'<rect x="{x}" y="{y + 15}" width="5" height="{h - 30}" fill="{color}"/>')
        self.text(x + 22, y + 39, title, 24, color, True)
        for i, row in enumerate(rows):
            self.text(x + 22, y + 77 + 29 * i, row, 20)

    def arrow(self, points, both=False):
        p = " ".join(f"{x},{y}" for x, y in points)
        self.items.append(f'<polyline points="{p}" fill="none" stroke="#52677b" stroke-width="2.5" stroke-linejoin="round"/>')
        ends = [(points[-2], points[-1])]
        if both:
            ends.append((points[1], points[0]))
        for previous, tip in ends:
            angle = math.atan2(tip[1] - previous[1], tip[0] - previous[0])
            x, y = tip
            vertices = [tip]
            for side in [-1, 1]:
                vertices.append((x - 12 * math.cos(angle) + side * 5 * math.sin(angle), y - 12 * math.sin(angle) - side * 5 * math.cos(angle)))
            points_text = " ".join(f"{a:.2f},{b:.2f}" for a, b in vertices)
            self.items.append(f'<polygon points="{points_text}" fill="#52677b"/>')

    def label(self, x, y, label):
        self.text(x, y, label, 18, "#52677b", anchor="middle")

    def footer(self, first, second):
        y = self.height - 92
        self.items.append(f'<path d="M 55 {y} H {self.width - 55}" stroke="#d3dce6"/>')
        self.text(55, y + 33, first, 18)
        self.text(55, y + 61, second, 18, "#52677b")

    def save(self, name):
        svg = "\n".join(self.items + ["</svg>"])
        (OUTPUT / f"{name}.svg").write_text(svg, encoding="utf-8")
        with fitz.open(stream=svg.encode("utf-8"), filetype="svg") as document:
            document[0].get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False).save(OUTPUT / f"{name}.png")


def architecture():
    d = Diagram(1600, 1160, "ROUTE ECU / ECTU", "Arquitetura do esquemático consolidado em 31/10/2026")
    d.box(580, 200, 420, 245, "STM32H743VIT6 · H7", ["Sincronismo e controle do motor", "Injeção, ignição e atuadores", "SPI1: ADCs / SPI2: CJ125", "USB, microSD e SWD próprio"], "#08766e", "#edf8f5")
    d.box(580, 710, 420, 245, "STM32G071RBT6 · G0", ["Captura das quatro rodas", "Temperaturas, EGT e CAN", "I²C2: FRAM + ADG729", "UART e SWD/reset próprios"], "#245fa1", "#edf3fb")
    d.box(55, 200, 420, 245, "Aquisição principal", ["CKP / CMP: VR ou Hall", "2 × ADS8688 via SPI", "TPS, APP1, pressões e AUX", "MAP / MAF e sinais do CJ125"], "#08766e")
    d.box(55, 495, 420, 190, "Estágios de saída", ["4 injetores / 4 comandos de ignição", "ETC, IAC e dois relés", "4 saídas PWM"], "#9c6526")
    d.box(55, 735, 420, 220, "Aquisição auxiliar", ["4 entradas de velocidade de roda", "ADS1115: quatro NTCs", "MAX31856 + ADG729:", "quatro termopares, leitura sequencial"], "#245fa1")
    d.box(1110, 210, 435, 175, "PC · Route ECU Workbench", ["USB Full Speed no H7", "Telemetria e tuning:", "integração de firmware em definição"], "#7054a1")
    d.box(1110, 485, 435, 140, "microSD", ["SDMMC de quatro bits no H7", "Armazenamento previsto para logs"], "#536b83")
    d.box(1110, 730, 435, 145, "Interface CAN FD", ["MCP2518FD: controlador SPI", "MCP2562FD: transceiver CAN"], "#245fa1")
    d.box(1110, 920, 435, 100, "FRAM · MB85RC1MT", ["I²C2 do G0 no netlist atual"], "#536b83")
    d.arrow([(475, 315), (580, 315)])
    d.label(528, 295, "Entradas")
    d.arrow([(580, 405), (525, 405), (525, 565), (475, 565)])
    d.arrow([(1000, 300), (1110, 300)], both=True)
    d.label(1055, 280, "USB")
    d.arrow([(1000, 405), (1055, 405), (1055, 550), (1110, 550)], both=True)
    d.label(990, 475, "SDMMC")
    d.arrow([(790, 445), (790, 710)], both=True)
    d.text(820, 525, "SPI4 mestre (H7)", 21, "#263d52", True)
    d.text(820, 558, "SPI2 escravo (G0)", 21)
    d.text(820, 591, "SCK, MOSI, MISO e NSS", 19)
    d.text(820, 622, "IRQ: G0 → H7", 19)
    d.arrow([(475, 825), (580, 825)])
    d.arrow([(1000, 805), (1110, 805)], both=True)
    d.label(1055, 782, "SPI1")
    d.arrow([(1000, 905), (1055, 905), (1055, 970), (1110, 970)], both=True)
    d.label(1055, 999, "I²C2")
    d.footer("Esquemático desta etapa concluído. A PCB da nova versão ainda está pendente.", "Diagrama de conexões e funções previstas; implementação e desempenho dependem de firmware e validação.")
    d.save("architecture")


def communication():
    d = Diagram(1600, 870, "Comunicação entre os MCUs e o PC", "Proposta de firmware: transferências assíncronas e trabalho de comunicação limitado")
    d.box(55, 190, 310, 170, "G0 · aquisição", ["Prepara blocos de dados", "Sequência, timestamp e CRC", "Avisa quando está pronto"], "#245fa1")
    d.box(445, 190, 310, 170, "SPI dedicado", ["H7 agenda a transferência", "DMA para TX e RX", "Recepção em buffers"], "#245fa1")
    d.box(835, 190, 310, 170, "H7 · telemetria", ["Valida e atualiza o estado", "Fila USB limitada", "Atendimento sem bloqueio"], "#08766e")
    d.box(1225, 190, 310, 170, "PC · Workbench", ["Recebe pelo USB do H7", "Exibe dados e estados", "Solicita parâmetros"], "#7054a1")
    for a, b in [(365,445),(755,835),(1145,1225)]:
        d.arrow([(a,275),(b,275)])
    d.label(1185, 253, "USB")
    d.box(445, 415, 700, 105, "H7 · controle do motor", ["Prioridade sobre a comunicação; usa uma cópia consistente dos dados."], "#9c6526", "#fff8eb")
    d.arrow([(600,360),(600,415)])
    d.box(55, 590, 310, 145, "G0 · configuração", ["Recebe o que lhe pertence", "Responde em outro quadro"], "#245fa1")
    d.box(445, 590, 310, 145, "Validar e aplicar", ["Limites e confirmação", "Atualização em ponto definido"], "#9c6526")
    d.box(835, 590, 310, 145, "H7 · comandos", ["Fila própria de solicitações", "Identificação e resposta"], "#08766e")
    d.box(1225, 590, 310, 145, "PC · tuning", ["Envia alterações pelo USB", "Acompanha a confirmação"], "#7054a1")
    for a, b in [(1225,1145),(835,755),(445,365)]:
        d.arrow([(a,660),(b,660)])
    d.label(405, 638, "SPI")
    d.arrow([(600,590),(600,520)])
    d.footer("O painel pode substituir amostras antigas; comandos precisam de confirmação e tratamento de fila cheia.", "DMA, protocolo, taxas de atualização e jitter ainda precisam ser implementados e medidos.")
    d.save("communication-flow")


def connectors():
    d = Diagram(1600, 950, "Conectores e organização do chicote", "Separação por função elétrica na folha ECUConnectors.SchDoc")
    d.box(55, 180, 700, 325, "J11 · Molex CMC48", [
        "Sensores e comunicação · 42 ligados + 6 reservas",
        "MAP / MAF, TPS1/2, APP1, pressões e AUX1–6",
        "IAT / CHT / ECT / EOT e retornos dedicados",
        "CKP / CMP: VR e Hall; quatro rodas e neutro",
        "CAN H/L, 5 V dos sensores e referências GND",
        "APP2 e futuras funções: posições reservadas",
    ], "#08766e", "#edf8f5")
    d.box(835, 180, 710, 325, "J12 · TE AMPSEAL 35", [
        "Atuação, alimentação e lambda · 34 ligados + 1 reserva",
        "Quatro injetores e quatro comandos de smart coils",
        "Borboleta eletrônica, IAC e dois relés",
        "Quatro saídas PWM e entrada de pós-chave",
        "Lambda: quatro sinais e dois fios do aquecedor",
        "VBAT de entrada e retornos GND",
    ], "#9c6526", "#fff8eb")
    d.box(55, 565, 700, 225, "Quatro conectores EGT dedicados", [
        "J17: EGT1 · J16: EGT2 · J15: EGT3 · J14: EGT4",
        "Modelo vinculado: OMEGA_PCC-SMP-K-5",
        "Cada termopar tem seu próprio par POS / NEG",
        "Fora das 83 posições de J11 + J12",
    ], "#245fa1", "#edf3fb")
    d.box(835, 565, 710, 225, "Interfaces de serviço separadas", [
        "USB no H7 para o Route ECU Workbench",
        "microSD e headers de programação / UART",
        "G0 com programação e reset próprios",
        "Relés externos: VBAT e LS acionam a bobina",
    ], "#7054a1")
    d.footer("Alocação elétrica documentada; revisar cavidades, footprints, contatos e trajetos de retorno na PCB.", "A separação dos ramais não cria isolamento elétrico: GND permanece comum no esquema.")
    d.save("connector-partition")


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with fitz.open(SOURCE) as document:
        for name, (number, _) in PAGES.items():
            document[number - 1].get_pixmap(matrix=fitz.Matrix(4, 4), alpha=False).save(OUTPUT / name)
        for name, (number, rect, _) in DETAILS.items():
            document[number - 1].get_pixmap(matrix=fitz.Matrix(6, 6), clip=fitz.Rect(rect), alpha=False).save(OUTPUT / name)
    architecture()
    communication()
    connectors()
    manifest = {
        "revision_date": "2026-10-31",
        "source": "ECTU.pdf",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "netlist": "Project Outputs for ECTU/ECTU.NET",
        "netlist_sha256": hashlib.sha256(NETLIST.read_bytes()).hexdigest(),
        "schematics": {name: {"page": number, "caption": caption} for name, (number, caption) in PAGES.items()},
        "details": {name: {"page": number, "clip_points": list(rect), "caption": caption} for name, (number, rect, caption) in DETAILS.items()},
        "diagrams": {
            "architecture": "Conexões do PDF e netlist atuais; funções descritas como previstas.",
            "communication-flow": "Proposta de firmware, sem validação de execução ou temporização.",
            "connector-partition": "Distribuição elétrica de J11/J12 e identificação dos quatro conectores EGT na exportação atual.",
        },
    }
    (OUTPUT / "sources.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Rendered {len(PAGES)} schematic pages, {len(DETAILS)} details and 3 diagrams to {OUTPUT}")


if __name__ == "__main__":
    main()
