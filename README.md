# Traitement-d-images

Le projet est réalisé dans le cadre d’apprentissage des outils de traitement d’images, notamment le domaine de
la morphologie. En tant qu’étudiante en master mathématiques de données, j’ai choisi d’étudier cette matière
car le prof nous a promis que ça changera notre vie :D, je l’ai cru bien évidement, mais la principale raison
est que j’aime tout ce qui est algorithmique assaisonné avec des mathématiques. 

Dans ce projet on nous demande de mettre en place un système automatique de détection d’inondation dans
des égouts. D’après l’énoncé, se sont des milieux complètement obscurs et humides. Les sondes classiques
de détection d’humidité ne fonctionnent pas dans ce cas, car l’humidité de l’environnement est tel qu’elles
émettent très souvent de fausses alertes. On fait donc appel à un expert en morphologie pour résoudre ce
problème . L’approche est la suivante, on va se baser sur un système entièrement visuel (appareil photo et
programme de traitement d’images) pour détecter si le niveau d’eau, dans une scène, dépasse une certaine
limite. Pour bien repérer le niveau d’eau on met une bande réfléchissante dans l’endroit concerné et le système
enregistre deux photos : une avec fash, donc en couleur et l’autre sans fash, donc en niveau de gris.
Je doit concevoir (et j’ai envie en plus ) un programme qui permet, à partir des deux images du système, de
décider s’il y a une inondation ou non. Je présente dans ce rapport la version gratuite (approche et code) de
mon programme. Et pour un programme plus pertinent et des résultats plus fiables, j’explique dans la fin de
ce document l’idée de la version premium :D.

# 1 Approche et programme

## 1.1 Idée générale

Je considère que j’ai au départ deux images, im_fash et im_nocture qui sont respectivement l’image en couleur
et l’image en niveau de gris. Dans l’image prise en fash, la bande réfléchissante reste toujours visible même
si elle est couverte d’eau. Par conte, dans l’image en niveau de gris la bande apparait très lumineuse s’il n’y
a pas d’inondation et on ne la voit pas dans le cas contraire. Par exemple dans cette image le programme doit
conclure à une absence d’inondation comme résultat. 

