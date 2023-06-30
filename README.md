# curve-marking

Curve Marking Technique for Sante Energy

## Product Symbols

| Product            | Symbol |
| ------------------ | ------ |
| Brent              | I      |
| Barge Crack        | BOA    |
| Fuel Oil East/West | SJS    |
| Visco              | STS    |
| 180                | SZS    |
| 380                | SYS    |
| LSGO               |        |
| Dubai              |        |
| dfl                |        |
| GO E/W             | BAP    |
| IPE Gasoil         | G      |

## Formulas

```
Kero = Regrade + SinGO (Marked on top of SinGO, Kero has bad liquidity)
380 = (Brent + Barge Crack)/6.35 + Fuel Oil East/West
Visco = 180 - 380
LSFO 0.5% = hi5 + 380
Gasoline = (EBOB/RBOB + RBOB) * 42 + 92 E/W /8.33
Mopj = (Brent + Mopj Crack) * 8.9
Sing Gas Oil = (IPE(G) + Go East/West(BAP)) / 7.45
```
