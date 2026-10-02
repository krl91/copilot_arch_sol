# Diagrammes

Inspiré du skill `drawio` d'awesome-copilot.

## Par défaut : Mermaid dans le brouillon
Rapide à relire et à corriger. Libellés en anglais, une vue par diagramme :
environnement (operational), scénario opérationnel (séquence), modes/états, architecture fonctionnelle,
allocation fonctions → composants.

## Sur demande : fichier draw.io
1. Écrire `1 Projects/<P>/Drafts/diagrams/<nom>.drawio` au format XML `mxGraphModel` (une page par vue).
2. Styles cohérents :
   | Élément | Style |
   |---|---|
   | Système étudié | `rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;strokeWidth=2;` |
   | Système externe / acteur | `rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;` |
   | Fonction | `rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;` |
   | Point d'attention | `rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;` |
   | Stockage | `shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;` |
   | Flux | `edgeStyle=orthogonalEdgeStyle;rounded=1;strokeWidth=2;` |
3. Ouvrir avec l'extension VS Code « Draw.io Integration » ou draw.io desktop, finaliser à la main.
4. Export PNG éditable (XML embarqué) si draw.io desktop est installé :
   `drawio -x -f png -e -b 10 -o <sortie.png> <entrée.drawio>`
   (Windows : `"C:/Program Files/draw.io/draw.io.exe"` si `drawio` n'est pas dans le PATH).

Tout libellé de diagramme suit la même règle que le texte : aucun élément sans source.