![image](https://user-images.githubusercontent.com/77968416/113585722-eafb5780-962c-11eb-85ea-d8ae2e9c5eed.png)

Tandis que dans cette image le programme doit alerter une présence d’inondation.

![image](https://user-images.githubusercontent.com/77968416/113585882-1b42f600-962d-11eb-9893-c62e573400d6.png)

On remarque que c’est la photo prise en obscurité qui nous indique la présence ou non d’une inondation. En
effet, on a qu’à vérifier si le niveau de la lumière de la bande réfléchissante dépasse ou non un certain seuil
qu’on fixera. Mais dans l’image im_nocture il peut y avoir des zones avec le même niveau de luminosité que
la bande réfléchissante, comment peut on être sûr qu’on est bien sur la bande ? La solution consiste à utiliser
l’image im_flash pour isoler la bande réfléchissante dans im_nocture. Et pour cela il faut d’abord réussir à
isoler proprement la bande de l’image im_flash. Trop d’isolation ! voyant ce que ça donne en terme d’étapes :

1. Afficher l’image im_fash en blanc et noir (image binaire), tel que la bande réfléchissante soit en noir
et le reste de l’image en blanc.
2. Repérer les pixels de la bande de l’image im_fash (facile puisqu’il sont tous noir) dans l’image im_nocture
et ainsi calculer la moyenne de leurs valeurs dans im_nocture.
3. Décider l’absence ou la présence d’inondation suivant la moyenne calculée dans l’étape 2, c-à-d si elle
dépasse ou non un seuil prédéfini.

## 1.2 Isoler la bande de l’image prise avec flash

pour faire ressortir la bande en noir et le reste de l’image en blanc dans l’image im_fash, je commence par
chercher le canal qui dégage le plus la bande en testant toute les possibilités et je trouve que c’est le canal bleu
qu’il me faut.

Niveau de gris obtenu sous le canal bleu :

![image](https://user-images.githubusercontent.com/77968416/113587177-b7213180-962e-11eb-805e-4f451dd224c3.png)

Niveau de gris obtenu sous le canal vert :

![image](https://user-images.githubusercontent.com/77968416/113587248-c99b6b00-962e-11eb-8674-4954c44005c7.png)

Mais on remarque que le canal bleu dégage aussi des zones avec une faible luminosité ce qui va me poser problème
lors du seuillage de mon image. Je remarque que ces zones ressort aussi dans le canal vert, tandis que la bande
devient quasiment invisible sous ce canal, j’ai eu donc l’idée de me débarrasser dans un premier lieu des zones
sombres qui sortent dans le canal bleu et vert, comment ? en seuillage l’image im_flash ouverte dans le canal
vert. En terme d’étapes voilà ce que je fais :

1. Ouvrir l’image im_flash sous le canal vert, l’image résultante est nommée im_Gvert,
2. seuiller l’image im_Gvert pour ressortir les zones sombres en noir, l’image résultante est nommée im_sombre,
3. Ouvrir l’image im_flash sous le canal bleu, l’image résultante est nommée im_Gbleu,
4. repérer les pixels noirs de im_sombre dans im_Gbleu et les mettre à 255.

Pour réaliser les étapes 1 et 2 j’utilise le bout de code suivant

<pre><code>
def extraire_sombre(im_flash, s_sombre): # S=115 c bon
    im_Gvert = im_flash[:, :, 1]#ouvrir l'im dans le canal vert
    im_Gvert_seuil = myutil.myseuil(im_Gvert, s_sombre)
    return im_Gvert_seuil
</code></pre>

et pour réaliser les étapes 3 et 4 j'utilise le bout de code suivant,

<pre><code>
def sans_sombre(im_flash, s_sombre):
    im_sombre=extraire_sombre(im_flash, s_sombre)
    im_Gbleu=im_flash[:, :, 0]#ouvrir l'im dans le canal bleu
    im_Gbleu[im_sombre<1]=255
    return im_Gbleu
 </code></pre>

Exemple d'un résultat de la fonction sans_sombre :

![image](https://user-images.githubusercontent.com/77968416/113601340-7bdc2e00-9641-11eb-9a8c-c9e7674ff652.png)

Le paramètre "s_sombre" qui sert à seuiller l’image im_Gvert je l’ai fixé par la suite à 115 après avoir fait plusieurs testes sur toutes les images dont je dispose pour essayer de trouver la valeur qui ne me fait pas perdre beaucoup d’informations dans la suite du programme et ceci par rapport à toutes les images.
Maintenant qu’on a l’image résultante de la fonction sans_sombre on peut la seuiller pour ressortir la bande réfléchissante. L’image seuillée a d’autres zones noirs à part la bande, mais qui sont nettement plus petit que la bande. Je fait une fermeture par reconstruction pour ne garder que la bande et rattraper des éventuels pixels détruits par la fermeture. Là encore je fais plusieurs testes sur toutes les images pour trouver la bonne valeur du seuil qui me permettra de garder le maximum d’informations sur la bande.
J’opte finalement pour la valeur 95, voici ce que tout ça donne en langage informatique :

<pre><code>
def bande_seule(im_flash, s_sombre, s_bande): #s_bande=95 c bon
    im_res=sans_sombre(im_flash, s_sombre)
    im_res = myutil.myseuil(im_res, s_bande)
    el_ferm = strel.build('carre', 6)
    el_recon = strel.build('diamant', 1)
    im_res = morpho.fermeture_recon(im_res, el_ferm, el_recon)
    return im_res
</code></pre>

Les six images im_flash du départ :

![image](https://user-images.githubusercontent.com/77968416/113604299-5cdf9b00-9645-11eb-8d22-dc1eb61f6868.png)

Les six images im_flash après la fonction bande_seule :

![image](https://user-images.githubusercontent.com/77968416/113605152-8947e700-9646-11eb-8aa1-e0acd2356415.png)


## 1.3 Absence/Présence de l’inondation

Le moment est venu pour que notre image im_nocturne participe à la résolution du problème et en effet elle joue un rôle primordiale. Rappelons que la fonction bande_seule nous a permis d’isoler la bande réfléchissante dans l’image im_falsh, on utilisera donc l’image résultante pour repérer les pixels de la bande dans l’image im_nocturne et calculer ainsi la moyenne de ces pixels, c’est exactement ce que fait la fonction niveau_lumiere. Ensuite on fixe un seuil qui nous permet de décider s’il y a une inondation ou non. Dans mon cas je prend un seuil de 240, je l’ai choisis en fonction des six images du projet. Celles qui ne représentent pas une inondation ont un niveau de lumière (de la bande) supérieur à 240.

<pre><code>
def niveau_lumiere(im_flash, im_nocturne, s_sombre, s_bande):
    res = bande_seule(im_flash, s_sombre, s_bande)
    n = np.mean(im_nocturne[res < 1])
    return n

def existe_inondation(im_flash, im_nocturne, s_sombre, s_bande, seuil):
    n=niveau_lumiere(im_flash, im_nocturne, s_sombre, s_bande)
    if n>seuil :
        return False
    else:
        return True
</code></pre>

# Version Premium
Mon programme n'est pas adapté pour fournir une reponse fiable à propos de l'existance d'une innondation pour n'importe quelle image donnée en etrée car le choix des paramètres s_sombre, s_bande et seuil n'est pas basé sur une approche mathématique rigoureuse. Pour une version beaucoup plus pertinente du programme j'ai pensé aux méthodes statistiques pour prendre la décision d'existence ou non d'inondation. En effet, au lieu d'avoir seulement six images avec les bonnes informations on peut avoir toute une base de données d'images labelisées qui nous permettera d'utiliser des algorithmes du machine learning.
