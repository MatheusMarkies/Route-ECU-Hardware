# Imagens da documentação

As imagens `schematic-*.png` são renderizações das 12 folhas do [ECTU.pdf](../../ECTU.pdf), exportado em 31/10/2026, sem redesenhar ou alterar os circuitos. Os arquivos `*-detail.png` são recortes renderizados diretamente da folha 11, para facilitar a leitura de J11, J12 e dos quatro conectores EGT. As páginas, coordenadas dos recortes e os hashes SHA-256 do PDF e da netlist estão em [sources.json](sources.json).

O diagrama `architecture` descreve a organização do hardware, e `connector-partition` mostra a divisão do chicote entre J11, J12 e as conexões EGT dedicadas. O diagrama `communication-flow` apresenta uma proposta de firmware; não representa uma integração já testada. Cada diagrama possui uma versão SVG editável e uma PNG para visualização no GitHub.

A exportação usada nesta atualização contém 12 folhas de esquemático. A PCB da nova versão ainda está pendente e não é apresentada como concluída no README.

Para regenerar as imagens após atualizar o PDF ou os diagramas:

```bash
python -m pip install pymupdf
python docs/generate_readme_images.py
```

O script lê o PDF, calcula os hashes do PDF e da netlist, e grava as imagens e o manifesto nesta pasta. Ele não altera o PDF, a netlist, os esquemáticos ou a PCB.
