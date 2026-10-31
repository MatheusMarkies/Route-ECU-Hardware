# Imagens da documentação

As imagens `schematic-*.png` são renderizações das folhas do [ECTU.pdf](../../ECTU.pdf), sem redesenhar ou alterar os circuitos. A origem de cada página e o SHA-256 do PDF usado estão em [sources.json](sources.json).

Os diagramas `architecture` descrevem a organização do hardware. Os diagramas `communication-flow` apresentam uma proposta de firmware; não representam uma integração já testada. Cada diagrama possui uma versão SVG editável e uma PNG para visualização no GitHub.

O layout antigo presente na exportação do projeto não foi usado nas imagens do README. A PCB da nova versão ainda está pendente.

Para regenerar as imagens após atualizar o PDF ou os diagramas:

```bash
python -m pip install pymupdf
python docs/generate_readme_images.py
```

O script apenas lê o PDF e grava as imagens e o manifesto nesta pasta. Ele não altera os esquemáticos nem a PCB.
