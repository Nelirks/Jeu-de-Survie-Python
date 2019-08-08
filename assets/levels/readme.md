# Nouveau système de stockage des cartes
objectif : caméra libre et multijoueur

## caractéristiques
- les zones font maintenant plusieurs écrans et a un seul set de texture
## fichier
la zone est stocké dans un fichier sous la forme d'un dictionnaire avec : 
- `dictionnaire["size"]` : liste enregisté avec pickle avec [largueur, hauteur] , la largeur et la hauteur est compté en tuiles
- `dictionnaire["set"]` : numéro du set de texture
- `dictionnaire["entities"]` : liste de `savableEntity` avec leur noms et leurs position
- `dictionnaire["solid"]` : textures du sol accessible avec solid[x][y]
