# Système de cartes, ajout des chunks
Dans l'optique de faire un jeu multijoueur la carte ne sera plus composé de régions mais de chunks, ces chunks seront carrés et permettent d'avoir la caméra centré sur le joueur.

## caractéristiques :
- 16 tuiles de large et 16 tuiles de long
- un seul set de texture possible (comme pour les régions)
- contient des entités et les tuiles solides
- les sets contiennent les noms des tuiles bloquantes `blockingTiles.txt`

## format de fichier
- Les zones de chunck sont stockés dans le dossier `./assets/chunks/`
- tous les chunks d'une zone sont stockés dans un sous dossier nommé du nom de la zone
- un chunck est stocké dans un fichier (avec pickle) avec l'extention `.chunck`
- le nom d'un chunck détermine ça position dans la zone format : `X.Y.chunck` ex : `5.1.chunck`
- chaque fichier de chunck contient un dictionnaire les tuiles solides dans `dictionnnaire["solid"]` et sa position dans `dictionnaire["position"]`
- chaque zone contient dans son dossier un fichier `info` contenant le nombre de chunk dans la largeur, le nombre de chunck dans la longueur et le numéro du set dans une liste enregistré avec pickle : `[X,Y,setNum]`
- les entités sont stockées dans le fichier `entities` de la zone
